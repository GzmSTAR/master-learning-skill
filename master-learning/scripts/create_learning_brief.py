#!/usr/bin/env python3
"""Create a Master Learning Brief scaffold."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


TEMPLATE = """# Learning Brief: {topic}

Generated: {today}
Mode: {mode}

## Task
- User goal: {goal}
- Target environment:
- Success criteria:
- Research depth: {mode}
- Confidence: provisional until sources are audited

## Source Table
| Source | Type | Date/Currency | Reliability | Key Use |
|---|---|---:|---|---|
|  |  |  |  |  |

## Domain Model
- Key concepts:
- Objects/data:
- Relationships:
- Vocabulary:

## Implementation Patterns
- Recommended architecture:
- Important APIs/contracts:
- Data/control flow:
- Testing pattern:
- Operational constraints:

## GitHub/Code Lessons
- Repositories reviewed:
- Useful patterns:
- Reuse/license notes:
- Known issues:

## Paper/Standard Lessons
- Papers/specs reviewed:
- Methods or requirements:
- Limits and assumptions:

## Risks and Anti-Patterns
- Risks:
- Edge cases:
- Things to avoid:

## Recommendation
- Build approach:
- Acceptance criteria:
- Next steps:

## Open Questions
- Unresolved:
- What needs user input:
- What needs more research:
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Master Learning Brief scaffold.")
    parser.add_argument("--topic", required=True, help="Topic or project domain.")
    parser.add_argument("--goal", default="", help="User goal to place in the brief.")
    parser.add_argument("--mode", choices=["scout", "deep", "refresh"], default="scout")
    parser.add_argument("--output", "-o", help="Output Markdown path. Defaults to stdout.")
    args = parser.parse_args()

    text = TEMPLATE.format(
        topic=args.topic,
        goal=args.goal or args.topic,
        mode=args.mode,
        today=date.today().isoformat(),
    )
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
