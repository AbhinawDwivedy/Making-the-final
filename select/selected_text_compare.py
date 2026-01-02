"""
Scenario 1: Selected Text Preservation - Model Comparison
Compares multiple models on selected text preservation performance.
"""

import os
import json
import argparse
from collections import defaultdict


def load_results(file_path):
    """Load evaluation results from JSONL file."""
    results = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                results.append(json.loads(line))
        return results
    except FileNotFoundError:
        print(f"⚠️  File not found: {file_path}")
        return None


def calculate_metrics(results):
    """Calculate aggregate metrics from results."""
    if not results:
        return None
    
    metrics = {
        "total_samples": len(results),
        "boundary_preservation": {
            "correctly_scoped_count": 0,
            "correctly_scoped_rate": 0.0
        },
        "average_scores": {},
        "score_distribution": defaultdict(lambda: defaultdict(int))
    }
    
    # Boundary check metrics
    correctly_scoped = sum(
        1 for r in results 
        if r.get("boundary_check", {}).get("correctly_scoped", False)
    )
    metrics["boundary_preservation"]["correctly_scoped_count"] = correctly_scoped
    metrics["boundary_preservation"]["correctly_scoped_rate"] = (
        correctly_scoped / len(results) if results else 0.0
    )
    
    # LLM evaluation metrics
    eval_metrics = [
        "selection_boundary_preservation",
        "edit_quality",
        "faithfulness",
        "completeness",
        "overall"
    ]
    
    for metric in eval_metrics:
        scores = []
        for r in results:
            if r.get("evaluation") and metric in r["evaluation"]:
                score = r["evaluation"][metric]["score"]
                scores.append(score)
                metrics["score_distribution"][metric][score] += 1
        
        metrics["average_scores"][metric] = (
            sum(scores) / len(scores) if scores else 0.0
        )
    
    return metrics


def print_comparison(model_metrics):
    """Print formatted comparison of models."""
    print(f"\n{'='*80}")
    print("📊 SCENARIO 1: SELECTED TEXT PRESERVATION - MODEL COMPARISON")
    print(f"{'='*80}\n")
    
    models = list(model_metrics.keys())
    
    # Sample counts
    print("📈 Sample Counts:")
    for model in models:
        count = model_metrics[model]["total_samples"]
        print(f"  {model}: {count} samples")
    
    # Boundary preservation rates
    print(f"\n🎯 Boundary Preservation (Correctly Scoped):")
    for model in models:
        rate = model_metrics[model]["boundary_preservation"]["correctly_scoped_rate"]
        count = model_metrics[model]["boundary_preservation"]["correctly_scoped_count"]
        total = model_metrics[model]["total_samples"]
        print(f"  {model}: {count}/{total} ({rate*100:.1f}%)")
    
    # Average scores comparison
    print(f"\n📊 Average Scores (0-5 scale):")
    print(f"{'Metric':<40} " + " ".join(f"{m:^12}" for m in models))
    print("-" * 80)
    
    metrics = [
        "selection_boundary_preservation",
        "edit_quality",
        "faithfulness",
        "completeness",
        "overall"
    ]
    
    for metric in metrics:
        row = f"{metric:<40}"
        for model in models:
            score = model_metrics[model]["average_scores"].get(metric, 0.0)
            row += f" {score:>12.2f}"
        print(row)
    
    # Winner summary
    print(f"\n🏆 Best Performing Model:")
    best_model = max(
        models,
        key=lambda m: model_metrics[m]["average_scores"].get("overall", 0)
    )
    best_score = model_metrics[best_model]["average_scores"]["overall"]
    print(f"  {best_model} (Overall: {best_score:.2f}/5)")
    
    print(f"\n{'='*80}\n")


def save_comparison_report(model_metrics, output_file):
    """Save detailed comparison report to JSON."""
    report = {
        "scenario": "Scenario 1: Selected Text Preservation",
        "models": model_metrics,
        "summary": {
            "best_model": max(
                model_metrics.keys(),
                key=lambda m: model_metrics[m]["average_scores"].get("overall", 0)
            ),
            "best_overall_score": max(
                m["average_scores"].get("overall", 0)
                for m in model_metrics.values()
            )
        }
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Detailed report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare model performance on Scenario 1"
    )
    parser.add_argument(
        "--results",
        nargs="+",
        required=True,
        help="Result files to compare (e.g., selected_text_results_gpt-4.1.jsonl)"
    )
    parser.add_argument(
        "--output",
        default="selected_text_comparison_report.json",
        help="Output comparison report file"
    )
    args = parser.parse_args()
    
    # Load and process results
    model_metrics = {}
    
    for result_file in args.results:
        # Extract model name from filename
        # Format: selected_text_results_{model}.jsonl
        model_name = result_file.replace("selected_text_results_", "").replace(".jsonl", "")
        
        results = load_results(result_file)
        if results:
            metrics = calculate_metrics(results)
            if metrics:
                model_metrics[model_name] = metrics
    
    if not model_metrics:
        print("❌ No valid results to compare")
        return
    
    # Print comparison
    print_comparison(model_metrics)
    
    # Save report
    save_comparison_report(model_metrics, args.output)


if __name__ == "__main__":
    main()
