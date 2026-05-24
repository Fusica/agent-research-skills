# Venue Writing Policy

Use this policy after the research has a stable kernel, paper route, venue
hypothesis, and evidence matrix from `paper-assembly/references/research-convergence-policy.md`.

## Inputs to Require

- `convergence_state`: current stable kernel, bounded questions, decision log,
  freeze criteria, and next narrowing step.
- `paper_route`: one primary route and at most one secondary route.
- `venue_hypothesis`: candidate venue cluster or selected target venue.
- `evidence_matrix`: claims mapped to experiments, metrics, figures, and tables.
- Planning with Files state when available: active `task_plan.md`, `findings.md`,
  and `progress.md`, resolved using
  `paper-assembly/references/planning-with-files-bridge.md`.

If any input is missing, write only a bounded plan and request or infer the
minimum missing state. Do not widen the paper scope during writing.

## Venue Profiles

- CVPR/ICCV/ECCV/TPAMI/TIP: emphasize visual method novelty, protocol-compatible
  baselines, dataset and metric fairness, ablations, qualitative evidence, and
  clear failure cases.
- T-RO/T-ASE/RA-L/ICRA/IROS/Science Robotics: emphasize robotics task relevance,
  assumptions, system integration, robustness, runtime, deployment constraints,
  and how perception/learning supports autonomy.
- NeurIPS/ICML/ICLR/AAAI: emphasize learning formulation, abstraction,
  generalization, controlled evidence, and why the method is not only an
  application-specific engineering change.
- TMM/TCSVT/EAAI: emphasize multimedia/video/AI engineering fit, efficiency,
  reproducible implementation, and application-specific evaluation.

## Claim-Evidence Rules

- Every strong claim in text must point to evidence in the matrix or be softened.
- Every figure/table must support a claim, resolve a reviewer risk, or explain
  the method/protocol.
- Do not add new citations, baselines, or experiments during writing unless they
  are needed for a bounded open question.
- If evidence supports only in-domain performance, do not write broad
  generalization, zero-shot, or deployment claims.

## Writing Lock

Once the selected venue profile and evidence matrix are coherent, stop adding
new angles. Refine wording, figures, tables, and responses around the current
stable kernel.

## Required Closure Block

End major writing, figure/table, self-review, revision, and rebuttal rounds with:

```text
Current Stable Kernel:
Venue/Writing Profile:
Evidence Coverage:
Open But Bounded Questions:
Decision Log:
Freeze Criteria:
Next Narrowing Step:
Planning Files Updated:
```
