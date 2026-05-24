# Research Convergence Policy

Use this policy when a research skill must keep exploration open while still
converging toward a publishable ML/robotics paper.

## Separation of Concerns

- Literature discovery is unrestricted. Do not exclude or prioritize papers by
  publisher, journal, venue, DOI prefix, domain, preprint status, or perceived
  source quality.
- Treat every found paper as available evidence. Later stages may decide that a
  paper is weak, irrelevant, redundant, or not worth citing, but search should
  not hide it.
- Scope narrowing is evidence-driven, not source-driven. The project narrows
  because the stable kernel, method, experiments, and claims become clearer.
- Venue positioning is a writing and packaging decision, not a literature
  search filter.

## Persistence and Planning Files

The convergence state is durable only when written to disk. A closure block in a
chat response or skill output is not enough. When the project uses Planning with
Files, read and update the active `task_plan.md`, `findings.md`, and
`progress.md` before and after substantive research work. Use
`paper-assembly/references/planning-with-files-bridge.md` for the exact plan
resolution and synchronization rules.

If no planning files exist, write the convergence state to a paper checkpoint
file or create Planning with Files state before running a long multi-step
pipeline.

## Progressive Convergence Ladder

1. Exploration: collect topic-relevant ideas, papers, methods, and analogies
   without prematurely excluding sources or adjacent areas.
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
- Planning Files Updated records which persistent files now contain this state,
  or explains why no persistent update was made.

## Anti-Drift Rules

- Do not introduce new minor objections after the freeze criteria are met
  unless they are fatal to novelty, feasibility, venue fit, or evidence.
- Do not dismiss novelty evidence because of where it appeared; assess overlap
  by content and relevance.
- Do not force every idea into UAV-only, CV-only, RL-only, or robotics-only
  scope. The scope should narrow because the paper type and evidence demand it.
- Prefer a stable, testable core over an ever-growing list of possible angles.
