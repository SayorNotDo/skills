# Personal Codex Skills

Portable skills synchronized across computers.

## First installation

Clone this repository as the user-level skills directory:

```bash
git clone git@github.com:SayorNotDo/skills.git ~/.agents/skills
```

On PowerShell, the same location can be written as:

```powershell
git clone git@github.com:SayorNotDo/skills.git "$HOME\.agents\skills"
```

Use this only when `~/.agents/skills` does not already contain personal skills. If it does, clone elsewhere and link or copy each skill directory into `~/.agents/skills`.

## Update

```bash
git -C ~/.agents/skills pull --ff-only
```

Codex normally detects skill changes automatically. Restart Codex if a new or updated skill does not appear.

## Included skills

- [engineering-standard](engineering-standard/README.md): project-aware quality constraints for feature, bugfix, refactor, and review work. Its scanner requires Python 3.11+ and uses only the standard library.

## Use and improve engineering-standard

Ask Codex to use `$engineering-standard` for a development or review task. Start with the [skill instructions](engineering-standard/SKILL.md) and [usage guide](engineering-standard/README.md) for supported tools, profile setup, and limitations.

When actual use exposes a problem, capture the scenario, expected behavior, actual behavior, and evidence. Then reproduce it, make a focused improvement, verify it, and publish a reviewed update.

- [Usage feedback template](engineering-standard/assets/usage-feedback.md): record an observed problem and supporting evidence.
- [Continuous improvement workflow](engineering-standard/references/continuous-improvement.md): decide whether the correction belongs in project configuration, scanner code, an adapter, or shared rules.
- [Evaluation protocol](engineering-standard/evals/README.md): compare skill versions or a no-skill baseline using repeatable tasks and recorded results.
- [Review without writes case](engineering-standard/evals/cases/review-no-writes.yaml): a synthetic regression scenario for preserving files during review.

Normal use does not automatically edit or publish the skill. Share sanitized cases; raw evaluation results stay local and are ignored by Git.

## Validation status

The scanner has 15 passing regression tests, and YAML, profile schema, and skill structure checks have passed. These checks validate the implementation and packaging. The agent behavior case above has not yet been executed, so end-to-end effectiveness has not yet been established. See the [verification instructions](engineering-standard/README.md#verification) to repeat local checks.
