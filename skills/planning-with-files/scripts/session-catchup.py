#!/usr/bin/env python3
"""
Session Catchup Script for planning-with-files

Analyzes the previous session to find unsynced context after the last
planning file update. Designed to run on SessionStart.

Usage: python3 session-catchup.py [project-path]
"""

import json
import sys
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import orjson
except ImportError:
    orjson = None

PLANNING_FILES = [
    'task_plan.zh.md',
    'task_plan.md',
    'progress.zh.md',
    'progress.md',
    'findings.zh.md',
    'findings.md',
]
MIN_SESSION_BYTES = 5000


def json_loads(line: str) -> Optional[Dict[str, Any]]:
    """Prefer optional orjson while keeping the hook dependency-free."""
    try:
        if orjson is not None:
            data = orjson.loads(line)
        else:
            data = json.loads(line)
    except (ValueError, TypeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def normalize_for_compare(path_value: str) -> str:
    expanded = os.path.expanduser(path_value)
    try:
        return str(Path(expanded).resolve())
    except (OSError, ValueError):
        return os.path.abspath(expanded)


def resolve_active_plan_dir(project_path: str) -> Optional[Path]:
    """Resolve project-local .planning/<plan_id>/ dirs used by these hooks."""
    root = Path(project_path)
    plan_root = root / '.planning'

    env_plan = os.getenv('PLAN_ID', '').strip()
    if env_plan:
        candidate = plan_root / env_plan
        if candidate.is_dir():
            return candidate

    active_file = plan_root / '.active_plan'
    try:
        active_plan = active_file.read_text(encoding='utf-8').strip()
    except OSError:
        active_plan = ''
    if active_plan:
        candidate = plan_root / active_plan
        if candidate.is_dir():
            return candidate

    if not plan_root.is_dir():
        return None

    latest: Optional[Path] = None
    latest_mtime = -1.0
    for candidate in plan_root.iterdir():
        if not candidate.is_dir() or candidate.name.startswith('.'):
            continue
        if not any((candidate / name).exists() for name in ('task_plan.zh.md', 'task_plan.md')):
            continue
        mtime = safe_stat_mtime(candidate)
        if mtime > latest_mtime:
            latest = candidate
            latest_mtime = mtime
    return latest


def planning_file_dirs(project_path: str) -> List[Path]:
    root = Path(project_path)
    dirs: List[Path] = []
    active_dir = resolve_active_plan_dir(project_path)
    if active_dir is not None:
        dirs.append(active_dir)
    dirs.append(root)
    return dirs


def existing_planning_files(project_path: str) -> List[Path]:
    files: List[Path] = []
    seen: set[Path] = set()
    for directory in planning_file_dirs(project_path):
        for name in PLANNING_FILES:
            path = directory / name
            if path.exists() and path not in seen:
                files.append(path)
                seen.add(path)
    return files


def safe_stat_mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def is_substantial_session(session: Path) -> bool:
    try:
        return session.stat().st_size > MIN_SESSION_BYTES
    except OSError:
        return False


def read_codex_meta(session_file: Path) -> Optional[Dict[str, Any]]:
    """Read the first session_meta; later meta records may be copied parent context."""
    try:
        with open(session_file, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                data = json_loads(line)
                if not data or data.get('type') != 'session_meta':
                    continue
                payload = data.get('payload')
                return payload if isinstance(payload, dict) else None
    except OSError:
        return None
    return None


def codex_meta_cwd(meta: Dict[str, Any]) -> Optional[str]:
    cwd = meta.get('cwd')
    return cwd if isinstance(cwd, str) else None


def find_current_codex_session(sessions: List[Path]) -> Optional[Path]:
    thread_id = os.getenv('CODEX_THREAD_ID', '').strip()
    if not thread_id:
        return None

    for session in sessions:
        if thread_id in session.name:
            return session
    return None


def is_codex_project_session(session: Path, project_cmp: str) -> bool:
    if not is_substantial_session(session):
        return False

    meta = read_codex_meta(session)
    if not meta:
        return False
    source = meta.get('source')
    if isinstance(source, dict) and 'subagent' in source:
        return False
    cwd = codex_meta_cwd(meta)
    return bool(cwd and normalize_for_compare(cwd) == project_cmp)


def get_codex_sessions(project_path: str) -> Iterable[Path]:
    sessions_dir = Path(os.path.expanduser(os.getenv('CODEX_SESSIONS_DIR', '~/.codex/sessions')))
    if not sessions_dir.exists():
        return

    project_cmp = normalize_for_compare(project_path)
    sessions = sorted(sessions_dir.rglob('rollout-*.jsonl'), key=safe_stat_mtime, reverse=True)
    current = find_current_codex_session(sessions)
    if current and is_codex_project_session(current, project_cmp):
        yield current

    for session in sessions:
        if session == current:
            continue
        if is_codex_project_session(session, project_cmp):
            yield session


def get_session_candidates(project_path: str) -> Tuple[str, Iterable[Path]]:
    return 'codex', get_codex_sessions(project_path)


def parse_session_messages(session_file: Path) -> List[Dict[str, Any]]:
    """Parse all messages from a session file, preserving order."""
    messages = []
    with open(session_file, 'r', encoding='utf-8', errors='replace') as f:
        for line_num, line in enumerate(f):
            data = json_loads(line)
            if data is not None:
                data['_line_num'] = line_num
                messages.append(data)
    return messages


def planning_file_from_path(path_value: Any) -> Optional[str]:
    if not isinstance(path_value, str):
        return None
    for pf in PLANNING_FILES:
        if path_value.endswith(pf):
            return pf
    return None


def planning_file_from_paths(paths: Iterable[Any]) -> Optional[str]:
    matches = {pf for path in paths if (pf := planning_file_from_path(path))}
    for pf in PLANNING_FILES:
        if pf in matches:
            return pf
    return None


def codex_planning_update(payload: Dict[str, Any]) -> Optional[str]:
    """Use Codex's structured apply_patch result instead of parsing tool text."""
    if payload.get('type') != 'patch_apply_end' or payload.get('success') is not True:
        return None
    changes = payload.get('changes')
    return planning_file_from_paths(changes.keys()) if isinstance(changes, dict) else None


def find_last_planning_update(messages: List[Dict[str, Any]]) -> Tuple[int, Optional[str]]:
    """
    Find the last time a planning file was written/edited.
    Returns (line_number, filename) or (-1, None) if not found.
    """
    last_update_line = -1
    last_update_file = None

    for msg in messages:
        line_num = msg.get('_line_num')
        if not isinstance(line_num, int):
            continue
        msg_type = msg.get('type')

        if msg_type == 'event_msg':
            payload = msg.get('payload')
            if isinstance(payload, dict):
                planning_file = codex_planning_update(payload)
                if planning_file:
                    last_update_line = line_num
                    last_update_file = planning_file

    return last_update_line, last_update_file


def text_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ''
    return '\n'.join(
        item.get('text', '')
        for item in content
        if isinstance(item, dict) and isinstance(item.get('text'), str)
    )


def parse_codex_tool_args(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
    raw_args = payload.get('arguments', payload.get('input', ''))
    if isinstance(raw_args, dict):
        return raw_args, json.dumps(raw_args, ensure_ascii=True)
    if not isinstance(raw_args, str):
        return {}, ''
    decoded = json_loads(raw_args)
    return (decoded, raw_args) if isinstance(decoded, dict) else ({}, raw_args)


def summarize_codex_tool(payload: Dict[str, Any]) -> str:
    tool_name = payload.get('name', 'tool')
    tool_args, raw_args = parse_codex_tool_args(payload)
    if tool_name == 'exec_command':
        command = tool_args.get('cmd', raw_args)
        if isinstance(command, str):
            return f"exec_command: {command[:80]}"
    return str(tool_name)


def extract_messages_after(messages: List[Dict[str, Any]], after_line: int) -> List[Dict[str, Any]]:
    """Extract conversation messages after a certain line number."""
    result = []
    for msg in messages:
        line_num = msg.get('_line_num')
        if not isinstance(line_num, int) or line_num <= after_line:
            continue

        msg_type = msg.get('type')
        is_meta = msg.get('isMeta', False)

        if msg_type == 'user' and not is_meta:
            content = text_content(msg.get('message', {}).get('content', ''))

            if content:
                if content.startswith(('<local-command', '<command-', '<task-notification')):
                    continue
                if len(content) > 20:
                    result.append({'role': 'user', 'content': content, 'line': line_num})

        elif msg_type == 'response_item':
            payload = msg.get('payload')
            if not isinstance(payload, dict):
                continue

            payload_type = payload.get('type')
            if payload_type == 'message':
                role = payload.get('role')
                if role not in ('user', 'assistant'):
                    continue
                content = text_content(payload.get('content'))
                if role == 'user':
                    if content.startswith(('<local-command', '<command-', '<task-notification')):
                        continue
                    if len(content) > 20:
                        result.append({'role': 'user', 'content': content, 'line': line_num})
                elif content:
                    result.append({
                        'role': 'assistant',
                        'content': content[:600],
                        'tools': [],
                        'line': line_num
                    })
            elif payload_type in ('function_call', 'custom_tool_call'):
                result.append({
                    'role': 'assistant',
                    'content': '',
                    'tools': [summarize_codex_tool(payload)],
                    'line': line_num
                })

    return result


def main():
    project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    # Check if planning files exist (indicates active task)
    planning_files = existing_planning_files(project_path)
    has_planning_files = bool(planning_files)
    if not has_planning_files:
        # No planning files in this project; skip catchup to avoid noise.
        return

    runtime_name, sessions = get_session_candidates(project_path)

    # Find a substantial previous session
    target_session = None
    for session in sessions:
        target_session = session
        break

    if not target_session:
        return

    messages = parse_session_messages(target_session)
    last_update_line, last_update_file = find_last_planning_update(messages)

    # No planning updates in the target session; skip catchup output.
    if last_update_line < 0:
        return

    # Only output if there's unsynced content
    messages_after = extract_messages_after(messages, last_update_line)

    if not messages_after:
        return

    # Output catchup report
    print("\n[planning-with-files] SESSION CATCHUP DETECTED")
    print(f"Previous session: {target_session.stem}")
    print(f"Runtime: {runtime_name}")

    print(f"Last planning update: {last_update_file} at message #{last_update_line}")
    print(f"Unsynced messages: {len(messages_after)}")

    print("\n--- UNSYNCED CONTEXT ---")
    for msg in messages_after[-15:]:  # Last 15 messages
        if msg['role'] == 'user':
            print(f"USER: {msg['content'][:300]}")
        else:
            if msg.get('content'):
                print(f"CODEX: {msg['content'][:300]}")
            if msg.get('tools'):
                print(f"  Tools: {', '.join(msg['tools'][:4])}")

    print("\n--- RECOMMENDED ---")
    print("1. Run: git diff --stat")
    print("2. Read: " + ", ".join(str(path) for path in planning_files[:3]))
    print("3. Update planning files based on above context")
    print("4. Continue with task")


if __name__ == '__main__':
    main()
