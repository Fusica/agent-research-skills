#!/usr/bin/env python3
"""Filter and tag publication JSONL records by venue and publisher quality policy."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse


DOI_PREFIX_BLOCKS = {
    "10.3390": "MDPI DOI prefix",
    "10.3389": "Frontiers DOI prefix",
    "10.1155": "Hindawi DOI prefix",
}

PUBLISHER_BLOCKS = {
    "mdpi": "blocked publisher: MDPI",
    "frontiers media": "blocked publisher: Frontiers Media",
    "hindawi": "blocked publisher: Hindawi",
    "omics international": "blocked publisher: OMICS International",
    "waset": "blocked publisher: WASET",
    "scientific research publishing": "blocked publisher: SCIRP",
    "scirp": "blocked publisher: SCIRP",
    "science publishing group": "blocked publisher: Science Publishing Group",
    "academic journals": "blocked publisher: Academic Journals",
    "iosr journals": "blocked publisher: IOSR Journals",
    "iiste": "blocked publisher: IISTE",
    "david publishing": "blocked publisher: David Publishing",
    "medcrave": "blocked publisher: MedCrave",
    "herald scholarly open access": "blocked publisher: Herald Scholarly Open Access",
    "crimson publishers": "blocked publisher: Crimson Publishers",
    "juniper publishers": "blocked publisher: Juniper Publishers",
    "longdom": "blocked publisher: Longdom Publishing",
    "austin publishing group": "blocked publisher: Austin Publishing Group",
    "bentham open": "blocked publisher: Bentham Open",
    "allied academies": "blocked publisher: Allied Academies",
    "baishideng": "blocked publisher: Baishideng Publishing Group",
    "gavin publishers": "blocked publisher: Gavin Publishers",
    "remedy publications": "blocked publisher: Remedy Publications",
    "jacobs publishers": "blocked publisher: Jacobs Publishers",
    "pulsus": "blocked publisher: Pulsus Group",
    "scires literature": "blocked publisher: SciRes Literature",
    "open access text": "blocked publisher: Open Access Text",
}

DOMAIN_BLOCKS = {
    "mdpi.com": "blocked domain: MDPI",
    "mdpi-res.com": "blocked domain: MDPI",
    "frontiersin.org": "blocked domain: Frontiers",
    "hindawi.com": "blocked domain: Hindawi",
    "omicsonline.org": "blocked domain: OMICS",
    "waset.org": "blocked domain: WASET",
    "scirp.org": "blocked domain: SCIRP",
    "sciencepublishinggroup.com": "blocked domain: Science Publishing Group",
    "academicjournals.org": "blocked domain: Academic Journals",
    "iosrjournals.org": "blocked domain: IOSR Journals",
    "iiste.org": "blocked domain: IISTE",
    "davidpublisher.com": "blocked domain: David Publishing",
    "medcraveonline.com": "blocked domain: MedCrave",
    "heraldopenaccess.us": "blocked domain: Herald Open Access",
    "crimsonpublishers.com": "blocked domain: Crimson Publishers",
    "juniperpublishers.com": "blocked domain: Juniper Publishers",
    "longdom.org": "blocked domain: Longdom",
    "austinpublishinggroup.com": "blocked domain: Austin Publishing Group",
    "benthamscience.com/open": "blocked domain: Bentham Open",
    "alliedacademies.org": "blocked domain: Allied Academies",
    "baishideng.com": "blocked domain: Baishideng",
    "gavinpublishers.com": "blocked domain: Gavin Publishers",
    "remedypublications.com": "blocked domain: Remedy Publications",
    "jacobspublishers.com": "blocked domain: Jacobs Publishers",
    "pulsus.com": "blocked domain: Pulsus",
    "sciresliterature.org": "blocked domain: SciRes Literature",
    "oatext.com": "blocked domain: Open Access Text",
}

JOURNAL_TITLE_BLOCKS = {
    "drones": "blocked journal title",
    "sensors": "blocked journal title",
    "remote sensing": "blocked journal title",
    "applied sciences": "blocked journal title",
    "electronics": "blocked journal title",
    "machines": "blocked journal title",
    "robotics": "blocked journal title",
    "aerospace": "blocked journal title",
    "ai": "blocked journal title",
    "algorithms": "blocked journal title",
    "information": "blocked journal title",
    "mathematics": "blocked journal title",
    "entropy": "blocked journal title",
    "vehicles": "blocked journal title",
    "journal of imaging": "blocked journal title",
    "big data and cognitive computing": "blocked journal title",
    "scientific reports": "blocked journal title",
    "ieee access": "blocked journal title",
    "heliyon": "blocked journal title",
    "plos one": "blocked journal title",
    "peerj computer science": "blocked journal title",
}

TIER_ALIASES: list[tuple[str, str, str]] = [
    ("tier1", "Science Robotics", "science robotics"),
    ("tier1", "IJRR", "international journal of robotics research"),
    ("tier1", "IJRR", "ijrr"),
    ("tier1", "T-RO", "ieee transactions on robotics"),
    ("tier1", "T-ASE", "ieee transactions on automation science and engineering"),
    ("tier1", "RA-L", "ieee robotics and automation letters"),
    ("tier1", "RSS", "robotics science and systems"),
    ("tier1", "RSS", "rss"),
    ("tier1", "ICRA", "icra"),
    ("tier1", "IROS", "iros"),
    ("tier1", "CoRL", "corl"),
    ("tier1", "CVPR", "cvpr"),
    ("tier1", "ICCV", "iccv"),
    ("tier1", "ECCV", "eccv"),
    ("tier1", "TPAMI", "transactions on pattern analysis and machine intelligence"),
    ("tier1", "TPAMI", "tpami"),
    ("tier1", "IJCV", "international journal of computer vision"),
    ("tier1", "TIP", "ieee transactions on image processing"),
    ("tier1", "TMM", "ieee transactions on multimedia"),
    ("tier1", "TCSVT", "transactions on circuits and systems for video technology"),
    ("tier1", "NeurIPS", "neurips"),
    ("tier1", "NeurIPS", "nips"),
    ("tier1", "ICML", "icml"),
    ("tier1", "ICLR", "iclr"),
    ("tier1", "AAAI", "aaai"),
    ("tier1", "IJCAI", "ijcai"),
    ("tier1", "AAMAS", "aamas"),
    ("tier1", "JMLR", "journal of machine learning research"),
    ("tier1", "JMLR", "jmlr"),
    ("tier2", "Journal of Field Robotics", "journal of field robotics"),
    ("tier2", "Autonomous Robots", "autonomous robots"),
    ("tier2", "Robotics and Autonomous Systems", "robotics and autonomous systems"),
    ("tier2", "IEEE Robotics & Automation Magazine", "robotics automation magazine"),
    ("tier2", "EAAI", "engineering applications of artificial intelligence"),
    ("tier2", "Pattern Recognition", "pattern recognition"),
    ("tier2", "CVIU", "computer vision and image understanding"),
    ("tier2", "WACV", "wacv"),
    ("tier2", "BMVC", "bmvc"),
    ("tier2", "ACCV", "accv"),
    ("tier2", "CASE", "case"),
    ("tier2", "TNNLS", "transactions on neural networks and learning systems"),
    ("tier2", "Neural Networks", "neural networks"),
    ("tier3", "T-ITS", "transactions on intelligent transportation systems"),
    ("tier3", "TGRS", "transactions on geoscience and remote sensing"),
    ("tier3", "ISPRS JPRS", "isprs journal of photogrammetry and remote sensing"),
    ("tier3", "Remote Sensing of Environment", "remote sensing of environment"),
    ("tier3", "Automatica", "automatica"),
    ("tier3", "TAC", "transactions on automatic control"),
    ("tier3", "Control Engineering Practice", "control engineering practice"),
]

PREPRINT_SOURCES = {"arxiv", "arxiv.org"}


def normalize(text: object) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", str(text or "").lower())).strip()


def record_values(record: dict) -> dict[str, str]:
    venue = record.get("venue") or record.get("journal") or record.get("booktitle") or record.get("container") or ""
    return {
        "venue": str(venue or ""),
        "publisher": str(record.get("publisher") or record.get("source_publisher") or ""),
        "doi": str(record.get("doi") or record.get("DOI") or ""),
        "source": str(record.get("source") or ""),
    }


def url_hosts(record: dict) -> list[str]:
    urls = []
    for key in ("url", "pdf_url", "landing_page_url", "oa_url"):
        value = record.get(key)
        if isinstance(value, str) and value:
            urls.append(value)
    hosts = []
    for url in urls:
        parsed = urlparse(url)
        host = parsed.netloc.lower() if parsed.netloc else url.lower()
        hosts.append(host)
        if parsed.path:
            hosts.append(f"{host}{parsed.path.lower()}")
    return hosts


def classify_target_venue(record: dict) -> tuple[str | None, str | None]:
    values = record_values(record)
    venue_norm = normalize(values["venue"])
    if not venue_norm:
        return None, None
    venue_tokens = set(venue_norm.split())
    for tier, canonical, alias in TIER_ALIASES:
        alias_norm = normalize(alias)
        if not alias_norm:
            continue
        if len(alias_norm) <= 5 and " " not in alias_norm:
            if alias_norm in venue_tokens:
                return tier, canonical
            continue
        if alias_norm in venue_norm:
            return tier, canonical
    return None, None


def is_preprint(record: dict) -> bool:
    values = record_values(record)
    source_norm = normalize(values["source"])
    venue_norm = normalize(values["venue"])
    if record.get("arxiv_id"):
        return True
    if any(src in source_norm for src in PREPRINT_SOURCES):
        return True
    return venue_norm in {"arxiv", "arxiv preprint"}


def rejection_reason(record: dict) -> str | None:
    values = record_values(record)
    publisher_norm = normalize(values["publisher"])
    venue_norm = normalize(values["venue"])
    doi = values["doi"].lower().removeprefix("https://doi.org/").strip()

    for prefix, reason in DOI_PREFIX_BLOCKS.items():
        if doi.startswith(prefix):
            return reason

    for needle, reason in PUBLISHER_BLOCKS.items():
        if normalize(needle) in publisher_norm:
            return reason

    for host_or_path in url_hosts(record):
        for domain, reason in DOMAIN_BLOCKS.items():
            if domain in host_or_path:
                return reason

    if venue_norm in JOURNAL_TITLE_BLOCKS:
        return JOURNAL_TITLE_BLOCKS[venue_norm]

    if venue_norm.startswith("frontiers in "):
        return "blocked journal family: Frontiers"

    return None


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
                record["_quality_filter_input"] = os.path.basename(path)
                records.append(record)
    return records


def save_jsonl(records: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            record = dict(record)
            record.pop("_quality_filter_input", None)
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_report(report: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def filter_records(records: list[dict], *, strict_target_venues: bool, allow_preprints: bool) -> tuple[list[dict], dict]:
    kept = []
    rejected = []
    tier_counts: dict[str, int] = {}
    reason_counts: dict[str, int] = {}

    for record in records:
        reason = rejection_reason(record)
        tier, canonical = classify_target_venue(record)
        preprint = is_preprint(record)

        if reason is None and strict_target_venues and tier is None and not (allow_preprints and preprint):
            reason = "not in target venue list"

        if reason:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
            rejected.append(
                {
                    "title": record.get("title", ""),
                    "venue": record.get("venue") or record.get("journal") or "",
                    "publisher": record.get("publisher", ""),
                    "doi": record.get("doi", ""),
                    "source": record.get("source", ""),
                    "input": record.get("_quality_filter_input", ""),
                    "reason": reason,
                }
            )
            continue

        tagged = dict(record)
        if tier:
            tagged["priority_tier"] = tier
            tagged["priority_venue"] = canonical
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        elif preprint:
            tagged["priority_tier"] = "preprint"
            tier_counts["preprint"] = tier_counts.get("preprint", 0) + 1
        else:
            tagged["priority_tier"] = "unclassified"
            tier_counts["unclassified"] = tier_counts.get("unclassified", 0) + 1
        kept.append(tagged)

    report = {
        "total": len(records),
        "kept": len(kept),
        "rejected": len(rejected),
        "tier_counts": dict(sorted(tier_counts.items())),
        "rejection_counts": dict(sorted(reason_counts.items())),
        "rejected_records": rejected,
    }
    return kept, report


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter publication JSONL records by venue quality policy")
    parser.add_argument("--input", "--inputs", nargs="+", required=True, help="Input JSONL file(s)")
    parser.add_argument("--output", "-o", required=True, help="Filtered output JSONL")
    parser.add_argument("--report", required=True, help="JSON report for rejected records")
    parser.add_argument("--strict-target-venues", action="store_true", help="Reject records outside target venues")
    parser.add_argument("--allow-preprints", action="store_true", help="Allow arXiv/preprints in strict mode")
    args = parser.parse_args()

    records = load_jsonl(args.input)
    kept, report = filter_records(
        records,
        strict_target_venues=args.strict_target_venues,
        allow_preprints=args.allow_preprints,
    )
    save_jsonl(kept, args.output)
    write_report(report, args.report)
    print(
        f"Quality filter: {report['total']} -> {report['kept']} kept, {report['rejected']} rejected -> {args.output}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
