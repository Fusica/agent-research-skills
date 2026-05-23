---
name: paper-compilation
description: Compile LaTeX papers to PDF with automatic error detection, chktex style checking, and citation/reference validation. Runs the full pdflatex + bibtex pipeline. Use when the user wants to compile a paper, fix compilation errors, or debug LaTeX.
argument-hint: [tex-file-path]
---

# Paper Compilation

Compile a LaTeX paper to PDF with error detection and correction.

## Input

- `$ARGUMENTS` — Path to the main `.tex` file

## Scripts

### Compile paper
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/paper-compilation/scripts/compile_paper.py paper/main.tex
python ${CODEX_HOME:-$HOME/.codex}/skills/paper-compilation/scripts/compile_paper.py paper/main.tex --check-style
python ${CODEX_HOME:-$HOME/.codex}/skills/paper-compilation/scripts/compile_paper.py paper/main.tex --output paper/output.pdf
```

Reports: compilation status, page count, warnings, citation/reference stats, style issues.

### Validate citations before compiling
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/citation-management/scripts/validate_citations.py \
  --tex paper/main.tex --bib paper/references.bib --check-figures --figures-dir paper/figures/
```

### Auto-fix LaTeX errors
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/paper-compilation/scripts/fix_latex_errors.py \
  --tex paper/main.tex --log compile.log --output paper/main_fixed.tex
```

Fixes: HTML tags in LaTeX, mismatched environments, missing figures. Key flags: `--dry-run`, `--auto-detect`

### Compile with auto-fix retry
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/paper-compilation/scripts/compile_paper.py paper/main.tex --auto-fix
```

Runs fix_latex_errors.py + recompile up to 3 rounds until compilation succeeds.

## Workflow

### Step 1: Pre-Compilation Validation
Run `validate_citations.py` to catch issues before compiling:
- Every `\cite{key}` has a matching `.bib` entry
- Every `\includegraphics{file}` exists
- No duplicate labels or sections
If a venue profile exists, confirm the compiled artifact is being checked against the intended template/page/anonymity expectations.
When available, also confirm the stable kernel, paper route, venue hypothesis, and evidence matrix are still represented by the compiled artifact.

### Step 2: Compile
Run `compile_paper.py` which executes: `pdflatex → bibtex → pdflatex → pdflatex`

### Step 3: Error Correction Loop (up to 5 rounds)
If compilation fails, read the error output and fix:
- `! Undefined control sequence` → Add missing package or fix typo
- `! Missing $ inserted` → Wrap math in `$...$`
- `! Missing } inserted` → Fix unmatched brace
- `Citation 'key' undefined` → Add to .bib or fix `\cite`
- `</end{figure}>` → Replace with `\end{figure}` (HTML syntax in LaTeX)

Apply minimal fixes. Do not remove packages unnecessarily. Recompile after each fix.

### Step 4: Post-Compilation Report
Check: page count vs venue limit, remaining warnings, chktex style issues.
Mention any compile-time issue that could affect evidence presentation, such as missing figures/tables, broken hyperlinks for traceability, or unresolved claim-support references.
End with a submission-readiness closure: stable kernel status, venue/template status, route and venue-hypothesis fit, evidence-matrix presentation status, bounded remaining issues, freeze criteria, and the next narrowing step.

## Troubleshooting

### pdflatex not found
```bash
# macOS
brew install --cask mactex-no-gui
# Ubuntu
sudo apt install texlive-full
```

### Alternative: latexmk (auto-handles multiple passes)
```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

## Related Skills
- Upstream: [latex-formatting](../latex-formatting/), [citation-management](../citation-management/), [figure-generation](../figure-generation/), [table-generation](../table-generation/)
- Downstream: [self-review](../self-review/)
- See also: [paper-assembly](../paper-assembly/)
