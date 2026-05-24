#!/bin/bash
# planning-with-files: Post-tool-use hook for Codex

HOOK_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
. "${HOOK_DIR}/plan-files.sh"
resolve_planning_files

if [ -f "$PLAN_FILE" ]; then
    echo "[planning-with-files] Update $(basename "$PROGRESS_FILE") with what you just did. If a phase is now complete, update $(basename "$PLAN_FILE") status."
fi
exit 0
