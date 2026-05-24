#!/bin/sh
# Shared planning-with-files path resolution for project-local hooks.

first_existing_file() {
    for candidate in "$@"; do
        if [ -f "$candidate" ]; then
            printf "%s\n" "$candidate"
            return 0
        fi
    done
    printf "%s\n" "$1"
}

resolve_planning_files() {
    HOOK_DIR="${HOOK_DIR:-$(CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd)}"
    PLAN_DIR="$(sh "${HOOK_DIR}/resolve-plan-dir.sh" 2>/dev/null)"
    PLAN_PREFIX="${PLAN_DIR:+${PLAN_DIR}/}"

    PLAN_FILE="$(first_existing_file "${PLAN_PREFIX}task_plan.zh.md" "${PLAN_PREFIX}task_plan.md")"
    PROGRESS_FILE="$(first_existing_file "${PLAN_PREFIX}progress.zh.md" "${PLAN_PREFIX}progress.md")"
    FINDINGS_FILE="$(first_existing_file "${PLAN_PREFIX}findings.zh.md" "${PLAN_PREFIX}findings.md")"
}
