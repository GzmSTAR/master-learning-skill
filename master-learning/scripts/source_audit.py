#!/usr/bin/env python3
"""Audit a Learning Brief or source list for minimum grounding coverage."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CATEGORIES = {
    "official": re.compile(r"official|docs?\.|developer|spec|standard|release notes|changelog", re.I),
    "github": re.compile(r"github\.com|repository|repo|source code", re.I),
    "paper": re.compile(r"doi\.org|arxiv|pubmed|crossref|paper|journal|proceedings", re.I),
    "local_code": re.compile(r"local code|workspace|repo path|tests?|src/|package\.json|pyproject|cargo\.toml", re.I),
}


def read_sources(path: Path) -> str:
    if path.suffix.lower() == ".json":
        return json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False)
    return path.read_text(encoding="utf-8")


def source_evidence(text: str) -> str:
    lines = text.splitlines()
    in_table = False
    rows: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("## source table"):
            in_table = True
            continue
        if in_table and stripped.startswith("## "):
            break
        if not in_table or not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or cells[0].lower() == "source" or set("".join(cells)) <= {"-", ":"}:
            continue
        if any(cell for cell in cells):
            rows.append(" ".join(cells))
    if rows:
        return "\n".join(rows)
    return text if "http://" in text or "https://" in text else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit source coverage for a Master Learning Brief.")
    parser.add_argument("path", help="Markdown or JSON source artifact.")
    parser.add_argument("--mode", choices=["scout", "deep", "refresh"], default="scout")
    args = parser.parse_args()

    text = source_evidence(read_sources(Path(args.path)))
    found = {name: bool(pattern.search(text)) for name, pattern in CATEGORIES.items()}
    warnings = []

    if not found["official"]:
        warnings.append("Missing official docs/spec/release-note evidence.")
    if not found["github"] and args.mode in {"scout", "deep"}:
        warnings.append("Missing GitHub or implementation example evidence.")
    if not found["paper"] and args.mode == "deep":
        warnings.append("Deep mode should include papers/standards when available.")
    if not found["local_code"]:
        warnings.append("No local code/workspace evidence detected; confirm whether a repo exists.")

    print("# Source Audit")
    print()
    print(f"Mode: {args.mode}")
    print()
    print("| Category | Found |")
    print("|---|---:|")
    for name, value in found.items():
        print(f"| {name} | {'yes' if value else 'no'} |")
    print()

    if warnings:
        print("## Warnings")
        for warning in warnings:
            print(f"- {warning}")
        print()
        print("Conclusion: grounding is provisional until warnings are resolved or explicitly accepted.")
        return 2

    print("Conclusion: minimum source coverage found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
