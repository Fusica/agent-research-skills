---
name: novelty-assessment
description: Assess research idea novelty through systematic literature search. Multi-round search-evaluate loops with harsh critic persona. Binary novel/not-novel decision with justification. Use before committing to a research direction.
argument-hint: [idea]
---

# Novelty Assessment

Rigorously assess whether a research idea is novel through systematic literature search.

## Input

- `$0` — Research idea description, title, or JSON file

## Scripts

### Automated novelty check
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/idea-generation/scripts/novelty_check.py \
  --idea "Your research idea description" \
  --max-rounds 10 --output novelty_report.json
```
This script collects unrestricted topic-relevant evidence only. Its default `decision: "unclear"` must be replaced by the agent after overlap assessment.

### Literature search
```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/search_semantic_scholar.py \
  --query "relevant search query" --max-results 10
```

## References

- Assessment prompts and criteria: `${CODEX_HOME:-$HOME/.codex}/skills/novelty-assessment/references/assessment-prompts.md`
- Publication relevance policy: `${CODEX_HOME:-$HOME/.codex}/skills/deep-research/references/publication-relevance-policy.md`
- Research convergence policy: `${CODEX_HOME:-$HOME/.codex}/skills/paper-assembly/references/research-convergence-policy.md`

## Workflow

### Step 1: Understand the Idea
- Identify the core contribution
- List the key technical components
- Determine the research area and subfield

### Step 2: Multi-Round Literature Search (up to 10 rounds)
For each round:
1. Generate a targeted search query
2. Search Semantic Scholar / arXiv / OpenAlex
3. Run `filter_publications.py` only as a keep-all compatibility passthrough, or use `novelty_check.py`
4. Review top topic-relevant results with abstracts
5. Assess overlap with the idea
6. Decide: need more searching, or ready to decide

### Step 3: Make Decision
- **Novel**: After sufficient searching, no retrieved paper significantly overlaps
- **Incremental**: The idea is related to strong prior work, but a sharper formulation, evidence target, or venue positioning may still make it publishable
- **Not Novel**: Found a paper that significantly overlaps
- **Unclear**: Search evidence is insufficient or the idea kernel is still unstable

### Step 4: Position the Idea
If novel, identify:
- Most similar existing papers (for Related Work)
- How the idea differs from each
- The specific gap this idea fills
- The likely paper type and candidate venue cluster
- Which experiments are needed to convert novelty into a publishable claim

### Step 5: Bound Remaining Questions
Do not keep adding minor novelty concerns indefinitely. Split open issues into:
- Fatal novelty risks
- Experiment-resolvable risks
- Writing or venue-positioning risks
- Non-blocking details

End with the closure block from the research convergence policy so the next round narrows rather than reopens the whole idea.

## Harsh Critic Persona

```
Be a harsh critic for novelty. Ensure there is a sufficient contribution
for a new conference or workshop paper. A trivial extension of existing
work is NOT novel. The idea must offer a meaningfully different approach,
formulation, or insight.
```

## Output Format

```json
{
  "decision": "novel" | "incremental" | "not_novel" | "unclear",
  "confidence": "high" | "medium" | "low",
  "justification": "After searching X rounds...",
  "most_similar_papers": [
    {"title": "...", "year": 2024, "overlap": "..."}
  ],
  "differentiation": "Our idea differs because...",
  "fatal_risks": [],
  "experiment_resolvable_risks": [],
  "venue_positioning_risks": [],
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

- Minimum 3 search rounds before declaring novel
- Try to recall exact paper names for targeted queries
- A paper idea is NOT novel if it's a trivial extension
- Consider both methodology novelty AND application novelty
- Check for concurrent/recent arXiv submissions
- Use any topically relevant paper as overlap evidence regardless of venue, publisher, journal, DOI prefix, domain, or preprint status
- Treat ML/robotics as a broad umbrella. Do not reject LLM/VLM/foundation-model or embodied-AI related ideas unless they lack a measurable link to the target research problem.
- Once the decision is stable, stop surfacing new small objections unless they are fatal to novelty, feasibility, or venue fit.

## Related Skills
- Upstream: [literature-search](../literature-search/), [deep-research](../deep-research/)
- Downstream: [idea-generation](../idea-generation/), [research-planning](../research-planning/)
- See also: [related-work-writing](../related-work-writing/)
