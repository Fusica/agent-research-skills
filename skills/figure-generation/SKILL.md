---
name: figure-generation
description: Generate publication-quality scientific figures using matplotlib/seaborn with a three-phase pipeline (query expansion, code generation with execution, VLM visual feedback). Handles bar charts, line plots, heatmaps, training curves, ablation plots, and more. Use when the user needs figures, plots, or visualizations for a paper.
argument-hint: [figure-description]
---

# Scientific Figure Generation

Generate publication-quality figures for research papers.

## Input

- `$0` — Description of the desired figure
- `$1` — (Optional) Path to data file (CSV, JSON, NPY, PKL) or results directory

## Scripts

### Generate figure template
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/figure-generation/scripts/figure_template.py --type bar --output figure_script.py --name comparison
python ${CODEX_HOME:-$HOME/.codex}/skills/figure-generation/scripts/figure_template.py --list-types
```

Available types: `bar`, `training-curve`, `heatmap`, `ablation`, `line`, `scatter`, `radar`, `violin`, `tsne`, `attention`

## Three-Phase Pipeline (from MatPlotAgent)

### Phase 1: Query Expansion
Expand the user's figure description into step-by-step coding specifications using the prompts in `references/figure-prompts.md`. Determine: figure type, data mapping (x/y/color/hue), style requirements, paper conventions.

### Phase 2: Code Generation with Execution Loop (up to 4 retries)
1. Generate a self-contained Python script using the template from `scripts/figure_template.py` as a starting point
2. Write script to a temp file and execute: `python figure_script.py`
3. If error: capture traceback, feed back, regenerate (see ERROR_PROMPT in references)
4. If no `.png` produced: add explicit save instruction, retry
5. On success: report the generated figure path

### Phase 3: Visual Refinement
Read the generated PNG file and visually inspect using the VLM feedback prompts from `references/figure-prompts.md`:
- Does the figure type match the request?
- Are labels, titles, and legends correct?
- Is the color scheme appropriate and consistent?
- Are axis scales sensible? Is text readable at publication size?

If improvements needed: generate corrective instructions and re-execute.

## References

- All MatPlotAgent prompts: `${CODEX_HOME:-$HOME/.codex}/skills/figure-generation/references/figure-prompts.md`
- Figure templates: `${CODEX_HOME:-$HOME/.codex}/skills/figure-generation/scripts/figure_template.py`
- Venue writing policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-writing-section/references/venue-writing-policy.md`
- Research convergence policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`

## Venue-Aware Figure Selection

Choose figures from the evidence matrix:
- Method/pipeline figure: show the stable kernel and paper route, not every implementation detail
- Quantitative plot: use when trends, robustness, sensitivity, or runtime tradeoffs matter more than raw table values
- Qualitative CV/robotics figure: show real inputs, outputs, failure modes, and protocol-relevant conditions
- LLM/VLM/embodied figure: show grounding, model interface, action/perception loop, or task outcome
- Failure-case panel: include when it bounds claims or addresses reviewer risk

## Output

Both PNG (preview, 300 DPI) and PDF (vector, for paper) formats. Plus the LaTeX include code:

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=\linewidth]{figures/figure_name.pdf}
    \caption{Description. Best viewed in color.}
    \label{fig:figure_name}
\end{figure}
```

## Quality Requirements
- DPI ≥ 300, or vector PDF
- Colorblind-friendly palette (no red-green only)
- All text ≥ 8pt at print size
- Consistent styling across all paper figures
- No matplotlib default title — use LaTeX caption
- Every figure must support a claim, clarify the method/protocol, or address a venue/reviewer risk
- Captions should state what the figure proves and its boundary conditions
- End major figure-generation rounds with the closure block from the venue writing policy

## Related Skills
- Upstream: [data-analysis](../data-analysis/), [experiment-code](../experiment-code/)
- Downstream: [paper-writing-section](../paper-writing-section/), [paper-compilation](../paper-compilation/), [slide-generation](../slide-generation/)
- See also: [table-generation](../table-generation/)
