# Source Quality Rubric

Rate sources by authority, relevance, currency, and reproducibility.

## Tiers

1. Primary and authoritative:
   - Official documentation, specs, standards, source code, release notes, API references.
   - Peer-reviewed papers for academic claims.
2. Strong implementation evidence:
   - Well-maintained GitHub repos with tests, examples, recent commits, and active issues.
   - Vendor examples and benchmark suites.
3. Useful context:
   - Engineering blog posts with code and dates.
   - Conference talks with linked artifacts.
4. Weak support:
   - Old tutorials, unmaintained repos, unsourced summaries, forum comments.
5. Do not rely on:
   - AI-generated answers without source verification.
   - Copied code with unclear license.
   - Unverifiable citations or repository claims.

## Minimum Coverage

For `scout`, use at least one primary source and one implementation example when available.

For `deep`, use primary docs/specs plus multiple independent implementation or academic sources.

If minimum coverage is impossible, mark the brief as provisional and list exactly what could not be verified.

## Currency

Prefer current sources. Treat old sources as risky when the task depends on APIs, dependencies, security, regulations, benchmarks, pricing, or model capabilities.
