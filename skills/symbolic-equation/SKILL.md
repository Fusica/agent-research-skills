---
name: symbolic-equation
description: Discover scientific equations from data using LLM-guided evolutionary search (LLM-SR). Multi-island algorithm with softmax-based cluster sampling, island reset, and LLM-proposed equation mutations. Use for symbolic regression and equation discovery.
argument-hint: [data-and-variables]
---

# Symbolic Equation Discovery

Discover interpretable scientific equations from data using LLM-guided evolutionary search.

## Input

- `$0` — Dataset description, variable names, and physical context

## References

- LLM-SR patterns (prompts, evolution, sampling): `${CODEX_HOME:-$HOME/.codex}/skills/symbolic-equation/references/llmsr-patterns.md`
- Research convergence policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`
- Venue-aware writing policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-writing-section/references/venue-writing-policy.md`

## Workflow (from LLM-SR)

### Step 1: Define Problem Specification
Create a specification with:
1. **Input variables**: Physical quantities with types (e.g., `x: np.ndarray`, `v: np.ndarray`)
2. **Output variable**: Target quantity to predict
3. **Evaluation function**: Fitness metric (typically negative MSE with parameter optimization)
4. **Physical context**: Domain knowledge to guide equation discovery

When any of the stable paper kernel, paper route, venue hypothesis, or evidence matrix already exists, use all available artifacts together to define the symbolic-equation task as support for a specific claim or evidence row. Do not use equation discovery to broaden the paper scope unless the user explicitly asks to reopen the kernel.

```python
# Example specification
@equation.evolve
def equation(x: np.ndarray, v: np.ndarray, params: np.ndarray) -> np.ndarray:
    """Describe the acceleration of a damped nonlinear oscillator."""
    return params[0] * x
```

### Step 2: Initialize Multi-Island Buffer
- Create N islands (default: 10) for population diversity
- Each island maintains independent clusters of equations
- Clusters group equations by performance signature

### Step 3: Evolutionary Search Loop
Repeat until convergence or max samples:
1. **Select island**: Random island selection
2. **Build prompt**: Sample top equations from clusters (softmax-weighted by score)
3. **LLM proposes**: Generate new equation as improved version
4. **Evaluate**: Execute on test data, compute fitness score
5. **Register**: Add to island's cluster if valid

### Step 4: Prompt Construction
Present previous equations as versioned sequence:
```python
def equation_v0(x, v, params):
    """Initial version."""
    return params[0] * x

def equation_v1(x, v, params):
    """Improved version of equation_v0."""
    return params[0] * x + params[1] * v

def equation_v2(x, v, params):
    """Improved version of equation_v1."""
    # LLM completes this
```

### Step 5: Island Reset (Diversity Maintenance)
Periodically (default: every 4 hours):
1. Sort islands by best score
2. Reset bottom 50% of islands
3. Seed each reset island with best equation from a surviving island
4. Restart cluster sampling temperature

### Step 6: Extract Best Equations
After search completes:
1. Collect best equation from each island
2. Rank by fitness score
3. Simplify if possible (algebraic simplification)
4. Validate on held-out data or task-relevant contexts before treating the equation as paper evidence
5. Report with physical interpretation and the exact evidence-matrix claim it supports

## Cluster Sampling

Temperature-scheduled softmax over cluster scores:
```
temperature = T_init * (1 - (num_programs % period) / period)
probabilities = softmax(cluster_scores / temperature)
```
- Higher temperature → more exploration
- Lower temperature → more exploitation of best clusters
- Within clusters: shorter programs are preferred (Occam's razor)

## Rules

- Equations must use only standard mathematical operations
- Parameter optimization via scipy BFGS or Adam
- Fitness = negative MSE (higher is better)
- Timeout protection for equation evaluation
- No recursive equations allowed
- Physical interpretability is preferred over pure fit
- For ML/robotics/CV/RL/embodied AI/LLM-VLM work, define validation around the task context: sequence splits, scenes, robots, environments, episodes, prompt/model conditions, or dataset protocols as appropriate.
- Treat discovered equations as explanatory or auxiliary evidence unless they directly drive the method and are validated under the target venue's expected protocol.
- End major symbolic-equation runs with a convergence closure: stable kernel impact, evidence row supported, bounded open questions, freeze criteria, and the next narrowing step.

## Related Skills
- Upstream: [data-analysis](../data-analysis/), [math-reasoning](../math-reasoning/)
- Downstream: [paper-writing-section](../paper-writing-section/)
- See also: [algorithm-design](../algorithm-design/)
