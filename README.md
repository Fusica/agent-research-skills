# Codex Research Skills Bundle

Personal sync bundle for the 31 `agent-research-skills` style research skills installed under `~/.codex/skills`.

This repository intentionally contains only the core academic research lifecycle skills, not unrelated personal or project-local skills.

## Contents

- Research discovery and planning: `github-research`, `deep-research`, `literature-search`, `literature-review`, `idea-generation`, `novelty-assessment`, `research-planning`
- Method design: `atomic-decomposition`, `algorithm-design`, `math-reasoning`, `symbolic-equation`
- Experiment pipeline: `experiment-design`, `experiment-code`, `code-debugging`, `data-analysis`
- Paper writing: `paper-writing-section`, `related-work-writing`, `survey-generation`, `paper-to-code`
- Figures, tables, and citations: `figure-generation`, `table-generation`, `citation-management`, `backward-traceability`
- LaTeX and compilation: `latex-formatting`, `paper-compilation`, `excalidraw-skill`
- Review and polish: `self-review`, `paper-revision`, `rebuttal-writing`, `slide-generation`, `paper-assembly`

## Install

On a new computer, clone this repository and install the skills:

```bash
git clone https://github.com/Fusica/agent-research-skills.git
cd agent-research-skills
./install.sh
```

By default, existing skills are left untouched. To replace existing copies:

```bash
./install.sh --force
```

The installer writes to:

```bash
${CODEX_HOME:-$HOME/.codex}/skills
```

Restart Codex after installing or updating skills.

## Update Existing Computer

From an existing checkout of this repository:

```bash
git pull
./install.sh --force
```

Or use the helper script:

```bash
./update.sh
```

`update.sh` pulls the latest `main` branch and overwrites the 31 bundled skills in `${CODEX_HOME:-$HOME/.codex}/skills`.

## Sync Local Edits Back

If you edit skills directly in `${CODEX_HOME:-$HOME/.codex}/skills`, copy the changed skill back into this repository before committing:

```bash
cp -R "${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>" "skills/<skill-name>"
git status
git add skills/<skill-name>
git commit -m "feat: update <skill-name> skill"
git push
```

## Notes

- The bundle was copied from the local Codex user-level skills directory and lightly normalized for Codex paths.
- Legacy upstream skill-path references in bundled Markdown have been rewritten to `${CODEX_HOME:-$HOME/.codex}/skills`.
- Some optional external tools mentioned by upstream skills may still require separate installation or a user-provided path.
- Agent research convergence state is persistent only after it is written to project files. When a project uses Planning with Files, the skills should read and update the active `task_plan.md`, `findings.md`, and `progress.md` via the bridge policy in `skills/paper-assembly/references/planning-with-files-bridge.md`.
