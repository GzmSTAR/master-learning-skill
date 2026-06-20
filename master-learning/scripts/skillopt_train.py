#!/usr/bin/env python3
"""SkillOpt-style static training and validation for master-learning."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class Check:
    name: str
    patterns: list[str]
    weight: int = 1


COMMON_CHECKS = [
    Check("trigger_unfamiliar_domain", ["unfamiliar", "domain", "framework"]),
    Check("trigger_current_sources", ["latest", "official docs", "release"]),
    Check("trigger_github", ["GitHub", "repositories", "issues"]),
    Check("trigger_papers_standards", ["papers", "standards", "spec"]),
    Check("local_truth_first", ["local", "repo", "code"]),
    Check("research_depths", ["scout", "deep", "refresh"]),
    Check("source_priority", ["official", "specs", "papers", "GitHub"]),
    Check("source_audit", ["Audit source coverage", "provisional"]),
    Check("learning_brief_contract", ["Task", "Domain", "Implementation", "Risks", "Recommendation", "Open"]),
    Check("validation_gate", ["validation gate", "acceptance criteria", "confidence"]),
    Check("anti_fabrication", ["Never fabricate", "network access fails", "Prefer primary"]),
    Check("skillopt_loop", ["rollout", "reflect", "bounded edits", "validation"]),
    Check("resource_routing", ["references/", "scripts/", "source_audit.py"]),
]

HARNESS_CHECKS = {
    "codex": [
        Check("codex_frontmatter", ["name: master-learning", "description:"]),
        Check("codex_usage", ["Codex", "Learning Brief"]),
    ],
    "claude": [
        Check("claude_frontmatter", ["context: fork", "agent: general-purpose"]),
        Check("claude_invocation", ["/master-learning", "$ARGUMENTS"]),
        Check("claude_no_implementation", ["Do not implement code", "Return a Learning Brief only"]),
    ],
}


def score_text(text: str, harness: str) -> tuple[float, list[dict]]:
    checks = COMMON_CHECKS + HARNESS_CHECKS[harness]
    rows = []
    points = 0
    total = sum(check.weight for check in checks)
    for check in checks:
        found = all(re.search(re.escape(pattern), text, re.IGNORECASE) for pattern in check.patterns)
        if found:
            points += check.weight
        rows.append({"check": check.name, "pass": found, "weight": check.weight})
    return points / total, rows


def suggested_edits(rows: list[dict]) -> list[str]:
    missing = [row["check"] for row in rows if not row["pass"]]
    suggestions = []
    if "skillopt_loop" in missing:
        suggestions.append("Add a SkillOpt-style loop section with rollout, reflection, bounded edits, and validation gates.")
    if "validation_gate" in missing:
        suggestions.append("Add a pre-implementation validation gate covering source coverage, confidence, and acceptance criteria.")
    if "local_truth_first" in missing:
        suggestions.append("Require local repo inspection before external assumptions.")
    if "resource_routing" in missing:
        suggestions.append("List reference files and helper scripts explicitly.")
    if not suggestions and missing:
        suggestions.append("Patch missing benchmark terms: " + ", ".join(missing))
    return suggestions


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a SkillOpt-style static benchmark for the master-learning skill.")
    parser.add_argument("--skill", required=True, help="Path to SKILL.md.")
    parser.add_argument("--harness", choices=["codex", "claude"], required=True)
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--output", "-o", help="Write Markdown training report.")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout.")
    args = parser.parse_args()

    text = Path(args.skill).read_text(encoding="utf-8")
    history = []
    best_score = 0.0
    for iteration in range(1, args.iterations + 1):
        score, rows = score_text(text, args.harness)
        accepted = score >= best_score
        best_score = max(best_score, score)
        history.append(
            {
                "iteration": iteration,
                "score": round(score, 4),
                "accepted": accepted,
                "failed": [row["check"] for row in rows if not row["pass"]],
                "suggested_edits": suggested_edits(rows),
            }
        )

    payload = {
        "date": date.today().isoformat(),
        "harness": args.harness,
        "skill": args.skill,
        "best_score": round(best_score, 4),
        "passes_release_gate": best_score >= 0.90,
        "history": history,
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    if args.output:
        lines = [
            f"# SkillOpt-Style Training Run: {args.harness}",
            "",
            f"Date: {payload['date']}",
            f"Skill: `{args.skill}`",
            f"Best score: {payload['best_score']}",
            f"Release gate: {'PASS' if payload['passes_release_gate'] else 'FAIL'}",
            "",
            "## Iterations",
        ]
        for item in history:
            lines.extend(
                [
                    "",
                    f"### Iteration {item['iteration']}",
                    f"- Score: {item['score']}",
                    f"- Candidate accepted: {'yes' if item['accepted'] else 'no'}",
                    f"- Failed checks: {', '.join(item['failed']) if item['failed'] else 'none'}",
                    f"- Suggested bounded edits: {'; '.join(item['suggested_edits']) if item['suggested_edits'] else 'none'}",
                ]
            )
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")

    return 0 if payload["passes_release_gate"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
