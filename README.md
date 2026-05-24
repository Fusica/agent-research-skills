# Codex Research Skills Bundle

Project-local sync bundle for the 31 `agent-research-skills` research skills plus `planning-with-files`.

The installer writes into the project you choose, not into the user-level `~/.codex/skills` directory. It also installs the Planning with Files Codex hooks so the project can use persistent plan files and session recovery.

## Contents

- Research discovery and planning: `github-research`, `deep-research`, `literature-search`, `literature-review`, `idea-generation`, `novelty-assessment`, `research-planning`
- Method design: `atomic-decomposition`, `algorithm-design`, `math-reasoning`, `symbolic-equation`
- Experiment pipeline: `experiment-design`, `experiment-code`, `code-debugging`, `data-analysis`
- Paper writing: `paper-writing-section`, `related-work-writing`, `survey-generation`, `paper-to-code`
- Figures, tables, and citations: `figure-generation`, `table-generation`, `citation-management`, `backward-traceability`
- LaTeX and compilation: `latex-formatting`, `paper-compilation`, `excalidraw-skill`
- Review and polish: `self-review`, `paper-revision`, `rebuttal-writing`, `slide-generation`, `paper-assembly`
- Persistent planning: `planning-with-files` plus `.codex/hooks.json` and `.codex/hooks/`

## Install Into A Project

Clone this repository once:

```bash
git clone https://github.com/Fusica/agent-research-skills.git
```

From the project you want Codex to use:

```bash
/path/to/agent-research-skills/install.sh
```

To replace existing project-local copies:

```bash
/path/to/agent-research-skills/install.sh --force
```

Or run from this bundle checkout and pass the target project explicitly:

```bash
./install.sh --target /path/to/project --force
```

The installer writes to:

```bash
<project>/.codex/skills
<project>/.codex/hooks.json
<project>/.codex/hooks/
```

It rewrites copied skill path references to the target project's absolute `.codex/skills` path, so the bundled scripts do not depend on `~/.codex/skills`.

Codex hooks also require this feature flag in `~/.codex/config.toml`:

```toml
[features]
hooks = true
```

After installing or updating project-local skills/hooks, restart Codex. Codex may ask you to trust the newly installed project hooks.

## Update Existing Checkout

From an existing checkout of this repository:

```bash
git pull
./install.sh --target /path/to/project --force
```

Or use the helper script:

```bash
./update.sh --target /path/to/project
```

`update.sh` pulls the latest `main` branch and then runs `install.sh --force`.

## Sync Local Edits Back

If you edit project-local skills directly, copy the changed skill back into this repository before committing:

```bash
cp -R "/path/to/project/.codex/skills/<skill-name>" "skills/<skill-name>"
git status
git add skills/<skill-name>
git commit -m "feat: update <skill-name> skill"
git push
```

If you edit project-local Planning with Files hooks, copy the hook bundle back too:

```bash
cp "/path/to/project/.codex/hooks.json" ".codex/hooks.json"
cp -R "/path/to/project/.codex/hooks/." ".codex/hooks/"
```

## Notes

- The 31 research skills were copied from the local Codex user-level skills directory and lightly normalized for Codex paths.
- `planning-with-files` and the hook bundle are synchronized from the project-local Aerial Gym Codex setup.
- Existing project-local skills and hook files are left untouched unless you pass `--force`.
- Agent research convergence state is persistent only after it is written to project files. When a project uses Planning with Files, the skills should read and update the active `task_plan.md`, `findings.md`, and `progress.md` via the bridge policy in `skills/paper-assembly/references/planning-with-files-bridge.md`.
