# Experiment Design Stage Prompts

Extracted from AI-Scientist-v2 (agent_manager.py) and AI-Researcher (exp_analyser.py).

## 4-Stage Progressive Experiment Framework (AI-Scientist-v2)

### Stage 1: Initial Implementation
**Goal**: Get a working baseline on a simple dataset.

```
Stage 1 - Initial Implementation:
- Implement the core method on the simplest dataset
- Ensure training converges (check training curves)
- Establish baseline metrics
- Verify code runs without errors

Completion criteria:
- Training loss decreases
- Validation metrics are reasonable (not random)
- Code executes end-to-end without errors
```

### Stage 2: Baseline Tuning
**Goal**: Optimize hyperparameters and test on route-appropriate independent evaluation contexts.

```
Stage 2 - Baseline Tuning:
- Tune learning rate, batch size, and key hyperparameters
- Test on the independent evaluation contexts required by the paper route
- Compare against published baselines
- Use route-appropriate replication: seeds for stochastic ML training, trials/episodes for RL, scenes/environments/robots for robotics, or prompt runs for LLM/VLM systems

Completion criteria:
- Results competitive with or better than baselines
- Consistent across the chosen replication unit when meaningful for the task
- Training curves show stable convergence
```

### Stage 3: Creative Research
**Goal**: Novel improvements and comprehensive evaluation.

```
Stage 3 - Creative Research:
- Implement novel improvements to the method
- Expand only to decisive datasets, tasks, environments, robots, scenes, trajectories, domains, or user scenarios
- Compare against 3+ baselines
- Ablation of key design choices
- Generate publication-quality figures

Completion criteria:
- Clear improvement over baselines in the decisive evaluation contexts
- Ablation supports contribution claims
- Figures are informative and well-designed
```

### Stage 4: Ablation Studies
**Goal**: Systematic component analysis.

```
Stage 4 - Ablation Studies:
- Remove/modify each key component one at a time
- Measure impact on performance
- Sensitivity analysis for key hyperparameters
- Report uncertainty using the appropriate repeated measurements: mean/std over seeds, success-rate intervals over trials, bootstrap CIs, or descriptive evidence when comparable repetitions are unavailable

Completion criteria:
- Every claimed contribution verified by ablation
- Hyperparameter sensitivity is reasonable
- Results table is complete with all comparisons
```

After every stage, add `convergence_state` with:
`current_stable_kernel`, `open_but_bounded_questions`, `decision_log`,
`freeze_criteria`, and `next_narrowing_step`. Do not add experiments unless
they support a claim, resolve a fatal risk, or decide between venue profiles.

## VLM-Based Stage Completion Check (AI-Scientist-v2)

```
Examine the training curves and results:
1. Is the training loss decreasing?
2. Is validation performance improving?
3. Has the model converged or does it need more epochs?
4. Are there signs of overfitting?
5. Is the performance competitive with baselines?

Based on this analysis, determine if the current stage is complete
or if more experiments are needed.
```

## Best-Node Selection (AI-Scientist-v2)

```
Given the following experiment results and their training curves,
holistically select the best experiment considering:
1. Final test performance (primary metric)
2. Training stability (smooth loss curves)
3. Consistency across seeds
4. Generalization (train-test gap)

Experiment results:
{results_json}

Select the best experiment and justify your choice.
```

## Ablation Study Design (AI-Researcher)

```
Given the experimental results:
{results}

Design an ablation study to verify each component's contribution:
1. List all key components of the method
2. For each component, propose a variant where it is removed/replaced
3. Predict expected impact of each removal
4. Prioritize: test the most impactful ablations first
```

## Sensitivity Analysis (AI-Researcher)

```
Design a sensitivity analysis for these hyperparameters:
{hyperparameters}

For each hyperparameter:
1. Define a reasonable range to test
2. Specify the number of values to try
3. Identify which metrics to track
4. Note any interactions between hyperparameters
```
