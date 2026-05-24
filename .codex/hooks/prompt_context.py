#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HOOK_DIR = Path(__file__).resolve().parent


def emit_system_message(message: str) -> None:
    message = message.strip()
    if not message:
        return
    json.dump({"systemMessage": message}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


def run_script(script_name: str) -> str:
    result = subprocess.run(
        ["sh", str(HOOK_DIR / script_name)],
        text=True,
        capture_output=True,
        check=False,
    )
    return "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part)


def main() -> int:
    event_name = sys.argv[1] if len(sys.argv) > 1 else "user-prompt-submit"
    script_name = "session-start.sh" if event_name == "session-start" else "user-prompt-submit.sh"
    try:
        emit_system_message(run_script(script_name))
    except Exception as exc:  # pragma: no cover
        emit_system_message(f"[planning-with-files hook] {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
