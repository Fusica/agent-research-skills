---
name: table-generation
description: Generate publication-quality LaTeX tables from experimental results. Convert JSON/CSV data to booktabs-styled tables with bold best results, multi-row layouts, and proper captions. Use when creating result tables, comparison tables, or ablation tables for papers.
argument-hint: [data-source]
---

# Table Generation

Convert experimental results into publication-ready LaTeX tables.

## Input

- `$0` — Table type: `comparison`, `ablation`, `descriptive`, `custom`
- `$1` — Data source: JSON file, CSV file, or inline data

## Scripts

### Generate LaTeX table from JSON/CSV
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/table-generation/scripts/results_to_table.py \
  --input results.json --type comparison \
  --bold-best max --caption "Performance comparison" \
  --label tab:main_results
```

Supports: `comparison`, `ablation`, `descriptive`, `multi-dataset` table types.
Additional flags: `--type multi-dataset` for methods x datasets x metrics layout, `--significance` for p-value stars, `--underline-second` for second-best results.

## References

- LaTeX table templates and examples: `${CODEX_HOME:-$HOME/.codex}/skills/table-generation/references/table-templates.md`
- Venue writing policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-writing-section/references/venue-writing-policy.md`
- Research convergence policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`

## Table Types

### `comparison` — Main results table
- Rows = methods (baselines + ours), Columns = metrics/datasets
- Bold the best result in each column
- Include mean +/- std when available
- Use `\multirow` for method categories (Supervised, Self-supervised, etc.)

### `ablation` — Ablation study table
- Rows = variants (full model, minus component A, minus component B, ...)
- Columns = metrics
- Bold the full model result
- Use checkmarks for component presence

### `descriptive` — Dataset/statistics table
- Dataset characteristics, hyperparameters, or summary statistics
- Clean formatting with proper units

### `custom` — Free-form table
- User specifies layout and content

## Venue-Aware Table Selection

Use the evidence matrix to decide which tables are necessary:
- CV/visual method papers: main benchmark, ablation, protocol/fairness notes, runtime/efficiency if claimed
- Robotics/system papers: main task success, robustness/deployment, runtime/hardware, ablation, failure cases
- ML/AI papers: controlled comparison, generalization, ablation, sensitivity, compute/efficiency
- LLM/VLM/embodied papers: grounding or task-success table, model-interface ablation, prompt/model variant comparison, failure taxonomy

## Required Packages
```latex
\usepackage{booktabs}    % \toprule, \midrule, \bottomrule
\usepackage{multirow}    % \multirow
\usepackage{multicol}    % multi-column layouts
\usepackage{threeparttable}  % table notes
```

## Output Format

Always generate tables with:
1. `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`)
2. `\caption{}` and `\label{tab:...}`
3. Bold best results using `\textbf{}`
4. Table notes via `threeparttable` when needed
5. Proper alignment (`l` for text, `c` or `r` for numbers)

## Rules

- Only include numbers from actual experimental logs — never hallucinate results
- All numbers must match the data source exactly
- Use `$\pm$` for standard deviations
- Use `\underline{}` for second-best results when appropriate
- Keep tables compact — avoid unnecessary columns
- Use `table*` for wide tables spanning two columns
- Add glossary/notes for abbreviated column headers
- Every table must support a claim in the evidence matrix or answer a reviewer/venue risk
- Include hardware, detector, dataset split, prompt/model, or protocol notes when needed for fairness
- Do not add columns merely because data exists; keep the table aligned with the selected venue profile
- End major table-generation rounds with the closure block from the venue writing policy

## Related Skills
- Upstream: [data-analysis](../data-analysis/), [experiment-code](../experiment-code/)
- Downstream: [paper-writing-section](../paper-writing-section/), [paper-compilation](../paper-compilation/)
- See also: [figure-generation](../figure-generation/)
