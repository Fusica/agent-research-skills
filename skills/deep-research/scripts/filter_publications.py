#!/usr/bin/env python3
"""Pass publication JSONL records through without source or venue filtering.

The current user preference is relevance-only literature discovery: keep all
candidate papers from all sources, then let downstream reasoning rank or group
them by topical fit. This script remains as a compatibility shim for skills and
older workflows that already call filter_publications.py.
"""

from __future__ import annotations

import argparse
import json
import os
import sys


def load_jsonl(paths: list[str]) -> list[dict]:
    records = []
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
                record["_policy_input"] = os.path.basename(path)
                records.append(record)
    return records


def save_jsonl(records: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            clean = dict(record)
            clean.pop("_policy_input", None)
            for stale_key in ("priority" + "_tier", "priority" + "_venue"):
                clean.pop(stale_key, None)
            handle.write(json.dumps(clean, ensure_ascii=False) + "\n")


def write_report(report: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def filter_records(records: list[dict]) -> tuple[list[dict], dict]:
    """Compatibility API: keep all records and remove old ranking tags."""
    kept = []
    for record in records:
        clean = dict(record)
        clean.pop("_policy_input", None)
        for stale_key in ("priority" + "_tier", "priority" + "_venue"):
            clean.pop(stale_key, None)
        kept.append(clean)

    report = {
        "policy": "relevance_only_keep_all_sources",
        "total": len(records),
        "kept": len(kept),
        "rejected": 0,
        "notes": [
            "No publisher, venue, journal, DOI, domain, or preprint source was excluded.",
        ],
        "rejected_records": [],
    }
    return kept, report


def main() -> None:
    parser = argparse.ArgumentParser(description="Keep publication JSONL records without source filtering")
    parser.add_argument("--input", "--inputs", nargs="+", required=True, help="Input JSONL file(s)")
    parser.add_argument("--output", "-o", required=True, help="Output JSONL")
    parser.add_argument("--report", required=True, help="JSON report")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    kept, report = filter_records(records)
    save_jsonl(kept, args.output)
    write_report(report, args.report)
    print(
        f"Publication policy: {report['total']} -> {report['kept']} kept, 0 rejected -> {args.output}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
