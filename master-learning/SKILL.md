---
name: master-learning
description: "Pre-project domain learning and research workflow for Codex. Use when starting unfamiliar, complex, high-risk, research-heavy, framework-heavy, paper-driven, GitHub-ecosystem-driven, or best-practice-sensitive projects where Codex should first study official docs, papers, standards, repositories, examples, issues, and local code before planning or implementing."
---

# Master Learning

Master Learning makes Codex act like a serious apprentice before acting like an expert. Use it to study the domain, ecosystem, source material, and implementation patterns before planning or changing code.

## Core Rule

Do not jump directly to implementation when the task depends on domain knowledge Codex has not grounded in current sources. First produce a Learning Brief. Then use the brief as the basis for the plan, design, tests, or implementation.

## Trigger Decision

Use this skill when any of these are true:

- The user asks to build in an unfamiliar domain, framework, research area, protocol, standard, or hardware/software ecosystem.
- The task mentions "research", "learn first", "best practices", "latest", "papers", "GitHub", "examples", "benchmarks", "standards", or equivalent intent in any language.
- A wrong assumption could cause wasted implementation work, unsafe design, poor academic/engineering quality, or incompatible APIs.
- The task involves selecting libraries, reproducing a paper, adapting a high-star repo, following official docs, or understanding local project conventions before editing.

Do not use this skill for trivial edits, direct bug fixes with clear local evidence, formatting-only work, or tasks where the user explicitly says not to research.

## Workflow

1. **Frame the learning goal.** Restate the project objective, audience, target environment, success criteria, and the unknowns that must be resolved.
2. **Choose research depth.** Start with `scout` unless the task is high-risk, novel, regulated, paper-driven, or source-conflicted; then use `deep`. Use `refresh` for maintenance tasks where the domain is known but dependencies may have changed.
3. **Collect sources in priority order.** Prefer official docs and local repo truth first, then standards/specs, papers, high-quality GitHub repos, examples/tests/issues, and credible engineering writeups.
4. **Learn patterns, not trivia.** Extract domain concepts, data/control flow, API contracts, common architectures, edge cases, failure modes, testing approaches, and anti-patterns.
5. **Audit source coverage.** Mark gaps clearly. If no official source, no code example, or no current source exists, label the conclusion as provisional.
6. **Produce a Learning Brief.** Keep it actionable: what to build, what to avoid, what to verify, and what assumptions remain.
7. **Proceed only after grounding.** Use the Learning Brief to make the implementation plan or code changes. If the brief exposes unresolved critical risk, ask or research further before implementation.

## SkillOpt-Style Validation Gate

This skill is optimized with a SkillOpt-inspired loop: rollout tasks, reflect on failures, apply bounded edits, and keep a candidate only when validation improves. At task time, use the same discipline:

- Treat the Learning Brief as the trainable procedure for the current project, not as a decorative report.
- Make bounded updates when evidence changes: add, delete, or replace only the rules needed to improve the next decision.
- Preserve rejected assumptions in the brief so they are not reintroduced later.
- Before implementation, run a validation gate: source coverage, local code fit, risk review, and acceptance criteria.
- If the validation gate fails, improve the brief instead of coding through uncertainty.

## Training Discipline

Use these SkillOpt-style controls during long projects or repeated skill improvement:

- **Text learning rate:** prefer one or two precise rule edits after each failure, not a full rewrite.
- **Rejected assumption buffer:** record assumptions that were disproven, such as stale APIs, abandoned repositories, incompatible licenses, weak papers, or examples that do not match the user's runtime.
- **Held-out validation:** test the updated brief against a different scenario before trusting the new rule.
- **Slow update:** if the same failure appears across multiple tasks, promote it from a one-off note into `SKILL.md` or a reference file.
- **Regression check:** confirm the skill still skips trivial tasks and does not over-research direct fixes.

## Scenario Handling Rules

- For **latest framework/API tasks**, verify official docs, release notes, migration notes, and local dependency versions before recommending code.
- For **paper reproduction tasks**, read the paper method, assumptions, evaluation setup, code/data availability, and mismatch with the user's environment.
- For **GitHub adaptation tasks**, inspect license, recent activity, examples, tests, issues, dependency health, and whether reuse is allowed or only learning is appropriate.
- For **local project tasks**, inspect manifests, configs, tests, docs, and existing conventions before external sources.
- For **low-risk direct fixes**, explicitly skip deep research and state why the skill is not needed.
- For **network-degraded tasks**, label missing external verification and continue only with local evidence or ask for permission/input when required.

## Output Contract

Every Learning Brief must include:

- `Task`: learning objective, target environment, success criteria, research depth, and confidence.
- `Sources`: URLs/paths, type, date/currency when available, reliability, and key use.
- `Domain Model`: key concepts, objects, terms, and relationships.
- `Local Code Lessons`: project structure, conventions, constraints, and relevant files when local code exists.
- `GitHub/Code Lessons`: repositories reviewed, useful patterns, license/reuse notes, and issues.
- `Paper/Standard Lessons`: methods, requirements, limits, and assumptions.
- `Implementation Patterns`: architecture, APIs/contracts, data/control flow, tests, and operational constraints.
- `Risks and Anti-Patterns`: edge cases, weak assumptions, and things to avoid.
- `Recommendation`: recommended approach, acceptance criteria, and next steps.
- `Open Questions`: unresolved decisions or missing evidence.

Use `references/learning-brief-template.md` when a structured Markdown artifact is useful.

## Bundled Resources

Read these files only when relevant:

- `references/research-depths.md`: choose `scout`, `deep`, or `refresh`.
- `references/source-quality-rubric.md`: score and compare sources.
- `references/github-mining.md`: inspect GitHub repositories without being fooled by stars alone.
- `references/paper-learning.md`: turn papers into engineering constraints.
- `references/skillopt-training.md`: SkillOpt-inspired optimization protocol used for this skill.
- `references/learning-brief-template.md`: produce a consistent brief.
- `references/anti-patterns.md`: avoid common failure modes.
- `training/benchmark-scenarios.json`: held-out scenario set used to regression-test this skill.

Scripts are optional helpers:

- `scripts/create_learning_brief.py`: create a Learning Brief scaffold.
- `scripts/github_scan.py`: search GitHub repositories and export candidates.
- `scripts/paper_scan.py`: search CrossRef, arXiv, and PubMed public APIs.
- `scripts/source_audit.py`: check source coverage and warn about weak grounding.
- `scripts/merge_learning_brief.py`: merge scan outputs into a brief draft.
- `scripts/skillopt_train.py`: run the local SkillOpt-style scenario training and validation benchmark.

## Integrity Rules

- Never fabricate source findings, citations, repository contents, or API behavior.
- If network access fails, say the research was degraded and explain what was not checked.
- Prefer primary sources over summaries.
- For "latest" claims, verify current docs or releases before relying on memory.
- Treat one blog post, one Stack Overflow answer, or one README as insufficient for high-risk decisions.
- When sources disagree, preserve the disagreement and recommend the safest verifiable path.
