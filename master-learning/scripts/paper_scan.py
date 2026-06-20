#!/usr/bin/env python3
"""Search CrossRef, arXiv, and PubMed public APIs for paper candidates."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "master-learning-skill"})
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "master-learning-skill"})
    with urllib.request.urlopen(req, timeout=25) as response:
        return response.read().decode("utf-8")


def crossref(query: str, limit: int) -> list[dict]:
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query": query, "rows": limit})
    data = get_json(url)
    out = []
    for item in data.get("message", {}).get("items", []):
        out.append(
            {
                "source": "CrossRef",
                "title": " ".join(item.get("title") or []),
                "year": (((item.get("published-print") or item.get("published-online") or {}).get("date-parts") or [[None]])[0][0]),
                "url": item.get("URL"),
                "doi": item.get("DOI"),
            }
        )
    return out


def arxiv(query: str, limit: int) -> list[dict]:
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": f"all:{query}", "start": 0, "max_results": limit}
    )
    text = get_text(url)
    root = ET.fromstring(text)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", default="", namespaces=ns) or "").replace("\n", " ").strip()
        published = entry.findtext("a:published", default="", namespaces=ns)
        url_value = entry.findtext("a:id", default="", namespaces=ns)
        out.append({"source": "arXiv", "title": title, "year": published[:4], "url": url_value, "doi": ""})
    return out


def pubmed(query: str, limit: int) -> list[dict]:
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "term": query, "retmode": "json", "retmax": limit}
    )
    ids = get_json(search_url).get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []
    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
    )
    data = get_json(summary_url).get("result", {})
    out = []
    for pmid in ids:
        item = data.get(pmid, {})
        out.append(
            {
                "source": "PubMed",
                "title": item.get("title", ""),
                "year": (item.get("pubdate", "")[:4]),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "doi": "",
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Search paper candidates from CrossRef, arXiv, and PubMed.")
    parser.add_argument("query", help="Search topic.")
    parser.add_argument("--limit", type=int, default=5, help="Results per source.")
    parser.add_argument("--sources", default="crossref,arxiv,pubmed", help="Comma-separated sources.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = parser.parse_args()

    sources = {s.strip().lower() for s in args.sources.split(",") if s.strip()}
    results: list[dict] = []
    degraded: list[str] = []
    for name, func in [("crossref", crossref), ("arxiv", arxiv), ("pubmed", pubmed)]:
        if name not in sources:
            continue
        try:
            results.extend(func(args.query, min(max(args.limit, 1), 20)))
        except Exception as exc:
            degraded.append(f"{name}: {exc}")

    if degraded:
        sys.stderr.write("Paper scan degraded: " + "; ".join(degraded) + "\n")

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print("| Source | Year | Title | URL/DOI |")
        print("|---|---:|---|---|")
        for row in results:
            title = row["title"].replace("|", "\\|")
            link = row.get("doi") or row.get("url") or ""
            print(f"| {row['source']} | {row.get('year') or ''} | {title} | {link} |")
    return 0 if not degraded else 2


if __name__ == "__main__":
    raise SystemExit(main())
