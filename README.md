# Master Learning Skill

`master-learning` is a Codex skill for pre-project domain learning. It makes Codex research and learn unfamiliar domains before planning or implementing, especially when a task depends on current docs, papers, standards, GitHub ecosystems, examples, issues, or local code conventions.

The guiding idea is simple: a master keeps the mind of an apprentice. Before building, learn the field.

## When to Use

Use `$master-learning` when you are:

- Starting a project in an unfamiliar technical or research domain.
- Choosing a framework, library, algorithm, paper implementation, or architecture.
- Asking Codex to follow best practices, latest docs, standards, or GitHub examples.
- Working on high-risk tasks where wrong assumptions would waste implementation time.

Do not use it for trivial edits or obvious local fixes.

## Install

Clone this repository, then copy the skill folder into your Codex skills directory:

```powershell
git clone https://github.com/GzmSTAR/master-learning-skill.git
Copy-Item -Recurse -Force .\master-learning-skill\master-learning "$env:USERPROFILE\.codex\skills\master-learning"
```

Restart Codex if the skill list does not refresh automatically.

## Usage

```text
Use $master-learning to study robot vision SLAM libraries, produce a Learning Brief, then plan the implementation.
```

```text
Use $master-learning before building this paper reproduction project. Check official docs, papers, GitHub repos, and known failure modes.
```

The skill produces a `Learning Brief` covering:

- Task and learning objective
- Source table
- Domain model
- Implementation patterns
- GitHub/code lessons
- Paper/standard lessons
- Risks and anti-patterns
- Recommendation and acceptance criteria

## Contents

```text
master-learning/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
```

The scripts use only the Python standard library:

- `create_learning_brief.py`
- `github_scan.py`
- `paper_scan.py`
- `source_audit.py`
- `merge_learning_brief.py`

## Validation

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "$env:USERPROFILE\.codex\skills\master-learning"
python "$env:USERPROFILE\.codex\skills\master-learning\scripts\create_learning_brief.py" --help
python "$env:USERPROFILE\.codex\skills\master-learning\scripts\github_scan.py" --help
python "$env:USERPROFILE\.codex\skills\master-learning\scripts\paper_scan.py" --help
python "$env:USERPROFILE\.codex\skills\master-learning\scripts\source_audit.py" --help
python "$env:USERPROFILE\.codex\skills\master-learning\scripts\merge_learning_brief.py" --help
```

## License

MIT
