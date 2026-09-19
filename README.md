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

- `engineering-standard`: project-aware quality constraints for feature, bugfix, refactor, and review work.
