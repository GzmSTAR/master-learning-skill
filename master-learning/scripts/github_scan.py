#!/usr/bin/env python3
"""Search GitHub repositories and emit a compact candidate table."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone


def request_json(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "master-learning-skill",
    }
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def repo_age_days(updated_at: str) -> int | None:
    if not updated_at:
        return None
    updated = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - updated).days


def main() -> int:
    parser = argparse.ArgumentParser(description="Search GitHub repositories for learning candidates.")
    parser.add_argument("query", help="GitHub search query, for example 'rust web framework'.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum repositories to return.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = parser.parse_args()

    q = urllib.parse.urlencode(
        {
            "q": args.query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(max(args.limit, 1), 50),
        }
    )
    url = f"https://api.github.com/search/repositories?{q}"
    try:
        payload = request_json(url)
    except urllib.error.HTTPError as exc:
        sys.stderr.write(f"GitHub scan degraded: HTTP {exc.code}. Try GITHUB_TOKEN for higher limits.\n")
        return 2
    except Exception as exc:
        sys.stderr.write(f"GitHub scan degraded: {exc}\n")
        return 2

    rows = []
    for item in payload.get("items", [])[: args.limit]:
        rows.append(
            {
                "name": item.get("full_name"),
                "url": item.get("html_url"),
                "stars": item.get("stargazers_count"),
                "updated_at": item.get("updated_at"),
                "stale_days": repo_age_days(item.get("updated_at")),
                "language": item.get("language"),
                "license": (item.get("license") or {}).get("spdx_id"),
                "description": item.get("description") or "",
            }
        )

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print("| Repo | Stars | Updated | Language | License | Notes |")
        print("|---|---:|---:|---|---|---|")
        for row in rows:
            notes = row["description"].replace("|", "\\|")
            print(
                f"| [{row['name']}]({row['url']}) | {row['stars']} | {row['updated_at']} | "
                f"{row['language'] or ''} | {row['license'] or ''} | {notes} |"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
