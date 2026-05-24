#!/usr/bin/env python3
"""Search Semantic Scholar Graph API and output JSONL paper metadata.

Self-contained: uses only stdlib (urllib, json).

Usage:
    python search_semantic_scholar.py --query "long horizon reasoning" --max-results 100
    python search_semantic_scholar.py --query "protein language model" --year-range 2020-2026
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request

S2_API = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,authors,abstract,year,venue,citationCount,externalIds,url,referenceCount,publicationDate"
SEARCH_LIMIT = 100  # S2 max per request


def normalize_venue(venue: str) -> str:
    """Return a whitespace-normalized venue string without ranking or filtering."""
    return " ".join((venue or "").split())


def s2_request(url: str, api_key: str | None = None) -> dict:
    """Make a request to the Semantic Scholar API with retry logic."""
    headers = {"User-Agent": "deep-research/1.0"}
    if api_key:
        headers["x-api-key"] = api_key

    req = urllib.request.Request(url, headers=headers)

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 2 ** (attempt + 1)
                print(f"Rate limited, waiting {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        except Exception:
            if attempt < 2:
                time.sleep(1)
                continue
            raise
    return {}


def parse_paper(data: dict) -> dict | None:
    """Parse an S2 paper response into our standard record format."""
    if not data or not data.get("title"):
        return None

    authors = []
    for a in data.get("authors", []) or []:
        name = a.get("name", "")
        if name:
            authors.append(name)

    external_ids = data.get("externalIds", {}) or {}
    arxiv_id = external_ids.get("ArXiv", "")
    doi = external_ids.get("DOI", "")

    pdf_url = ""
    if arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

    abstract = data.get("abstract", "") or ""

    venue = data.get("venue", "") or ""

    return {
        "paperId": data.get("paperId", ""),
        "doi": doi,
        "arxiv_id": arxiv_id,
        "title": data["title"],
        "authors": authors,
        "abstract": " ".join(abstract.split()),
        "year": data.get("year"),
        "venue": venue,
        "venue_normalized": normalize_venue(venue),
        "peer_reviewed": None,
        "citationCount": data.get("citationCount", 0) or 0,
        "referenceCount": data.get("referenceCount", 0) or 0,
        "url": data.get("url", ""),
        "publicationDate": data.get("publicationDate", ""),
        "pdf_url": pdf_url,
        "source": "semantic_scholar",
    }


def search_papers(
    query: str,
    max_results: int = 100,
    year_range: str | None = None,
    api_key: str | None = None,
) -> list[dict]:
    """Search for papers and return deduplicated results without source filtering."""
    all_papers = []
    seen_ids = set()

    offset = 0
    while len(all_papers) < max_results:
        limit = min(SEARCH_LIMIT, max_results - len(all_papers))
        params = {
            "query": query,
            "offset": offset,
            "limit": limit,
            "fields": FIELDS,
        }
        if year_range:
            params["year"] = year_range

        url = f"{S2_API}/paper/search?{urllib.parse.urlencode(params)}"

        try:
            resp = s2_request(url, api_key)
        except Exception as e:
            print(f"Warning: search failed at offset {offset}: {e}", file=sys.stderr)
            break

        papers = resp.get("data", [])
        if not papers:
            break

        for item in papers:
            if len(all_papers) >= max_results:
                break

            paper = parse_paper(item)
            if not paper:
                continue

            # Dedup by paperId
            pid = paper["paperId"]
            if pid in seen_ids:
                continue
            seen_ids.add(pid)

            all_papers.append(paper)

        total = resp.get("total", 0)
        offset += limit
        if offset >= total:
            break

        # Rate limit: ~10 requests per second for public API
        time.sleep(0.5)

    return all_papers


def get_paper_details(paper_id: str, api_key: str | None = None) -> dict | None:
    """Get detailed info for a single paper by S2 paperId or arxiv:<id>."""
    url = f"{S2_API}/paper/{urllib.parse.quote(paper_id, safe='')}?fields={FIELDS}"
    try:
        data = s2_request(url, api_key)
        return parse_paper(data)
    except Exception as e:
        print(f"Warning: failed to fetch {paper_id}: {e}", file=sys.stderr)
        return None


def get_citations(paper_id: str, max_results: int = 50, api_key: str | None = None) -> list[dict]:
    """Get papers that cite the given paper."""
    url = f"{S2_API}/paper/{urllib.parse.quote(paper_id, safe='')}/citations?fields={FIELDS}&limit={min(max_results, 1000)}"
    try:
        resp = s2_request(url, api_key)
        results = []
        for item in resp.get("data", []):
            citing = item.get("citingPaper", {})
            paper = parse_paper(citing)
            if paper:
                results.append(paper)
        return results[:max_results]
    except Exception as e:
        print(f"Warning: failed to fetch citations for {paper_id}: {e}", file=sys.stderr)
        return []


def get_references(paper_id: str, max_results: int = 50, api_key: str | None = None) -> list[dict]:
    """Get papers referenced by the given paper."""
    url = f"{S2_API}/paper/{urllib.parse.quote(paper_id, safe='')}/references?fields={FIELDS}&limit={min(max_results, 1000)}"
    try:
        resp = s2_request(url, api_key)
        results = []
        for item in resp.get("data", []):
            cited = item.get("citedPaper", {})
            paper = parse_paper(cited)
            if paper:
                results.append(paper)
        return results[:max_results]
    except Exception as e:
        print(f"Warning: failed to fetch references for {paper_id}: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(description="Search Semantic Scholar and output JSONL")
    parser.add_argument("--query", required=True, help="Search keywords")
    parser.add_argument("--max-results", type=int, default=100, help="Max papers to return")
    parser.add_argument("--year-range", help="Year range filter (e.g. 2020-2026)")
    parser.add_argument("--api-key", help="S2 API key (optional, increases rate limits)")
    parser.add_argument("--citations-of", help="Get papers citing this paper ID")
    parser.add_argument("--references-of", help="Get papers referenced by this paper ID")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    if args.citations_of:
        papers = get_citations(args.citations_of, args.max_results, args.api_key)
    elif args.references_of:
        papers = get_references(args.references_of, args.max_results, args.api_key)
    else:
        papers = search_papers(
            query=args.query,
            max_results=args.max_results,
            year_range=args.year_range,
            api_key=args.api_key,
        )

    out = open(args.output, "w") if args.output else sys.stdout
    try:
        for paper in papers:
            out.write(json.dumps(paper, ensure_ascii=False) + "\n")
    finally:
        if args.output:
            out.close()

    print(f"Found {len(papers)} papers", file=sys.stderr)


if __name__ == "__main__":
    main()
