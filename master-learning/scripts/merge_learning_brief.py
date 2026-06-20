#!/usr/bin/env python3
"""Merge scan outputs into a draft Learning Brief."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def load_json(path: str | None) -> list[dict]:
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    return [data]


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge GitHub and paper scan JSON into a brief draft.")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--goal", default="")
    parser.add_argument("--mode", choices=["scout", "deep", "refresh"], default="scout")
    parser.add_argument("--github-json", help="JSON output from github_scan.py --json")
    parser.add_argument("--paper-json", help="JSON output from paper_scan.py --json")
    parser.add_argument("--output", "-o", help="Output Markdown path. Defaults to stdout.")
    args = parser.parse_args()

    repos = load_json(args.github_json)
    papers = load_json(args.paper_json)

    lines = [
        f"# Learning Brief: {args.topic}",
        "",
        f"Generated: {date.today().isoformat()}",
        f"Mode: {args.mode}",
        "",
        "## Task",
        f"- User goal: {args.goal or args.topic}",
        "- Target environment:",
        "- Success criteria:",
        "- Confidence: provisional until primary sources and local code are reviewed",
        "",
        "## Source Table",
        "| Source | Type | Date/Currency | Reliability | Key Use |",
        "|---|---|---:|---|---|",
    ]
    for repo in repos:
        lines.append(
            f"| [{repo.get('name')}]({repo.get('url')}) | GitHub | {repo.get('updated_at', '')} | inspect | implementation pattern |"
        )
    for paper in papers:
        link = paper.get("doi") or paper.get("url") or ""
        title = (paper.get("title") or "").replace("|", "\\|")
        lines.append(f"| [{title}]({link}) | {paper.get('source')} | {paper.get('year', '')} | inspect | research evidence |")

    lines.extend(
        [
            "",
            "## Domain Model",
            "- Key concepts:",
            "- Objects/data:",
            "- Relationships:",
            "",
            "## Implementation Patterns",
            "- Recommended architecture:",
            "- Important APIs/contracts:",
            "- Testing pattern:",
            "",
            "## GitHub/Code Lessons",
            "- Repositories reviewed:",
            "- Useful patterns:",
            "- Reuse/license notes:",
            "",
            "## Paper/Standard Lessons",
            "- Papers/specs reviewed:",
            "- Methods or requirements:",
            "- Limits and assumptions:",
            "",
            "## Risks and Anti-Patterns",
            "- Risks:",
            "- Edge cases:",
            "- Things to avoid:",
            "",
            "## Recommendation",
            "- Build approach:",
            "- Acceptance criteria:",
            "- Next steps:",
            "",
            "## Open Questions",
            "- Unresolved:",
            "- What needs user input:",
            "- What needs more research:",
            "",
        ]
    )
    text = "\n".join(lines)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
