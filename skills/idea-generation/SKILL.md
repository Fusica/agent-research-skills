---
name: idea-generation
description: Generate novel research ideas with iterative refinement and novelty checking against literature. Score ideas on Interestingness, Feasibility, and Novelty. Use when brainstorming research directions or validating idea novelty.
argument-hint: [research-area]
---

# Idea Generation

Generate and refine novel research ideas with literature-backed novelty assessment.

## Input

- `$0` — Research area, task description, or existing codebase context
- `$1` — Optional: additional context (e.g., "for NeurIPS", constraints)

## Scripts

### Novelty check against Semantic Scholar
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/idea-generation/scripts/novelty_check.py \
  --idea "Adaptive attention head pruning via gradient-guided importance" \
  --max-rounds 5
```

Collects quality-filtered novelty evidence. Treat its `decision: "unclear"` as intentional; the agent must classify overlap and emit the convergence closure block.

## References

- Ideation prompts (generation, reflection, novelty): `${CODEX_HOME:-$HOME/.codex}/skills/idea-generation/references/ideation-prompts.md`
- Venue quality policy: `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/references/venue-quality-policy.md`
- Research convergence policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`

## Workflow

### Step 1: Generate Ideas
Given a research area and optional code/paper context:
1. Generate 3-5 diverse research ideas
2. For each idea, provide: Name, Title, Experiment plan, and ratings
3. Keep source quality filtering hard, but keep research scope broad within the ML/robotics umbrella
4. Use the ideation prompt templates from references

### Step 1.5: Classify Paper Type and Venue Fit
For each idea, classify the most plausible paper type:
- Algorithmic ML / robot learning
- CV perception, pose, tracking, or benchmark method
- Robotics systems, deployment, or autonomy
- Embodied AI / LLM-VLM / foundation-model integration
- Multimedia/video/AI engineering application

Then list 2-4 candidate venue clusters and the evidence they would require.
This is a convergence aid, not a hard exclusion rule.

### Step 2: Iterative Refinement (up to 5 rounds per idea)
For each idea:
1. Critically evaluate quality, novelty, and feasibility
2. Refine the idea while preserving its core spirit
3. Stop when converged ("I am done") or max rounds reached

### Step 3: Novelty Assessment
For each promising idea:
1. Run `novelty_check.py` or manually search Semantic Scholar / arXiv
2. Apply the venue quality filter before judging similar papers
3. Treat script output as evidence, not a final verdict
4. Use the novelty checking prompts from references
5. Multi-round search: generate queries, review filtered results, decide
6. Decision: Novel / Incremental / Not Novel / Unclear with justification

### Step 4: Rank and Select
- Score each idea on three dimensions (1-10): Interestingness, Feasibility, Novelty
- Be cautious and realistic on ratings
- Select the top idea(s) for development
- Freeze the current idea kernel when the contribution type, target venue cluster, and minimum evidence plan are stable enough to move into research planning

### Step 5: Closure
End each round with the closure block from the research convergence policy:
Current Stable Kernel, Open But Bounded Questions, Decision Log, Freeze Criteria, and Next Narrowing Step.

## Output Format

```json
{
  "Name": "adaptive_attention_pruning",
  "Title": "Adaptive Attention Head Pruning via Gradient-Guided Importance Scoring",
  "Experiment": "Detailed implementation plan...",
  "Interestingness": 8,
  "Feasibility": 7,
  "Novelty": 9,
  "novel": true,
  "most_similar_papers": ["paper1", "paper2"],
  "paper_type": "CV perception method",
  "venue_hypothesis": ["CVPR/ICCV/ECCV", "TPAMI/TIP"],
  "minimum_evidence": ["main benchmark", "ablation", "runtime/fairness check"],
  "resource_risks": ["small curated dataset may be needed"],
  "convergence_state": {
    "current_stable_kernel": "...",
    "open_but_bounded_questions": ["..."],
    "decision_log": ["..."],
    "freeze_criteria": "...",
    "next_narrowing_step": "..."
  }
}
```

## Rules

- Ideas must be feasible enough to evaluate; if they need new datasets, hardware, paid APIs, or large compute, keep them only when the resource risk is explicit and the expected venue payoff justifies it
- Do not overfit ideas to a specific dataset or model — aim for wider significance
- Be a harsh critic for novelty — ensure sufficient contribution for a conference paper
- Each idea should stem from a simple, elegant question or hypothesis
- Always check novelty before committing to an idea
- Do not use MDPI, blocked low-quality venues, or predatory-publisher matches as novelty evidence; if they appear, treat them only as excluded by user quality policy
- Do not make the scope unnecessarily rigid. LLM/VLM, embodied AI, and foundation-model ideas are allowed when they support a measurable ML/robotics contribution.
- Avoid endless expansion. Once the stable kernel and venue hypothesis are strong enough, stop adding minor angles and move to planning or experiments.

## Related Skills
- Upstream: [literature-search](../literature-search/), [deep-research](../deep-research/)
- Downstream: [research-planning](../research-planning/), [experiment-design](../experiment-design/)
- See also: [novelty-assessment](../novelty-assessment/)
