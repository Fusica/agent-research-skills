---
name: self-review
description: Automatically review an academic paper using the NeurIPS review form with three reviewer personas, ensemble scoring, and reflection refinement. Extracts text from PDF, runs structured review, and outputs actionable feedback. Use when the user wants to review a paper before submission or get feedback on a draft.
argument-hint: [pdf-or-tex-file]
---

# Self-Review

Review an academic paper using a structured review form with multiple reviewer personas.

## Input

- `$ARGUMENTS` — Path to PDF file or `.tex` file

## Scripts

### Extract text from PDF
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/self-review/scripts/extract_pdf_text.py paper.pdf --output paper_text.txt
python ${CODEX_HOME:-$HOME/.codex}/skills/self-review/scripts/extract_pdf_text.py paper.pdf --format markdown
```

Tries pymupdf4llm (best) → pymupdf → pypdf. Install: `pip install pymupdf4llm pymupdf pypdf`

### Parse PDF into structured sections
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/self-review/scripts/parse_pdf_sections.py \
  --pdf paper.pdf --output sections.json
```

Extracts title (via font size), section headings, and section text. Requires: `pip install pymupdf`
Key flags: `--format text`, `--verbose`

## Workflow

### Step 1: Load Paper
- If PDF: use `extract_pdf_text.py` to extract text
- If `.tex`: read the LaTeX source directly

### Step 2: Select Venue-Aware Reviewer Personas
Read the venue writing policy and choose personas that match the paper route. Use three independent reviews, mixing general and venue-specific personas:

1. **CV/benchmark reviewer**: Checks protocol fairness, baselines, metrics, ablations, qualitative evidence
2. **Robotics systems reviewer**: Checks task relevance, assumptions, runtime, deployment, robustness, autonomy linkage
3. **ML/AI reviewer**: Checks learning formulation, abstraction, generalization, and controlled evidence
4. **Journal reviewer**: Checks completeness, clarity, reproducibility, and whether claims are fully supported
5. **Open-minded bridge reviewer**: Checks LLM/VLM/foundation-model or embodied-AI connections without over-penalizing nontraditional scope

For each persona, generate a review following the NeurIPS review JSON format in `references/review-form.md`.

### Step 3: Reflection Refinement (up to 3 rounds per reviewer)
After each review, apply the reflection prompt: re-evaluate accuracy and soundness, refine if needed. Stop when "I am done".

### Step 4: Aggregate
- Combine all three reviews
- Average numerical scores (round to nearest integer)
- Synthesize a meta-review finding consensus
- Weight scores using AgentLaboratory weights: Overall (1.0), Contribution (0.4), Presentation (0.2), others (0.1 each)

### Step 5: Actionable Report

Output format:
```
## Review Summary
- **Overall Score**: X/10 (Weighted: Y/10)
- **Decision**: Accept / Reject
- **Confidence**: Z/5

## Strengths (consensus across reviewers)
1. ...
2. ...

## Weaknesses (consensus across reviewers)
1. ...
2. ...

## Questions for Authors
1. ...

## Specific Suggestions for Improvement
1. [Section X, Page Y]: ...
2. [Section Z, Page W]: ...

## Score Breakdown
| Dimension | R1 | R2 | R3 | Avg |
|-----------|----|----|-----|-----|
| Overall | ... | ... | ... | ... |
| Contribution | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

## Closure
Current Stable Kernel:
Venue/Writing Profile:
Evidence Coverage:
Open But Bounded Questions:
Decision Log:
Freeze Criteria:
Next Narrowing Step:
```

## References

- NeurIPS review form, scoring weights, personas, reflection prompts: `${CODEX_HOME:-$HOME/.codex}/skills/self-review/references/review-form.md`
- PDF text extraction: `${CODEX_HOME:-$HOME/.codex}/skills/self-review/scripts/extract_pdf_text.py`
- Venue writing policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-writing-section/references/venue-writing-policy.md`
- Research convergence policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`

## Missing Sections Check
You MUST verify that all required sections are present: Abstract, Introduction, Methods/Approach, Experiments/Results, Discussion/Conclusion. Reduce scores if any are missing.

## Evidence and Scope Check
Verify that each major claim maps to the evidence matrix and selected venue profile. Flag unsupported generalization, deployment, zero-shot, runtime, or broad autonomy claims. End the report with the closure block from the venue writing policy, including the remaining bounded questions.

## Related Skills
- Upstream: [paper-compilation](../paper-compilation/)
- Downstream: [paper-revision](../paper-revision/), [rebuttal-writing](../rebuttal-writing/)
- See also: [slide-generation](../slide-generation/)
