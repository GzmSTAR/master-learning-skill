# Research Depths

Choose the lightest depth that can make implementation decisions defensible.

## scout

Use for ordinary unfamiliar work. Spend enough effort to avoid obvious wrong assumptions.

Required coverage:
- Local project files or repo conventions, if a repo exists.
- Official docs for the main framework/library/API.
- One or more representative examples or tests.
- Known pitfalls from issues, changelogs, or migration notes when relevant.

Output: short Learning Brief with recommended approach and unresolved gaps.

## deep

Use for high-risk, research-heavy, novel, regulated, expensive, or architecture-shaping work.

Required coverage:
- Official docs, specs, or standards.
- At least three independent high-quality sources where available.
- GitHub implementation examples with recent activity and tests.
- Papers or technical reports when the task is paper-driven.
- Failure modes, security/safety implications, and validation strategy.

Output: decision-ready Learning Brief with alternatives and explicit confidence.

## refresh

Use when the domain is known but current facts may have changed.

Required coverage:
- Release notes/changelogs.
- Current official docs.
- Breaking changes and deprecations.
- Local code compatibility.

Output: delta-focused brief: what changed, what still holds, and what needs update.
