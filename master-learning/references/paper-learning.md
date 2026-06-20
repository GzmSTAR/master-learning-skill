# Paper Learning

Use papers to learn mechanisms and constraints, not to decorate a brief with citations.

## When to Read Papers

Read papers when:
- The user references a method, model, algorithm, benchmark, dataset, or result.
- Engineering choices depend on empirical tradeoffs.
- The domain is research-heavy or has no stable engineering standard.
- A GitHub repo claims to implement a paper.

## Extraction Protocol

For each paper, capture:
- Problem statement and assumptions.
- Method or algorithm in implementation terms.
- Inputs, outputs, data requirements, and evaluation metrics.
- Baselines and limitations.
- Reproducibility artifacts: code, data, configs, seeds, environment.
- What should and should not be copied into the user's project.

## Engineering Translation

Convert paper lessons into:
- Interfaces and data schemas.
- Algorithms or pipeline stages.
- Test cases and benchmark checks.
- Performance and resource constraints.
- Risks where the paper setting differs from the user's setting.

Do not claim a paper supports a design unless the relevant section was actually checked.
