#!/bin/bash
# planning-with-files: Stop hook for Codex

HOOK_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
. "${HOOK_DIR}/plan-files.sh"
resolve_planning_files

if [ ! -f "$PLAN_FILE" ]; then
    exit 0
fi

TOTAL=$(grep -cE "^### (Phase|第 .+阶段)" "$PLAN_FILE" || true)
COMPLETE=$(grep -cE "\*\*(Status|状态)[：:]\*\*[[:space:]]*complete|\[complete\]" "$PLAN_FILE" || true)
IN_PROGRESS=$(grep -cE "\*\*(Status|状态)[：:]\*\*[[:space:]]*in_progress|\[in_progress\]" "$PLAN_FILE" || true)
PENDING=$(grep -cE "\*\*(Status|状态)[：:]\*\*[[:space:]]*pending|\[pending\]" "$PLAN_FILE" || true)

if [ "$COMPLETE" -eq 0 ] && [ "$IN_PROGRESS" -eq 0 ] && [ "$PENDING" -eq 0 ]; then
    COMPLETE=$(grep -c "\[complete\]" "$PLAN_FILE" || true)
    IN_PROGRESS=$(grep -c "\[in_progress\]" "$PLAN_FILE" || true)
    PENDING=$(grep -c "\[pending\]" "$PLAN_FILE" || true)
fi

: "${TOTAL:=0}"
: "${COMPLETE:=0}"
: "${IN_PROGRESS:=0}"
: "${PENDING:=0}"

if [ "$COMPLETE" -eq "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
    echo "{\"followup_message\": \"[planning-with-files] ALL PHASES COMPLETE ($COMPLETE/$TOTAL). If the user has additional work, add new phases to $(basename "$PLAN_FILE") before starting.\"}"
    exit 0
fi

if [ "$TOTAL" -gt 0 ]; then
    echo "{\"followup_message\": \"[planning-with-files] Task incomplete ($COMPLETE/$TOTAL phases done; $IN_PROGRESS in progress, $PENDING pending). Before final response, run a plan-follow review for this turn's changes. If a Codex subagent is available and the user has authorized subagents, use one focused subagent to compare the changes against $(basename "$PLAN_FILE"). Then update $(basename "$PROGRESS_FILE") if needed.\"}"
else
    echo "{\"followup_message\": \"[planning-with-files] Active plan found: $(basename "$PLAN_FILE"). Before final response, run a plan-follow review for this turn's changes. If a Codex subagent is available and the user has authorized subagents, use one focused subagent. Then update $(basename "$PROGRESS_FILE") if needed.\"}"
fi
exit 0
