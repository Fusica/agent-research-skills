---
name: literature-search
description: Search academic literature using Semantic Scholar, arXiv, and OpenAlex APIs. Returns structured JSONL with title, authors, year, venue, abstract, citations, and BibTeX. Use when the user needs to find papers, check related work, or build a bibliography.
argument-hint: [search-query]
---

# Literature Search

Search multiple academic databases to find relevant papers.

## Input

- `$ARGUMENTS` — The search query (natural language)

## Planning Context

Before broad literature search for an active paper project, read the Planning
with Files state and convergence policy:
`${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`.
Use the active plan to choose search scope and write durable findings back to
`findings.md` / `progress.md` when available.

## Scripts

### Semantic Scholar (primary — best for ML/AI, has BibTeX)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/search_semantic_scholar.py \
  --query "QUERY" --max-results 20 \
  --api-key "$(grep S2_API_Key $HOME/keys.md 2>/dev/null | cut -d: -f2 | tr -d ' ')" \
  -o results_s2.jsonl
```

Useful optional flag: `--year-range 2020-2026` only when the user explicitly asks for a time window.

### arXiv (latest preprints)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/search_arxiv.py \
  --query "QUERY" --max-results 10 -o results_arxiv.jsonl
```

### OpenAlex (broadest coverage, free, no API key)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/literature-search/scripts/search_openalex.py \
  --query "QUERY" --max-results 20 -o results_openalex.jsonl
```

### Merge & Deduplicate
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/paper_db.py merge \
  --inputs results_s2.jsonl results_arxiv.jsonl results_openalex.jsonl \
  --output merged_raw.jsonl
```

### Publication Policy (keep all sources)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/filter_publications.py \
  --input merged_raw.jsonl \
  --output merged.jsonl \
  --report publication_policy_report.json
```
This is a compatibility passthrough. It keeps all papers from all sources and removes stale source-ranking metadata.

### CrossRef (DOI-based lookup, broadest type coverage)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/literature-search/scripts/search_crossref.py \
  --query "QUERY" --rows 10 --output results_crossref.jsonl
```

Key flags: `--bibtex` (output .bib format), `--rows N`

### Google Scholar (manual/browser cross-check only)
Google Scholar does not provide a stable official public API. Do not use it as the default scripted backend. Use it only for browser/manual spot checks: exact-title lookup, author profile inspection, citation trail sanity checks, or cases where Semantic Scholar/OpenAlex/CrossRef disagree.

### Download arXiv Source (get .tex files)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/literature-search/scripts/download_arxiv_source.py \
  --title "Paper Title" --output-dir arxiv_papers/
```

Key flags: `--arxiv-id 1706.03762`, `--metadata`, `--max-results N`

### Generate BibTeX from results
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/bibtex_manager.py \
  --jsonl merged.jsonl --output references.bib
```

## Workflow

1. Expand the user's query into 2-4 complementary search queries
2. Run Semantic Scholar search (primary) with expanded queries
3. Run arXiv for very recent preprints (< 3 months)
4. Optionally run OpenAlex for broader coverage
5. Use Google Scholar only as a manual/browser cross-check when structured sources miss or disagree
6. Merge and deduplicate results to `merged_raw.jsonl`
7. Run `filter_publications.py` only if a workflow expects `merged.jsonl`; it does not exclude records
8. Rank by topical relevance to the user's query; use citations and recency only as descriptive metadata or tie-breakers
9. Present structured results table and mention that the publication policy kept all records
10. If a stable kernel or venue hypothesis exists, label each result as core evidence, bridge evidence, baseline candidate, or background

## Relevance-Only Source Policy

Use `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/references/publication-relevance-policy.md`.

Do not exclude, prioritize, or downgrade papers by venue, publisher, journal, DOI prefix, domain, or preprint status. Keep anything topically relevant.

## Output Format

Present results as a table + detailed entries with BibTeX keys. Always note preprint status.
End iterative search rounds with Current Stable Kernel, Open But Bounded Questions, Decision Log, Freeze Criteria, and Next Narrowing Step when the search is part of idea/novelty/planning work.

## Related Skills
- Downstream: [citation-management](../citation-management/), [literature-review](../literature-review/), [related-work-writing](../related-work-writing/)
- See also: [deep-research](../deep-research/), [novelty-assessment](../novelty-assessment/)
