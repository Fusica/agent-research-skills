#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$ROOT_DIR/skills"
HOOKS_JSON_SOURCE="$ROOT_DIR/.codex/hooks.json"
HOOKS_SOURCE_DIR="$ROOT_DIR/.codex/hooks"

FORCE=0
INSTALL_HOOKS=1
REWRITE_PATHS=1
TARGET_EXPLICIT=0
TARGET_PROJECT="${CODEX_PROJECT:-$PWD}"

usage() {
  cat <<'EOF'
Usage: install.sh [options]

Install all bundled skills into a project-local Codex directory:
  <project>/.codex/skills

Options:
  --target <path>   Project root to install into. Defaults to the current directory.
  --force           Replace existing bundled skills and planning hook files.
  --no-hooks        Install skills only; do not install .codex hooks.
  --no-rewrite      Do not rewrite copied skill path references to project-local paths.
  -h, --help        Show this help.

Examples:
  # From the target project:
  /path/to/agent-research-skills/install.sh --force

  # From this bundle checkout:
  ./install.sh --target /path/to/project --force
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=1
      ;;
    --target)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --target" >&2
        exit 2
      fi
      TARGET_PROJECT="$2"
      TARGET_EXPLICIT=1
      shift
      ;;
    --target=*)
      TARGET_PROJECT="${1#--target=}"
      TARGET_EXPLICIT=1
      ;;
    --no-hooks)
      INSTALL_HOOKS=0
      ;;
    --no-rewrite)
      REWRITE_PATHS=0
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Missing skills directory: $SOURCE_DIR" >&2
  exit 1
fi

if [[ ! -d "$TARGET_PROJECT" ]]; then
  echo "Target project does not exist: $TARGET_PROJECT" >&2
  exit 1
fi

TARGET_PROJECT="$(cd "$TARGET_PROJECT" && pwd)"

if [[ "$TARGET_PROJECT" == "$ROOT_DIR" && "$TARGET_EXPLICIT" -ne 1 ]]; then
  echo "Refusing to install into the bundle checkout by default." >&2
  echo "Run this installer from your target project, or pass --target /path/to/project." >&2
  exit 2
fi

TARGET_CODEX_DIR="$TARGET_PROJECT/.codex"
TARGET_SKILLS_DIR="$TARGET_CODEX_DIR/skills"
TARGET_HOOKS_JSON="$TARGET_CODEX_DIR/hooks.json"
TARGET_HOOKS_DIR="$TARGET_CODEX_DIR/hooks"

mkdir -p "$TARGET_SKILLS_DIR"

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
  planning-with-files
)

installed=0
skipped=0
hooks_installed=0
hooks_skipped=0
rewritten=0
copy_path_result=""

copy_path() {
  local src="$1"
  local dst="$2"
  local label="$3"

  if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then
    echo "skip existing: $label"
    skipped=$((skipped + 1))
    copy_path_result="skipped"
    return 0
  fi

  if [[ -e "$dst" ]]; then
    rm -rf "$dst"
  fi

  mkdir -p "$(dirname "$dst")"
  cp -R "$src" "$dst"
  echo "installed: $label"
  installed=$((installed + 1))
  copy_path_result="installed"
}

rewrite_skill_paths() {
  local root="$1"
  local escaped_target
  escaped_target="$(printf '%s' "$TARGET_SKILLS_DIR" | sed -e 's/[&|\\]/\\&/g')"

  while IFS= read -r -d '' file; do
    if ! grep -Iq . "$file"; then
      continue
    fi
    if grep -q '\${CODEX_HOME:-\$HOME/.codex}/skills\|~/.codex/skills' "$file"; then
      perl -0pi -e 's|\$\{CODEX_HOME:-\$HOME/\.codex\}/skills|'"$escaped_target"'|g; s|~/.codex/skills|'"$escaped_target"'|g' "$file"
      rewritten=$((rewritten + 1))
    fi
  done < <(find "$root" -type f -print0)
}

for skill in "${skills[@]}"; do
  src="$SOURCE_DIR/$skill"
  dst="$TARGET_SKILLS_DIR/$skill"

  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Missing skill source: $src/SKILL.md" >&2
    exit 1
  fi

  copy_path "$src" "$dst" "skill:$skill"

  if [[ "$REWRITE_PATHS" -eq 1 && "$copy_path_result" == "installed" && -d "$dst" ]]; then
    rewrite_skill_paths "$dst"
  fi
done

if [[ "$INSTALL_HOOKS" -eq 1 ]]; then
  if [[ ! -f "$HOOKS_JSON_SOURCE" ]]; then
    echo "Missing hooks config: $HOOKS_JSON_SOURCE" >&2
    exit 1
  fi
  if [[ ! -d "$HOOKS_SOURCE_DIR" ]]; then
    echo "Missing hooks directory: $HOOKS_SOURCE_DIR" >&2
    exit 1
  fi

  mkdir -p "$TARGET_HOOKS_DIR"

  if [[ -e "$TARGET_HOOKS_JSON" && "$FORCE" -ne 1 ]]; then
    echo "skip existing: hooks.json"
    hooks_skipped=$((hooks_skipped + 1))
  else
    if [[ -e "$TARGET_HOOKS_JSON" ]]; then
      rm -f "$TARGET_HOOKS_JSON"
    fi
    cp "$HOOKS_JSON_SOURCE" "$TARGET_HOOKS_JSON"
    echo "installed: hooks.json"
    hooks_installed=$((hooks_installed + 1))
  fi

  while IFS= read -r -d '' src; do
    name="$(basename "$src")"
    dst="$TARGET_HOOKS_DIR/$name"

    if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then
      echo "skip existing: hook:$name"
      hooks_skipped=$((hooks_skipped + 1))
      continue
    fi

    if [[ -e "$dst" ]]; then
      rm -rf "$dst"
    fi

    cp -R "$src" "$dst"
    echo "installed: hook:$name"
    hooks_installed=$((hooks_installed + 1))
  done < <(find "$HOOKS_SOURCE_DIR" -mindepth 1 -maxdepth 1 ! -name '__pycache__' -print0)
fi

echo "done: skills_installed=$installed skipped=$skipped hooks_installed=$hooks_installed hooks_skipped=$hooks_skipped rewritten_files=$rewritten target=$TARGET_CODEX_DIR"
echo "note: Codex must have [features] hooks = true in ~/.codex/config.toml, and may ask you to trust newly installed project hooks."
