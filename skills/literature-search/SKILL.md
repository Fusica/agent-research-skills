---
name: literature-search
description: Search academic literature using Semantic Scholar, arXiv, and OpenAlex APIs. Returns structured JSONL with title, authors, year, venue, abstract, citations, and BibTeX. Use when the user needs to find papers, check related work, or build a bibliography.
argument-hint: [search-query]
---

# Literature Search

Search multiple academic databases to find relevant papers.

## Input

- `$ARGUMENTS` — The search query (natural language)

## Scripts

### Semantic Scholar (primary — best for ML/AI, has BibTeX)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/search_semantic_scholar.py \
  --query "QUERY" --max-results 20 --year-range 2022-2026 \
  --api-key "$(grep S2_API_Key $HOME/keys.md 2>/dev/null | cut -d: -f2 | tr -d ' ')" \
  -o results_s2.jsonl
```

Key flags: `--peer-reviewed-only`, `--top-conferences`, `--min-citations N`, `--venue NeurIPS ICML`

### arXiv (latest preprints)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/search_arxiv.py \
  --query "QUERY" --max-results 10 -o results_arxiv.jsonl
```

### OpenAlex (broadest coverage, free, no API key)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/literature-search/scripts/search_openalex.py \
  --query "QUERY" --max-results 20 --year-range 2022-2026 \
  --min-citations 5 -o results_openalex.jsonl
```

### Merge & Deduplicate
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/paper_db.py merge \
  --inputs results_s2.jsonl results_arxiv.jsonl results_openalex.jsonl \
  --output merged_raw.jsonl
```

### Quality Filter (required for ML/robotics/CV/RL/embodied AI/LLM-VLM work)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/filter_publications.py \
  --input merged_raw.jsonl \
  --output merged.jsonl \
  --report quality_filter_report.json \
  --allow-preprints
```
Use `--strict-target-venues` only when the user explicitly asks for target-venue-only results. Otherwise, hard-block low-quality/predatory sources and use venue tiers as ranking signals so high-quality bridge work is not lost.

### CrossRef (DOI-based lookup, broadest type coverage)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/literature-search/scripts/search_crossref.py \
  --query "QUERY" --rows 10 --output results_crossref.jsonl
```

Key flags: `--bibtex` (output .bib format), `--rows N`

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
5. Merge and deduplicate results to `merged_raw.jsonl`
6. Run `filter_publications.py` before ranking or presenting results
7. Rank by: citations (0.25) + recency (0.25) + priority_tier/venue quality (0.3) + relevance (0.2)
8. Present structured results table and mention how many records were excluded by `quality_filter_report.json`
9. If a stable kernel or venue hypothesis exists, label each result as core evidence, bridge evidence, baseline candidate, or background

## Venue Quality Tiers

Use `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/references/venue-quality-policy.md`.

For the user's ML/robotics/CV/RL/embodied AI/LLM-VLM scope, Tier 1 includes Science Robotics, IJRR, T-RO, T-ASE, RA-L, RSS, ICRA, IROS, CoRL, CVPR, ICCV, ECCV, TPAMI, IJCV, TIP, TMM, TCSVT, NeurIPS, ICML, ICLR, AAAI, IJCAI, AAMAS, and JMLR.

Hard-block MDPI and other blacklist matches by publisher, DOI prefix, domain, or exact journal title before presenting results.
Do not treat the target venue list as a hard scope boundary unless requested.

## Output Format

Present results as a table + detailed entries with BibTeX keys. Always note preprint status.
End iterative search rounds with Current Stable Kernel, Open But Bounded Questions, Decision Log, Freeze Criteria, and Next Narrowing Step when the search is part of idea/novelty/planning work.

## Related Skills
- Downstream: [citation-management](../citation-management/), [literature-review](../literature-review/), [related-work-writing](../related-work-writing/)
- See also: [deep-research](../deep-research/), [novelty-assessment](../novelty-assessment/)
