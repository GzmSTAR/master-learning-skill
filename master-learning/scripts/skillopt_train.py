#!/usr/bin/env python3
"""SkillOpt-style scenario training and validation for master-learning."""

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
    Check("optimization_controls", ["Text learning rate", "Rejected assumption buffer", "Held-out validation", "Slow update"]),
    Check("regression_skip", ["trivial", "skip", "over-research"]),
    Check("resource_routing", ["references/", "scripts/", "source_audit.py", "benchmark-scenarios.json"]),
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

DEFAULT_SCENARIOS = [
    {
        "id": "latest-framework-api",
        "prompt": "Use the latest framework API correctly before coding.",
        "must_have": ["official docs", "release notes", "migration notes", "dependency versions"],
        "expected_depth": "refresh",
    },
    {
        "id": "paper-reproduction",
        "prompt": "Reproduce a paper-backed method in code.",
        "must_have": ["paper method", "assumptions", "evaluation setup", "code/data availability"],
        "expected_depth": "deep",
    },
    {
        "id": "github-adaptation",
        "prompt": "Adapt a high-star GitHub project safely.",
        "must_have": ["license", "recent activity", "examples", "tests", "issues"],
        "expected_depth": "deep",
    },
    {
        "id": "local-project-first",
        "prompt": "Plan a feature inside an existing repo.",
        "must_have": ["manifests", "configs", "tests", "existing conventions"],
        "expected_depth": "scout",
    },
    {
        "id": "low-risk-skip",
        "prompt": "Fix a typo without research.",
        "must_have": ["low-risk direct fixes", "skip deep research", "not needed"],
        "expected_depth": "skip",
    },
    {
        "id": "network-degraded",
        "prompt": "Research when network access fails.",
        "must_have": ["network-degraded", "missing external verification", "local evidence"],
        "expected_depth": "scout",
    },
]


def contains(text: str, phrase: str) -> bool:
    return re.search(re.escape(phrase), text, re.IGNORECASE) is not None


def load_scenarios(path: str | None) -> list[dict]:
    if not path:
        return DEFAULT_SCENARIOS
    return json.loads(Path(path).read_text(encoding="utf-8"))


def score_text(text: str, harness: str, scenarios: list[dict]) -> tuple[float, list[dict]]:
    checks = COMMON_CHECKS + HARNESS_CHECKS[harness]
    rows = []
    points = 0
    total = sum(check.weight for check in checks)
    for check in checks:
        found = all(contains(text, pattern) for pattern in check.patterns)
        if found:
            points += check.weight
        rows.append({"check": check.name, "pass": found, "weight": check.weight})

    for scenario in scenarios:
        required = scenario.get("must_have", [])
        found_terms = [term for term in required if contains(text, term)]
        passed = len(found_terms) == len(required)
        weight = int(scenario.get("weight", 2))
        total += weight
        if passed:
            points += weight
        rows.append(
            {
                "check": f"scenario:{scenario['id']}",
                "pass": passed,
                "weight": weight,
                "missing": [term for term in required if term not in found_terms],
            }
        )
    return points / total, rows


def suggested_edits(rows: list[dict]) -> list[str]:
    suggestions = []
    for row in rows:
        if row["pass"]:
            continue
        name = row["check"]
        if name.startswith("scenario:"):
            suggestions.append(f"Add bounded guidance for {name.removeprefix('scenario:')}: {', '.join(row.get('missing', []))}.")
        elif name == "optimization_controls":
            suggestions.append("Add SkillOpt controls: text learning rate, rejected buffer, held-out validation, and slow update.")
        elif name == "regression_skip":
            suggestions.append("Add an explicit regression rule to skip deep research for trivial direct fixes.")
        elif name == "validation_gate":
            suggestions.append("Add a pre-implementation validation gate covering source coverage, confidence, and acceptance criteria.")
        elif name == "resource_routing":
            suggestions.append("List reference files, helper scripts, and benchmark scenarios explicitly.")
        else:
            suggestions.append(f"Patch missing benchmark check: {name}.")
    return suggestions


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a SkillOpt-style scenario benchmark for the master-learning skill.")
    parser.add_argument("--skill", required=True, help="Path to SKILL.md.")
    parser.add_argument("--harness", choices=["codex", "claude"], required=True)
    parser.add_argument("--scenarios", help="JSON scenario file. Defaults to built-in scenarios.")
    parser.add_argument("--iterations", type=int, default=12)
    parser.add_argument("--output", "-o", help="Write Markdown training report.")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout.")
    args = parser.parse_args()

    text = Path(args.skill).read_text(encoding="utf-8")
    scenarios = load_scenarios(args.scenarios)
    history = []
    best_score = 0.0
    best_failed: list[str] = []
    for iteration in range(1, args.iterations + 1):
        score, rows = score_text(text, args.harness, scenarios)
        accepted = score >= best_score
        if accepted:
            best_score = score
            best_failed = [row["check"] for row in rows if not row["pass"]]
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
        "scenario_count": len(scenarios),
        "iterations": args.iterations,
        "best_score": round(best_score, 4),
        "best_failed": best_failed,
        "passes_release_gate": best_score >= 0.95 and not best_failed,
        "history": history,
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    if args.output:
        lines = [
            f"# SkillOpt-Style Scenario Training Run: {args.harness}",
            "",
            f"Date: {payload['date']}",
            f"Skill: `{args.skill}`",
            f"Scenarios: {payload['scenario_count']}",
            f"Iterations: {payload['iterations']}",
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
