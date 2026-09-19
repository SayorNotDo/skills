---
name: engineering-standard
description: Apply portable engineering-quality constraints to feature, bugfix, refactor, and code-review work. Use when implementing or reviewing code that should follow project-aware architecture, readability, validation, testing, and change-scope standards; complements task-execution workflows rather than replacing them.
---

# Engineering Standard

Apply the repository's established conventions first, then use this skill to fill gaps and make quality checks explicit.

## Route the task

1. Locate `.engineering/project-profile.yaml` from the repository root.
2. If it is absent, run `python scripts/scan_project.py <repo> --output <repo>/.engineering/project-profile.yaml`, inspect the result, and adjust uncertain fields from repository evidence. Preserve an existing profile unless the user asks to replace it.
3. Read `references/core-rules.yaml`. Treat `required` rules as gates; apply `recommended` rules unless repository constraints justify an exception.
4. Read only the adapters named by `project.languages` and `project.frameworks` in the profile: `references/adapters/python.md`, `typescript.md`, `rust.md`, or `vue.md`.
5. Read exactly one matching workflow: `references/workflows/feature.md`, `bugfix.md`, `refactor.md`, or `review.md`.

## Resolve strictness

- `strict`: every applicable required and recommended rule is a gate. Record any exception with evidence.
- `balanced`: required rules are gates; recommended rules guide tradeoffs.
- `pragmatic`: required rules remain gates when applicable; prefer the smallest safe change and record deferred improvements.

Repository instructions and user requirements outrank this skill. Resolve a conflict explicitly in the delivery summary.

## Complete the task

Before delivery, account for every applicable Core Rule using implementation evidence, automated checks, or a concise exception. Run the profile's formatter, linter, type checker, and test runner when configured and relevant. Report behavior and boundaries changed, verification outcomes, exceptions or residual risks, and unrelated opportunities left untouched.

Completion is observable: requested behavior is present, applicable configured checks pass, and every applicable required rule has evidence or an explicit exception.
