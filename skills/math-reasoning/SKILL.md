---
name: math-reasoning
description: Formal mathematical reasoning for research papers — derive equations, write proofs, formalize problem settings, select statistical tests, and generate LaTeX math notation. Use when the user needs mathematical derivations, theorem proofs, notation tables, or statistical analysis formalization.
argument-hint: [task-or-context]
---

# Mathematical Reasoning

Perform rigorous mathematical reasoning and produce publication-quality LaTeX output.

## Input

- `$0` — Task type: `derive`, `prove`, `formalize`, `stats`, `notation`, `verify`
- `$1` — Context: equation, theorem statement, problem description, or data description

## Tasks

### `derive` — Step-by-step equation derivation
Show every intermediate step. Justify each with the rule applied. Box final result with `\boxed{}`. Number important equations with `\label{eq:name}`.

### `prove` — Formal theorem proof
Use appropriate technique: direct, contradiction, induction, construction, or cases. See `references/proof-templates.md` for LaTeX templates.

### `formalize` — Problem setting formalization
Convert informal description into formal mathematical framework with: variable definitions, domain/range specifications, assumptions, objective function.

### `stats` — Statistical test selection
Use the decision tree in `references/notation-guide.md` to select appropriate tests. Report p-values, effect sizes, confidence intervals.

### `notation` — Generate notation table
Create a `\begin{table}` with all symbols used in the paper. Use standard ML notation from `references/notation-guide.md`.

### `verify` — Check mathematical correctness
Verify: dimensional consistency, boundary cases, gradient computations, notation consistency across sections.

## References

- Standard ML notation + statistical tests: `${CODEX_HOME:-$HOME/.codex}/skills/math-reasoning/references/notation-guide.md`
- Proof templates and theorem environments: `${CODEX_HOME:-$HOME/.codex}/skills/math-reasoning/references/proof-templates.md`
- Venue writing policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-writing-section/references/venue-writing-policy.md`
- Research convergence policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`

## Rules

- Define ALL symbols before first use: "Let $\mathcal{X}$ denote..."
- Use consistent notation throughout the paper
- Number equations that are referenced later
- Use `\tag{reason}` for key derivation steps
- State assumptions explicitly
- Cite lemmas and prior results used in proofs
- When available, check the stable kernel, paper route, venue hypothesis, and evidence matrix before choosing notation or claim strength
- Match formalism to the paper route: CV/pose notation, robotics state/action/system assumptions, RL objectives, embodied AI interfaces, or LLM/VLM grounding interfaces as appropriate
- Do not overstate theory. If the math is a rationale or consistency argument rather than a theorem, label it as such and keep claims within the evidence matrix and venue hypothesis
- End major formalization rounds with the venue-writing closure block when the math affects writing or venue positioning

## Related Skills
- Upstream: [research-planning](../research-planning/)
- Downstream: [algorithm-design](../algorithm-design/), [paper-writing-section](../paper-writing-section/)
- See also: [symbolic-equation](../symbolic-equation/), [data-analysis](../data-analysis/)
