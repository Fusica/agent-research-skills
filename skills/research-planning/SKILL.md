---
name: research-planning
description: Design research plans and paper architectures. Given a research topic or idea, generate structured plans with methodology outlines, paper structure, dependency-ordered task lists, UML diagrams, and experiment designs. Use when starting a new research project or paper.
argument-hint: [topic-or-idea]
---

# Research Planning

Create comprehensive research plans and paper architectures from a research topic or idea.

## Input

- `$0` — Research topic, idea description, or paper to reproduce

## References

- Planning prompts from Paper2Code, AI-Researcher, AgentLaboratory: `${CODEX_HOME:-$HOME/.codex}/skills/research-planning/references/planning-prompts.md`
- Output schemas and templates: `${CODEX_HOME:-$HOME/.codex}/skills/research-planning/references/output-schemas.md`
- Research convergence policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`

## Workflow

### Step 1: Understand the Research Context
- Read any provided papers, code, or references
- Identify the core research question and its significance
- Assess available resources (datasets, compute, existing code)

### Step 2: Generate Research Plan
Use the 4-stage planning approach (adapted from Paper2Code):

1. **Overall Plan** — Strategic overview: methodology, key experiments, evaluation metrics
2. **Architecture Design** — File structure, system design, Mermaid class/sequence diagrams
3. **Logic Design** — Task breakdown with dependencies, required packages, shared knowledge
4. **Configuration** — Extract or specify hyperparameters, training details, config.yaml

### Step 2.5: Choose a Paper Route
Before expanding the plan, choose one primary and at most one secondary paper route:
- Algorithmic ML / robot learning: emphasize formulation, learning mechanism, generalization, and strong controlled experiments
- CV perception or benchmark method: emphasize datasets, baselines, metrics, ablations, qualitative cases, and protocol fairness
- Robotics systems or deployment: emphasize task relevance, system assumptions, runtime, robustness, deployment constraints, and autonomy linkage
- Embodied AI / LLM-VLM integration: emphasize the concrete robotics capability, measurable behavior, and why the foundation model changes the system
- Multimedia/video/AI engineering: emphasize video/multimodal task fit, efficiency, and reproducible engineering evidence

Map the route to candidate venue clusters and the evidence each cluster would require. Keep this as a working hypothesis until experiments justify a writing lock.

### Step 3: Structure the Paper
Design the paper structure with section-by-section plan:
- Abstract, Introduction, Background, Related Work, Methods, Experiments, Results, Discussion/Conclusion
- For each section: key points to cover, required figures/tables, target word count

### Step 4: Create Task Dependency Graph
- Order tasks by dependency (data → model → training → evaluation → writing)
- Identify parallelizable tasks
- Flag risks and potential failure modes

### Step 5: Convergence State
End the plan with the closure block from the research convergence policy. The plan should narrow the project from broad ML/robotics exploration into a stable paper kernel, not reopen unrelated directions.

## Output Format

```json
{
  "research_question": "...",
  "methodology": "...",
  "paper_structure": {
    "sections": ["Abstract", "Introduction", ...],
    "section_plans": { "Introduction": "..." }
  },
  "task_list": [
    {"task": "...", "depends_on": [], "priority": 1}
  ],
  "baselines": ["..."],
  "datasets": ["..."],
  "evaluation_metrics": ["..."],
  "risks": ["..."],
  "paper_route": "robotics systems",
  "venue_hypothesis": ["T-RO/T-ASE", "RA-L/ICRA/IROS"],
  "evidence_matrix": [
    {"claim": "...", "required_experiments": ["..."], "required_tables": ["..."]}
  ],
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

- Each plan component must be detailed and actionable
- Include specific implementation references when available
- Ensure all components work together coherently
- Always include a testing/evaluation plan
- Flag ambiguities explicitly rather than making assumptions
- Do not over-constrain scope early. Keep LLM/VLM, embodied AI, CV, RL, and robotics options open until the paper route and evidence matrix justify narrowing.
- Once a route is selected, avoid adding unrelated tasks unless they change venue fit, evidence sufficiency, or feasibility.

## Related Skills
- Upstream: [idea-generation](../idea-generation/), [literature-review](../literature-review/)
- Downstream: [experiment-design](../experiment-design/), [paper-assembly](../paper-assembly/)
- See also: [atomic-decomposition](../atomic-decomposition/)
