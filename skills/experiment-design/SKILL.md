---
name: experiment-design
description: Design experiment plans with progressive stages — initial implementation, baseline tuning, creative research, and ablation studies. Plan baselines, datasets, hyperparameter sweeps, and evaluation metrics. Use when planning experiments for a research paper.
argument-hint: [idea-or-plan]
---

# Experiment Design

Design structured, progressive experiment plans for research papers.

## Input

- `$0` — Research idea, plan, or method description

## References

- 4-stage progressive experiment prompts: `${CODEX_HOME:-$HOME/.codex}/skills/experiment-design/references/stage-prompts.md`
- Research convergence policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`

## Scripts

### Generate experiment design
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/experiment-design/scripts/design_experiments.py --plan research_plan.json --output experiment_design.json
python ${CODEX_HOME:-$HOME/.codex}/skills/experiment-design/scripts/design_experiments.py --method "contrastive learning" --task classification --format markdown
```

Generates baselines, ablation matrix, hyperparameter grid, metric selection. Stdlib-only.

## 4-Stage Progressive Framework (from AI-Scientist-v2)

### Stage 1: Initial Implementation
- Focus on getting a basic working implementation
- Use a simple dataset
- Aim for basic functional correctness
- Completion: at least one working (non-buggy) implementation

### Stage 2: Baseline Tuning
- Tune hyperparameters (learning rate, epochs, batch size)
- Do NOT change model architecture
- Test on at least two independent evaluation contexts when the paper route requires it. Contexts may be datasets, tasks, environments, robots, scenes, trajectories, domains, or user scenarios.
- Completion: stable training curves, improvement over Stage 1

### Stage 3: Creative Research
- Explore novel improvements and insights
- Be creative and think outside the box
- Expand to the smallest set of decisive evaluation contexts needed for the venue hypothesis rather than a fixed dataset count.
- Completion: demonstrated novel improvement

### Stage 4: Ablation Studies
- Systematic component analysis
- Each ablation tests a different aspect
- Use the same decisive evaluation contexts as Stage 3 unless a specific ablation needs a narrower diagnostic context.
- Completion: all planned ablations done

## Venue-Aware Evidence Matrix

Before listing experiments, identify the current paper route and candidate venue cluster from the research plan. Then build an evidence matrix:

| Claim Type | Required Evidence |
|------------|-------------------|
| Algorithmic ML / robot learning | Controlled baselines, multi-seed or repeated runs where meaningful, learning-curve evidence, generalization tests |
| CV perception / benchmark method | Protocol-compatible baselines, dataset splits, standard metrics, ablations, qualitative results, fairness notes |
| Robotics systems / deployment | Task assumptions, robustness checks, latency/runtime, hardware or deployment constraints, failure modes, autonomy relevance |
| Embodied AI / LLM-VLM integration | Concrete robot capability, measurable behavior, model interface, grounding checks, ablation against non-foundation-model alternatives |
| Multimedia/video/AI engineering | Video/multimodal metrics, efficiency, reproducible pipeline, application-specific constraints |

Use the evidence matrix to stop experiment drift: add experiments only if they support a paper claim, resolve a fatal risk, or decide between venue profiles.

## Output Format

```json
{
  "stages": [
    {
      "name": "initial_implementation",
      "goals": ["Basic working baseline", "Simple dataset"],
      "max_iterations": 5,
      "completion_criteria": "Working implementation with non-zero accuracy"
    }
  ],
  "baselines": ["Method A", "Method B"],
  "datasets": ["Dataset1", "Dataset2", "Dataset3"],
  "metrics": ["accuracy", "F1", "inference_time"],
  "ablation_components": ["component_A", "component_B"],
  "venue_hypothesis": ["T-RO/T-ASE", "RA-L/ICRA/IROS"],
  "evidence_matrix": [
    {"claim": "...", "experiment": "...", "metric": "...", "target_table_or_figure": "..."}
  ],
  "convergence_state": {
    "current_stable_kernel": "...",
    "open_but_bounded_questions": ["..."],
    "decision_log": ["..."],
    "freeze_criteria": "...",
    "next_narrowing_step": "..."
  },
  "hyperparameter_grid": {
    "lr": [1e-4, 1e-3, 1e-2],
    "batch_size": [32, 64, 128]
  },
  "replication": {
    "unit": "seed | trial | episode | scene | environment | robot | prompt_run",
    "count": 3,
    "statistical_test": "paired_ttest | bootstrap_ci | none"
  }
}
```

## Rules

- Always start simple (Stage 1) before complex experiments
- Each stage builds on the best result from the previous stage
- Use route-aware replication evidence. Seeds are appropriate for stochastic ML training; trials, episodes, scenes, robots, environments, or prompt runs may be more appropriate for robotics, RL, and LLM/VLM systems.
- Document every experiment run in notes.txt
- Generate figures for training curves and comparisons
- Match experiments to the paper route instead of blindly expanding the grid
- Do not require every idea to satisfy every venue. Design the minimum decisive evidence for the current venue hypothesis.
- End each design round with the closure block from the research convergence policy.

## Related Skills
- Upstream: [research-planning](../research-planning/), [idea-generation](../idea-generation/)
- Downstream: [experiment-code](../experiment-code/), [data-analysis](../data-analysis/)
- See also: [paper-assembly](../paper-assembly/)
