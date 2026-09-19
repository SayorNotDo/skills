# Engineering Standard Skill

A portable MVP for applying consistent engineering-quality constraints across repositories. Copy this directory into a Codex skills directory or keep it inside a repository and invoke its `SKILL.md`.

## Responsibility boundary

Superpowers-style workflows answer **how the agent executes a task**: discovery, brainstorming, planning, decomposition, debugging, and iterative verification.

Engineering Standard answers **what quality the resulting change must satisfy**: boundaries, responsibilities, complexity, naming, validation, errors, tests, dependencies, and change scope.

They compose naturally: use the execution workflow to organize the work and this skill to constrain the implementation and review it. This MVP does not include a full CLI, database, or Web UI.

## Layout

```text
engineering-standard/
├── SKILL.md
├── agents/openai.yaml
├── assets/project-profile.yaml
├── references/
│   ├── core-rules.yaml
│   ├── project-profile.schema.yaml
│   ├── adapters/{python,typescript,rust,vue}.md
│   └── workflows/{feature,bugfix,refactor,review}.md
└── scripts/scan_project.py
```

## Quick start

```bash
python scripts/scan_project.py /path/to/repository
python scripts/scan_project.py /path/to/repository --output /path/to/repository/.engineering/project-profile.yaml
```

The scanner uses only the Python standard library. It preserves an existing output file unless `--force` is supplied. Review generated values because detection is intentionally conservative.

## Profile lifecycle

The first run creates `.engineering/project-profile.yaml`. Later runs read that profile rather than rescanning. Edit it when the project's tools or architecture change. The schema documents allowed fields and values.

## Verification

From this directory:

```bash
python -m unittest discover -s tests -v
python scripts/scan_project.py .
python /path/to/skill-creator/scripts/quick_validate.py .
```
