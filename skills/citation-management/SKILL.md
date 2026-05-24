---
name: citation-management
description: Manage BibTeX citations for LaTeX papers. Harvest missing citations from a draft using Semantic Scholar, validate cite keys against .bib files, deduplicate entries, and format bibliography. Use when working with references, BibTeX, or citations.
argument-hint: [tex-or-bib-file]
---

# Citation Management

Manage the full lifecycle of citations in a LaTeX paper.

## Input

- `$0` — Action: `harvest`, `validate`, `add`, `format`
- `$1` — Path to `.tex` or `.bib` file

## Planning Context

When citations support an active paper project, read
`${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`
and the Planning with Files bridge before adding or removing citation themes.
Log added citations, excluded low-quality sources, and validation results to the
active planning files when available.

## Scripts

### Validate citations (check all cite keys resolve)
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/citation-management/scripts/validate_citations.py \
  --tex paper/main.tex --bib paper/references.bib --check-figures --figures-dir paper/figures/
```

Reports: missing citations, unused bib entries, duplicate keys, duplicate sections, duplicate labels, undefined references, missing figures.

### Generate BibTeX from paper database
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/bibtex_manager.py \
  --jsonl paper_db.jsonl --output references.bib
```

### Search for a specific paper to add
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/search_semantic_scholar.py \
  --query "attention is all you need" --max-results 5 \
  --api-key "$(grep S2_API_Key $HOME/keys.md 2>/dev/null | cut -d: -f2 | tr -d ' ')"
```

Before adding any candidate from search output, apply the user venue quality filter:

```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/filter_publications.py \
  --input candidates_raw.jsonl \
  --output candidates_filtered.jsonl \
  --report quality_filter_report.json \
  --allow-preprints
```
Use `--strict-target-venues` only when the user asks for target-venue-only citation candidates. Otherwise, hard-block low-quality sources and rank by venue tier/relevance.

### Harvest missing citations automatically
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/citation-management/scripts/harvest_citations.py \
  --tex paper/main.tex --bib paper/references.bib --output candidates.bib --max-rounds 10
```

Scans .tex for uncited claims, searches Semantic Scholar, outputs candidate BibTeX entries.
Key flags: `--dry-run` (preview only), `--verbose`, `--api-key`

### Auto-fix missing citation placeholders
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/citation-management/scripts/validate_citations.py \
  --tex paper/main.tex --bib paper/references.bib --fix
```

Generates `references_fixed.bib` with placeholder entries for all missing citation keys.

## Action: `harvest` — Iterative Citation Harvesting

Based on AI-Scientist's 20-round citation harvesting loop. For each round:

1. Read the current `.tex` draft
2. Identify the most important missing citation
3. Search Semantic Scholar via script
4. Apply the venue quality filter to candidate papers
5. Select the most relevant paper from filtered results
6. Extract BibTeX and generate a clean key (`lastNameYearWord`)
7. Append to `.bib` (skip if key exists)
8. Insert `\cite{key}` at the appropriate location
9. Stop when no more gaps or 20 rounds reached

**Key rules:**
- DO NOT add a citation that already exists
- Only add citations found via API — never fabricate
- Never add MDPI, blocked low-quality venues, or predatory-publisher matches as citations
- Cite broadly — not just popular papers
- Do not copy verbatim from prior literature
- Tag each added citation by purpose when possible: core related work, bridge method, baseline, dataset/protocol, background, or reviewer-requested
- Do not add citations that widen the paper after writing lock unless they resolve a bounded open question or reviewer risk

## Action: `validate` — Pre-Compilation Check

Run `validate_citations.py` to catch all issues before compilation. Fix any reported problems.

## Action: `add` — Add Specific Paper

Search Semantic Scholar for the paper, extract BibTeX, clean the key, append to `.bib`.
If search returns multiple candidates, filter them first and add only candidates that pass the user venue quality policy.

BibTeX key format: `firstAuthorLastNameYearFirstContentWord` (e.g., `vaswani2017attention`)

## Action: `format` — Standardize .bib

- Sort entries alphabetically by key
- Ensure consistent indentation (2 spaces)
- Remove empty fields
- Protect proper nouns with `{Braces}` in titles
- Ensure required fields per entry type

## Related Skills
- Upstream: [literature-search](../literature-search/), [deep-research](../deep-research/)
- Downstream: [paper-compilation](../paper-compilation/), [latex-formatting](../latex-formatting/)
- See also: [related-work-writing](../related-work-writing/)
