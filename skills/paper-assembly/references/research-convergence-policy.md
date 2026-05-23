# Research Convergence Policy

Use this policy when a research skill must keep exploration open while still
converging toward a publishable ML/robotics paper.

## Separation of Concerns

- Hard filters apply only to source quality: blocked publishers, predatory
  venues, low-quality mega journals, and unreliable sources must not become
  novelty evidence, core related work, or citation support.
- Reputable preprints, arXiv papers, technical reports, and strong open-source
  artifacts may be used as lower-confidence novelty-risk signals when clearly
  labeled as non-peer-reviewed. Do not cite them as final authority unless the
  venue and task make that acceptable.
- Scope filters are soft priorities, not exclusions. The main umbrella is
  ML/robotics, including computer vision, robot learning, RL, embodied AI,
  UAV/autonomous systems, multimodal perception, LLM/VLM/foundation-model
  methods for robotics, and adjacent learning/control methods when they can
  support a measurable paper claim.
- Venue positioning becomes stricter over time. Early ideation may explore
  broadly; experiment design and writing must eventually choose a paper type
  and venue cluster.

## Progressive Convergence Ladder

1. Exploration: collect high-quality ideas, papers, methods, and analogies
   without prematurely excluding bridge areas such as LLM/VLM or embodied AI.
2. Stable kernel: identify the problem, target user/scenario, core technical
   hypothesis, expected contribution type, and the first plausible venue
   cluster.
3. Paper type selection: classify the work as one or two of:
   algorithmic ML, CV benchmark/method, robotics systems, robot learning/RL,
   embodied AI/foundation-model integration, or application/deployment paper.
4. Venue hypothesis: map the paper type to candidate venues and required taste:
   CVPR/ICCV/ECCV/TPAMI/TIP for visual methods and benchmark strength;
   T-RO/T-ASE/RA-L/ICRA/IROS/Science Robotics for robotics validity,
   system evidence, deployment, and task relevance; NeurIPS/ICML/ICLR/AAAI
   for learning formulation, abstraction, and strong generalization evidence;
   TMM/TCSVT/EAAI for multimedia/video/AI engineering fit.
5. Evidence matrix: every major claim must map to datasets, baselines,
   metrics, ablations, runtime/fairness checks, and expected figures/tables.
6. Writing lock: once evidence and venue fit are sufficient, stop widening the
   scope and write to the chosen venue profile.

## Required Closure Block

For iterative skills, end every substantive round with:

```text
Current Stable Kernel:
Open But Bounded Questions:
Decision Log:
Freeze Criteria:
Next Narrowing Step:
```

- Current Stable Kernel contains claims that should not be reopened without
  new evidence.
- Open But Bounded Questions lists only issues that can change the next
  concrete decision.
- Decision Log records what was added, removed, or frozen this round.
- Freeze Criteria explains when exploration stops.
- Next Narrowing Step names exactly one next decision or experiment.

## Anti-Drift Rules

- Do not introduce new minor objections after the freeze criteria are met
  unless they are fatal to novelty, feasibility, venue fit, or evidence.
- Do not treat low-quality or blocked venues as proof that an idea lacks
  novelty.
- Do not force every idea into UAV-only, CV-only, RL-only, or robotics-only
  scope. The scope should narrow because the paper type and evidence demand it.
- Prefer a stable, testable core over an ever-growing list of possible angles.
