#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$ROOT_DIR/skills"
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
FORCE=0

if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Missing skills directory: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

skills=(
  github-research
  deep-research
  literature-search
  literature-review
  idea-generation
  novelty-assessment
  research-planning
  atomic-decomposition
  algorithm-design
  math-reasoning
  symbolic-equation
  experiment-design
  experiment-code
  code-debugging
  data-analysis
  paper-writing-section
  related-work-writing
  survey-generation
  paper-to-code
  figure-generation
  table-generation
  citation-management
  backward-traceability
  latex-formatting
  paper-compilation
  excalidraw-skill
  self-review
  paper-revision
  rebuttal-writing
  slide-generation
  paper-assembly
)

installed=0
skipped=0

for skill in "${skills[@]}"; do
  src="$SOURCE_DIR/$skill"
  dst="$TARGET_DIR/$skill"

  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Missing skill source: $src/SKILL.md" >&2
    exit 1
  fi

  if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then
    echo "skip existing: $skill"
    skipped=$((skipped + 1))
    continue
  fi

  if [[ -e "$dst" ]]; then
    rm -rf "$dst"
  fi

  cp -R "$src" "$dst"
  echo "installed: $skill"
  installed=$((installed + 1))
done

echo "done: installed=$installed skipped=$skipped target=$TARGET_DIR"
