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

From a checkout of this repository:

```bash
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

## Notes

- The bundle was copied from the local Codex user-level skills directory and lightly normalized for Codex paths.
- Legacy `~/.claude/skills` references in bundled Markdown have been rewritten to `${CODEX_HOME:-$HOME/.codex}/skills`.
- Some optional external tools mentioned by upstream skills may still require separate installation or a user-provided path.
