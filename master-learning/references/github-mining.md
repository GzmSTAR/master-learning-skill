# GitHub Mining

Do not treat stars as proof of correctness. Use stars only as a discovery signal.

## Repository Screening

Prefer repositories with:
- Recent commits or releases.
- Clear license.
- Tests, examples, CI, or benchmark scripts.
- Issues/PRs that show active maintenance.
- Documentation that explains constraints and setup.
- Code that matches the user's target language and runtime.

Be cautious with:
- Abandoned repositories.
- Repos with many stars but stale dependencies.
- Demo-only code without tests.
- Benchmarks that cannot be reproduced.
- Code copied from papers without license clarity.

## What to Read

Read in this order:
1. README and docs for problem framing.
2. Examples and tests for real usage.
3. Core modules for architecture and data flow.
4. Issues/PRs for edge cases and known failures.
5. CI and dependency files for environment assumptions.

## Lessons to Extract

For each useful repository, capture:
- What problem it solves.
- Core architecture and abstractions.
- APIs or CLI contracts.
- Dependencies and runtime assumptions.
- Testing pattern.
- Failure modes reported by users.
- Whether its code can be reused, referenced, or only learned from.
