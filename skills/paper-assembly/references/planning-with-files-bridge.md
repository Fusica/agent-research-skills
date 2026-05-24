# Planning with Files Bridge

Use this bridge whenever an Agent Research Skill runs inside a project that uses
Planning with Files.

## Persistence Boundary

The convergence block is not persistent by itself. Text such as `Current Stable
Kernel`, `paper_route`, `venue_hypothesis`, `evidence_matrix`, `Decision Log`,
`Freeze Criteria`, and `Next Narrowing Step` becomes durable only after it is
written to project files such as:

- `task_plan.md`
- `findings.md`
- `progress.md`
- `.planning/<active-plan>/task_plan.md`
- `.planning/<active-plan>/findings.md`
- `.planning/<active-plan>/progress.md`
- a paper checkpoint file such as `checkpoint.json`

Conversation context and final-answer text are volatile. Treat them as working
memory, not as the source of truth.

## Plan Resolution

Before making a research, experiment, writing, citation, figure, table, review,
or rebuttal decision, locate the active planning files in this order:

1. If `PLAN_ID` is set and `.planning/$PLAN_ID/task_plan.md` exists, use that.
2. If `.planning/.active_plan` points to a directory with `task_plan.md`, use it.
3. If `.planning/*/task_plan.md` exists, use the newest plan directory.
4. Otherwise, use root-level `task_plan.md`, `findings.md`, and `progress.md`
   when they exist.
5. If no planning files exist and the task is multi-step, create them or ask the
   user before starting broad execution.

Read `task_plan.md`, `findings.md`, and the recent tail of `progress.md` before
changing scope, selecting a route, adding experiments, adding citations, or
rewriting claims.

## Synchronization Rules

- Task plan controls scope. Do not add a new paper route, dataset, baseline,
  citation theme, figure, table, or rebuttal thread unless it fits the active
  plan or is logged as a deliberate plan change.
- Findings store durable research knowledge. Add important papers, repository
  discoveries, reviewer-risk findings, and evidence interpretations there.
- Progress stores execution history. Log completed phases, commands, generated
  artifacts, failed attempts, and verification results there.
- When producing or changing a convergence block, mirror the current stable
  kernel, bounded questions, decision log, freeze criteria, and next narrowing
  step into the active planning files.
- If Planning with Files hooks are active, still read the files explicitly before
  major decisions. Hooks are a reminder, not a substitute for state sync.

## Closure Requirement

Major Agent Research Skill outputs should end with both:

```text
Current Stable Kernel:
Open But Bounded Questions:
Decision Log:
Freeze Criteria:
Next Narrowing Step:
```

and a brief persistence note:

```text
Planning Files Updated:
- task_plan.md: ...
- findings.md: ...
- progress.md: ...
```

If files were not updated, state why.
