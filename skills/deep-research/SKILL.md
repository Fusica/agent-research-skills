---
name: deep-research
description: Conduct systematic academic literature reviews in 6 phases, producing structured notes, a curated paper database, and a synthesized final report. Output is organized by phase for clarity.
argument-hint: [topic]
---

# Deep Research Skill

## Trigger

Activate this skill when the user wants to:
- "Research a topic", "literature review", "find papers about", "survey papers on"
- "Deep dive into [topic]", "what's the state of the art in [topic]"
- Uses `/research <topic>` slash command

## Overview

This skill conducts systematic academic literature reviews in 6 phases, producing structured notes, a curated paper database, and a synthesized final report. Output is organized **by phase** for clarity.

**Installation**: `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/` — scripts, references, and this skill definition.
**Output**: `././deep-research-output/{slug}/` relative to the current working directory.

## CRITICAL: Strict Sequential Phase Execution

**You MUST execute all 6 phases in strict order: 1 → 2 → 3 → 4 → 5 → 6. NEVER skip any phase.**

This is the single most important rule of this skill. Violations include:
- ❌ Jumping from Phase 2 to Phase 5/6 (skipping Deep Dive and Code)
- ❌ Writing synthesis or report before completing Phase 3 deep reading
- ❌ Producing a final report based only on abstracts/titles from search results
- ❌ Combining or merging phases (e.g., doing "Phase 3-5 together")

### Phase Gate Protocol

Before starting Phase N+1, you MUST verify that Phase N's **required output files** exist on disk. If they don't exist, you have NOT completed that phase.

| Phase | Gate: Required Output Files |
|-------|---------------------------|
| 1 → 2 | `phase1_frontier/frontier.md` exists AND contains ≥10 papers |
| 2 → 3 | `phase2_survey/survey.md` exists AND `paper_db.jsonl` has 35-80 papers |
| 3 → 4 | `phase3_deep_dive/selection.md` AND `phase3_deep_dive/deep_dive.md` exist AND deep_dive.md contains detailed notes for ≥8 papers |
| 4 → 5 | `phase4_code/code_repos.md` exists AND contains ≥3 repositories |
| 5 → 6 | `phase5_synthesis/synthesis.md` AND `phase5_synthesis/gaps.md` exist |

**After completing each phase, print a phase completion checkpoint:**
```
✅ Phase N complete. Output: [list files written]. Proceeding to Phase N+1.
```

### Why Every Phase Matters

- **Phase 3 (Deep Dive)** is where you actually READ papers — without it, your synthesis is superficial and based only on abstracts
- **Phase 4 (Code & Tools)** grounds the research in practical implementations — without it, you miss the open-source ecosystem
- **Phase 5 (Synthesis)** requires deep knowledge from Phase 3 — you cannot synthesize papers you haven't read
- **Phase 6 (Report)** assembles content from ALL prior phases — it should cite specific findings from Phase 3 notes

## Publication Relevance Policy

Keep literature discovery unrestricted. Do not exclude or prioritize papers by
venue, publisher, journal, DOI prefix, domain, preprint status, or perceived
source quality. Include any paper that is relevant to the user's topic.

Use `filter_publications.py` only as a compatibility passthrough for older
workflow steps that expect this command:

```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/filter_publications.py \
  --input merged_raw.jsonl \
  --output paper_db.jsonl \
  --report publication_policy_report.json
```

See `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/references/publication-relevance-policy.md` for the current keep-all relevance policy.
When deep research is part of a paper pipeline, also load `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md` and end Phase 5/6 with the convergence closure block.

## Search Tools

### 1. paper_finder (optional external tool — conference papers only)
**Location**: Not bundled. Use only if the current machine has a working `paper_finder.py` and the user provides its path.

Searches ai-paper-finder.info (HuggingFace Space) for published conference papers. Supports filtering by conference + year. Outputs JSONL with BibTeX.

```bash
python /path/to/paper_finder.py --mode scrape --config <config.yaml>
python /path/to/paper_finder.py --mode download --jsonl <results.jsonl>
python /path/to/paper_finder.py --list-venues
```

Config example:
```yaml
searches:
  - query: "long horizon reasoning agent"
    num_results: 100
    venues:
      neurips: [2024, 2025]
      iclr: [2024, 2025, 2026]
      icml: [2024, 2025]
output:
  root: ./deep-research-output/{slug}/phase1_frontier/search_results
  overwrite: true
```

### 2. search_semantic_scholar.py (supplementary — citation data + broader coverage)
**Location**: `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/search_semantic_scholar.py`
Use broad topic queries and keep all source types. API key: `$HOME/keys.md` (field `S2_API_Key`)

### 3. search_arxiv.py (supplementary — latest preprints)
**Location**: `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/search_arxiv.py`
For searching recent papers not yet published at conferences. Mark citations with `(preprint)`.

### Other Scripts
| Script | Location | Key Flags |
|--------|----------|-----------|
| `download_papers.py` | `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/` | `--jsonl`, `--output-dir`, `--max-downloads`, `--sort-by-citations` |
| `extract_pdf.py` | `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/` | `--pdf`, `--pdf-dir`, `--output-dir`, `--sections-only` |
| `paper_db.py` | `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/` | subcommands: `merge`, `search`, `filter`, `tag`, `stats`, `add`, `export` |
| `filter_publications.py` | `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/` | `--input`, `--output`, `--report` |
| `bibtex_manager.py` | `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/` | `--jsonl`, `--output`, `--keys-only` |
| `compile_report.py` | `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/` | `--topic-dir` |

### URL/Browser Mode (no Bash)
1. **Paper discovery**: use web search or direct API URLs for Semantic Scholar/arXiv/OpenAlex
2. **Paper reading**: use ar5iv HTML, downloaded PDFs, or the available local PDF reader
3. **Writing**: save JSONL, notes, and report files in the active workspace

## 6-Phase Workflow

### Phase 1: Frontier
Search broadly for topic-relevant papers, preprints, surveys, and adjacent work.
1. Write `phase1_frontier/paper_finder_config.yaml` with broad query variants
2. Run paper_finder scrape when it is useful for the topic
3. Search the web for relevant paper lists and project pages
4. Identify trending directions, key breakthroughs, and direct overlaps
→ Output: `phase1_frontier/frontier.md`, `phase1_frontier/search_results/`

### Phase 2: Survey
Build a comprehensive landscape with broader time range. Target **35-80 topic-relevant papers** after relevance selection.
1. Write `phase2_survey/paper_finder_config.yaml` covering broad topic variants
2. Run paper_finder + Semantic Scholar + arXiv
3. Merge all results to `merged_raw.jsonl`: `python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/paper_db.py merge`
4. Run the publication passthrough to create `paper_db.jsonl`: `python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/filter_publications.py --input merged_raw.jsonl --output paper_db.jsonl --report publication_policy_report.json`.
5. Filter to 35-80 most relevant if needed: `python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/paper_db.py filter --min-score 0.80 --max-papers 70`
6. Cluster by theme, write survey notes
→ Output: `phase2_survey/survey.md`, `phase2_survey/search_results/`, `paper_db.jsonl`

### Phase 3: Deep Dive ⚠️ DO NOT SKIP

**This phase is MANDATORY.** You must actually READ 8-15 full papers, not just their abstracts.

1. Select 8-15 papers from paper_db.jsonl with rationale → write `phase3_deep_dive/selection.md`
2. Download PDFs: `python download_papers.py --jsonl paper_db.jsonl --output-dir phase3_deep_dive/papers/ --sort-by-citations --max-downloads 15`
3. For EACH selected paper, read the full text (PDF via the local PDF reader or HTML via ar5iv/browser fetch)
4. Write detailed structured notes per paper (see note-format.md template): problem, contributions, methodology, experiments, limitations, connections
5. Write ALL notes → `phase3_deep_dive/deep_dive.md`

**Phase 3 Gate**: `deep_dive.md` must contain detailed notes for ≥8 papers, each with methodology and experiment sections filled in. Abstract-only summaries do NOT count.

→ Output: `phase3_deep_dive/selection.md`, `phase3_deep_dive/deep_dive.md`, `phase3_deep_dive/papers/`

### Phase 4: Code & Tools ⚠️ DO NOT SKIP

**This phase is MANDATORY.** You must survey the open-source ecosystem.

1. Extract GitHub URLs from papers read in Phase 3
2. Search the web for implementations: "site:github.com {method name}", "site:paperswithcode.com {topic}"
3. For each repo found: record URL, stars, language, last updated, documentation quality
4. Search for related benchmarks and datasets
5. Write → `phase4_code/code_repos.md` (must contain ≥3 repositories)

**Phase 4 Gate**: `code_repos.md` must exist and contain at least 3 repositories with metadata.

→ Output: `phase4_code/code_repos.md`

### Phase 5: Synthesis (REQUIRES Phase 3 + 4 complete)
Cross-paper analysis. **Weight peer-reviewed findings higher**.
This phase MUST build on the detailed notes from Phase 3 and the code landscape from Phase 4.
Taxonomy, comparative tables, gap analysis.

**Before starting**: Verify `phase3_deep_dive/deep_dive.md` and `phase4_code/code_repos.md` exist. If not, go back and complete those phases first.

→ Output: `phase5_synthesis/synthesis.md`, `phase5_synthesis/gaps.md`

### Phase 6: Compilation (REQUIRES Phase 1-5 complete)
Assemble final report from ALL prior phase outputs. Mark preprint citations with `(preprint)` suffix.

**Before starting**: Verify ALL phase outputs exist:
- `phase1_frontier/frontier.md`
- `phase2_survey/survey.md`
- `phase3_deep_dive/deep_dive.md`
- `phase4_code/code_repos.md`
- `phase5_synthesis/synthesis.md` + `gaps.md`

If ANY are missing, go back and complete the missing phase(s) first.

→ Output: `phase6_report/report.md`, `phase6_report/references.bib`

## Output Directory

```
output/{topic-slug}/
├── paper_db.jsonl                    # Master database (accumulated)
├── phase1_frontier/
│   ├── paper_finder_config.yaml
│   ├── search_results/
│   └── frontier.md
├── phase2_survey/
│   ├── paper_finder_config.yaml
│   ├── search_results/
│   └── survey.md
├── phase3_deep_dive/
│   ├── papers/
│   ├── selection.md
│   └── deep_dive.md
├── phase4_code/
│   └── code_repos.md
├── phase5_synthesis/
│   ├── synthesis.md
│   └── gaps.md
└── phase6_report/
    ├── report.md
    └── references.bib
```

## Key Conventions

- **Paper IDs**: Use `arxiv_id` when available, otherwise Semantic Scholar `paperId`
- **Citations**: `[@key]` format, key = firstAuthorYearWord (e.g., `[@vaswani2017attention]`)
- **JSONL schema**: title, authors, abstract, year, venue, venue_normalized, peer_reviewed, citationCount, paperId, arxiv_id, pdf_url, tags, source
- **Source marking**: Note source type when useful, but do not remove papers based on source type
- **Incremental saves**: Each phase writes to disk immediately
- **Paper count**: Target 35-80 papers in final paper_db.jsonl (use `paper_db.py filter`)

## References

- `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/references/workflow-phases.md` — Detailed 6-phase methodology
- `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/references/note-format.md` — Note templates, BibTeX format, report structure
- `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/references/api-reference.md` — arXiv, Semantic Scholar, ar5iv API guide
- `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/references/publication-relevance-policy.md` — unrestricted relevance-only publication policy

## Related Skills
- Downstream: [literature-search](../literature-search/), [literature-review](../literature-review/), [citation-management](../citation-management/)
- See also: [novelty-assessment](../novelty-assessment/), [survey-generation](../survey-generation/)
