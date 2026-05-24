#!/bin/bash
# planning-with-files: Pre-tool-use hook for Codex

HOOK_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
. "${HOOK_DIR}/plan-files.sh"
resolve_planning_files

echo '{"decision": "allow"}'
exit 0
