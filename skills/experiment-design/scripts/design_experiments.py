#!/usr/bin/env python3
"""Generate experiment design from a research plan.

Takes a research plan (JSON or text description) and generates
a structured experiment design with baselines, ablation matrix,
hyperparameter grid, and evaluation metrics.

Self-contained: uses only stdlib.

Usage:
    python design_experiments.py --plan research_plan.json --output experiment_design.json
    python design_experiments.py --method "contrastive learning" --task "image classification" --output design.json
    python design_experiments.py --plan plan.json --format markdown
"""

import argparse
import json
import os
import sys


DEFAULT_HYPERPARAMS = {
    "learning_rate": [1e-4, 3e-4, 1e-3],
    "batch_size": [16, 32, 64],
    "epochs": [50, 100],
    "weight_decay": [0, 1e-4, 1e-2],
    "dropout": [0.0, 0.1, 0.3],
}

DEFAULT_METRICS = {
    "classification": ["accuracy", "f1_macro", "precision", "recall", "auroc"],
    "regression": ["mse", "mae", "r2", "rmse"],
    "generation": ["bleu", "rouge_l", "meteor", "perplexity"],
    "detection": ["map", "map50", "precision", "recall", "f1"],
    "segmentation": ["iou", "dice", "pixel_accuracy"],
    "retrieval": ["mrr", "ndcg", "recall_at_k", "precision_at_k"],
    "general": ["accuracy", "f1", "loss"],
}

STAGE_TEMPLATES = [
    {
        "name": "initial_implementation",
        "description": "Get a basic working implementation",
        "goals": [
            "Implement core method",
            "Run on simplest dataset",
            "Verify training loop works",
        ],
        "max_iterations": 5,
        "completion_criteria": "Working implementation with non-trivial performance",
    },
    {
        "name": "baseline_tuning",
        "description": "Tune hyperparameters and establish baselines",
        "goals": [
            "Tune learning rate and batch size",
            "Compare against at least 2 baselines",
            "Test on route-appropriate independent evaluation contexts",
        ],
        "max_iterations": 10,
        "completion_criteria": "Stable training, improvement over baselines",
    },
    {
        "name": "creative_research",
        "description": "Explore novel improvements",
        "goals": [
            "Try architectural modifications",
            "Explore loss function variants",
            "Expand only to decisive evaluation contexts for the venue hypothesis",
        ],
        "max_iterations": 15,
        "completion_criteria": "Demonstrated novel improvement",
    },
    {
        "name": "ablation_studies",
        "description": "Systematic component analysis",
        "goals": [
            "Ablate each proposed component",
            "Test sensitivity to hyperparameters",
            "Use the replication unit appropriate for the paper route",
        ],
        "max_iterations": 10,
        "completion_criteria": "All planned ablations completed",
    },
]


def generate_ablation_matrix(components: list[str]) -> list[dict]:
    """Generate ablation study matrix from component list."""
    ablations = [{"name": "Full Model", "components": {c: True for c in components}}]
    for comp in components:
        ablation = {
            "name": f"w/o {comp}",
            "components": {c: (c != comp) for c in components},
        }
        ablations.append(ablation)
    return ablations


def generate_design(plan: dict) -> dict:
    """Generate a full experiment design from a research plan."""
    method = plan.get("method", "proposed method")
    task_type = plan.get("task_type", "general")
    paper_route = plan.get("paper_route", "unspecified")
    venue_hypothesis = plan.get("venue_hypothesis", [])
    components = plan.get("components", ["component_A", "component_B", "component_C"])
    baselines = plan.get("baselines", [])
    datasets = plan.get("datasets", [])
    evaluation_contexts = plan.get("evaluation_contexts") or datasets or ["primary_evaluation_context"]
    evidence_matrix = plan.get("evidence_matrix") or [
        {
            "claim": f"{method} improves the primary task",
            "experiment": "main comparison against protocol-compatible baselines",
            "metric": "primary_metric",
            "target_table_or_figure": "main results table",
        },
        {
            "claim": "Each proposed component contributes to the result",
            "experiment": "component ablation",
            "metric": "primary_metric",
            "target_table_or_figure": "ablation table",
        },
    ]
    custom_metrics = plan.get("metrics", [])
    upstream_state = plan.get("convergence_state", {}) if isinstance(plan.get("convergence_state"), dict) else {}
    replication = plan.get("replication", {}) if isinstance(plan.get("replication"), dict) else {}
    replication_unit = replication.get("unit") or plan.get("replication_unit") or "seed"
    replication_count = int(replication.get("count") or plan.get("num_seeds") or plan.get("num_repetitions") or 1)
    comparable_repetitions = bool(replication.get("comparable", replication_count >= 3))

    # Select metrics
    metrics = custom_metrics or DEFAULT_METRICS.get(task_type, DEFAULT_METRICS["general"])

    # Generate hyperparameter grid
    hp_grid = plan.get("hyperparameter_grid", {})
    if not hp_grid:
        hp_grid = {
            "learning_rate": DEFAULT_HYPERPARAMS["learning_rate"],
            "batch_size": DEFAULT_HYPERPARAMS["batch_size"],
        }

    # Generate ablation matrix
    ablations = generate_ablation_matrix(components)

    # Compute total experiments estimate
    n_hp_configs = 1
    for vals in hp_grid.values():
        n_hp_configs *= len(vals)
    n_contexts = max(len(evaluation_contexts), 1)
    n_ablations = len(ablations)
    n_baselines = max(len(baselines), 1)
    total_runs = (n_hp_configs + n_ablations + n_baselines) * n_contexts * replication_count

    design = {
        "method": method,
        "task_type": task_type,
        "paper_route": paper_route,
        "venue_hypothesis": venue_hypothesis,
        "stages": STAGE_TEMPLATES,
        "baselines": baselines,
        "datasets": datasets,
        "evaluation_contexts": evaluation_contexts,
        "metrics": metrics,
        "primary_metric": metrics[0] if metrics else "accuracy",
        "components": components,
        "ablation_matrix": ablations,
        "evidence_matrix": evidence_matrix,
        "hyperparameter_grid": hp_grid,
        "replication": {
            "unit": replication_unit,
            "count": replication_count,
            "comparable": comparable_repetitions,
        },
        "num_seeds": replication_count if replication_unit == "seed" else None,
        "estimated_total_runs": total_runs,
        "evaluation_protocol": {
            "report_mean_std": comparable_repetitions,
            "statistical_test": (
                replication.get("statistical_test")
                or ("paired_ttest" if comparable_repetitions and replication_unit == "seed" else "none")
            ),
            "significance_level": 0.05,
        },
        "convergence_state": {
            "current_stable_kernel": upstream_state.get(
                "current_stable_kernel",
                plan.get(
                    "stable_kernel",
                    f"{method} on {task_type} with route-aware evaluation",
                ),
            ),
            "open_but_bounded_questions": upstream_state.get(
                "open_but_bounded_questions",
                plan.get(
                    "open_but_bounded_questions",
                    ["Confirm that each claim in the evidence matrix has a feasible experiment"],
                ),
            ),
            "decision_log": upstream_state.get(
                "decision_log",
                plan.get(
                    "decision_log",
                    ["Generated route-aware experiment design from the current research plan"],
                ),
            ),
            "freeze_criteria": upstream_state.get(
                "freeze_criteria",
                plan.get(
                    "freeze_criteria",
                    "Freeze experiment expansion once every major claim has decisive evidence and venue fit is clear.",
                ),
            ),
            "next_narrowing_step": upstream_state.get(
                "next_narrowing_step",
                plan.get(
                    "next_narrowing_step",
                    "Run the smallest main comparison that can validate or falsify the stable kernel.",
                ),
            ),
        },
    }

    return design


def format_markdown(design: dict) -> str:
    """Format experiment design as markdown."""
    lines = [f"# Experiment Design: {design['method']}\n"]

    lines.append(f"## Task Type: {design['task_type']}\n")
    lines.append(f"## Paper Route: {design['paper_route']}\n")
    if design["venue_hypothesis"]:
        lines.append("## Venue Hypothesis\n")
        for venue in design["venue_hypothesis"]:
            lines.append(f"- {venue}")
        lines.append("")

    lines.append("## Stages\n")
    for i, stage in enumerate(design["stages"], 1):
        lines.append(f"### Stage {i}: {stage['name']}")
        lines.append(f"{stage['description']}\n")
        for goal in stage["goals"]:
            lines.append(f"- {goal}")
        lines.append(f"- Completion: {stage['completion_criteria']}\n")

    if design["baselines"]:
        lines.append("## Baselines\n")
        for b in design["baselines"]:
            lines.append(f"- {b}")
        lines.append("")

    if design["datasets"]:
        lines.append("## Datasets\n")
        for d in design["datasets"]:
            lines.append(f"- {d}")
        lines.append("")

    if design["evaluation_contexts"]:
        lines.append("## Evaluation Contexts\n")
        for c in design["evaluation_contexts"]:
            lines.append(f"- {c}")
        lines.append("")

    lines.append("## Evidence Matrix\n")
    lines.append("| Claim | Experiment | Metric | Target |")
    lines.append("|---|---|---|---|")
    for item in design["evidence_matrix"]:
        lines.append(
            "| {claim} | {experiment} | {metric} | {target} |".format(
                claim=item.get("claim", ""),
                experiment=item.get("experiment", ""),
                metric=item.get("metric", ""),
                target=item.get("target_table_or_figure", ""),
            )
        )
    lines.append("")

    lines.append("## Metrics\n")
    lines.append(f"Primary: **{design['primary_metric']}**\n")
    for m in design["metrics"]:
        lines.append(f"- {m}")
    lines.append("")

    lines.append("## Ablation Matrix\n")
    comps = design["components"]
    header = "| Variant | " + " | ".join(comps) + " |"
    sep = "|" + "|".join(["---"] * (len(comps) + 1)) + "|"
    lines.append(header)
    lines.append(sep)
    for ab in design["ablation_matrix"]:
        row = f"| {ab['name']} | "
        row += " | ".join("Y" if ab["components"][c] else "N" for c in comps)
        row += " |"
        lines.append(row)
    lines.append("")

    lines.append("## Hyperparameter Grid\n")
    for param, vals in design["hyperparameter_grid"].items():
        lines.append(f"- {param}: {vals}")
    lines.append("")

    lines.append(f"## Summary\n")
    lines.append(f"- Replication: {design['replication']['count']} x {design['replication']['unit']}")
    lines.append(f"- Estimated total runs: {design['estimated_total_runs']}")
    lines.append(f"- Statistical test: {design['evaluation_protocol']['statistical_test']}")

    state = design["convergence_state"]
    lines.append("")
    lines.append("## Convergence State\n")
    lines.append(f"- Current Stable Kernel: {state['current_stable_kernel']}")
    lines.append("- Open But Bounded Questions:")
    for item in state["open_but_bounded_questions"]:
        lines.append(f"  - {item}")
    lines.append("- Decision Log:")
    for item in state["decision_log"]:
        lines.append(f"  - {item}")
    lines.append(f"- Freeze Criteria: {state['freeze_criteria']}")
    lines.append(f"- Next Narrowing Step: {state['next_narrowing_step']}")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate experiment design from research plan")
    parser.add_argument("--plan", help="Research plan JSON file")
    parser.add_argument("--method", help="Method name (if no plan file)")
    parser.add_argument("--task", help="Task type: classification, regression, generation, etc.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json",
                        help="Output format (default: json)")
    parser.add_argument("--output", "-o", help="Output file")
    args = parser.parse_args()

    if args.plan and os.path.exists(args.plan):
        with open(args.plan, encoding="utf-8") as f:
            plan = json.load(f)
    elif args.method:
        plan = {
            "method": args.method,
            "task_type": args.task or "general",
        }
    else:
        print("Error: specify --plan or --method", file=sys.stderr)
        sys.exit(1)

    design = generate_design(plan)

    if args.format == "markdown":
        output = format_markdown(design)
    else:
        output = json.dumps(design, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Design written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
