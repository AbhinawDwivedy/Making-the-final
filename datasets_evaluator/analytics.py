
# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from pathlib import Path
# import os

# # Set style
# sns.set_theme(style="whitegrid")

# DATASET_DIR = Path("datasets_evaluator")
# RESULTS_DIR = DATASET_DIR / "results"

# def load_results(task_name):
#     file_path = RESULTS_DIR / task_name / "cross_eval_results.json"
#     if not file_path.exists():
#         print(f"Results for {task_name} not found.")
#         return None
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def extract_scores(data, task_name):
#     rows = []
#     for item in data:
#         # Mini -> 4.1 (Mini judged 4.1)
#         eval_mini_of_4_1 = item.get("evaluation_of_4_1_by_mini", {})
#         # 4.1 -> Mini (4.1 judged Mini)
#         eval_4_1_of_mini = item.get("evaluation_of_mini_by_4_1", {})
        
#         # Extract scores
#         # Structure: { "faithfulness": { "score": 5, ... }, "overall": ... }
        
#         def get_metrics(eval_obj, judge_name, generator_name):
#             return {
#                 "Task": task_name,
#                 "Generator": generator_name,
#                 "Judge": judge_name,
#                 "Faithfulness": eval_obj.get("faithfulness", {}).get("score", 0),
#                 "Completeness": eval_obj.get("completeness", {}).get("score", 0),
#                 "Robustness": eval_obj.get("robustness", {}).get("score", 0),
#                 "Overall": eval_obj.get("overall", {}).get("score", 0)
#             }
            
#         rows.append(get_metrics(eval_mini_of_4_1, "Mini", "4.1"))
#         rows.append(get_metrics(eval_4_1_of_mini, "4.1", "Mini"))
        
#     return pd.DataFrame(rows)

# def generate_charts(df, task_name, output_dir):
#     # Melt for easier plotting
#     df_melted = df.melt(id_vars=["Generator", "Judge"], 
#                         value_vars=["Faithfulness", "Completeness", "Robustness", "Overall"],
#                         var_name="Metric", value_name="Score")
    
#     # Plot: Comparison of Models (Averaged across Judges? Or separate?)
#     # "vice versa 4.1 will write it and mini will evlaute it"
#     # User might want to see how each model performed according to the OTHER model.
#     # Generator: 4.1 (Judged by Mini) vs Generator: Mini (Judged by 4.1)
#     # This is a bit asymmetric but that's what was asked.
    
#     plt.figure(figsize=(10, 6))
#     ax = sns.barplot(data=df_melted, x="Metric", y="Score", hue="Generator", palette="viridis")
#     plt.title(f"Model Performance Comparison - {task_name.capitalize()}")
#     plt.ylim(0, 5.5)
#     plt.legend(title="Generator Model")
    
#     # Add labels
#     for container in ax.containers:
#         ax.bar_label(container, fmt='%.2f')
        
#     plt.tight_layout()
#     plt.savefig(output_dir / f"{task_name}_comparison_chart.png")
#     plt.close()

# def generate_report(df, task_name, output_dir):
#     # Summary stats
#     summary = df.groupby("Generator")[["Faithfulness", "Completeness", "Robustness", "Overall"]].mean()
    
#     metrics = ["Faithfulness", "Completeness", "Robustness", "Overall"]
    
#     md_lines = []
#     md_lines.append(f"# Analytics Report: {task_name.capitalize()}")
#     md_lines.append("")
#     md_lines.append(f"## Performance Summary")
#     md_lines.append("Average scores (out of 5):")
#     md_lines.append("")
#     md_lines.append(summary.to_markdown())
#     md_lines.append("")
    
#     # Detailed Analysis
#     md_lines.append("## Detailed Analysis")
    
#     # 4.1 Performance (Judged by Mini)
#     perf_4_1 = summary.loc["4.1"] if "4.1" in summary.index else None
#     perf_mini = summary.loc["Mini"] if "Mini" in summary.index else None
    
#     if perf_4_1 is not None and perf_mini is not None:
#         md_lines.append(f"- **Overall Winner**: {'4.1' if perf_4_1['Overall'] > perf_mini['Overall'] else 'Mini'}")
#         diff = perf_4_1['Overall'] - perf_mini['Overall']
#         md_lines.append(f"- **Score Difference**: {abs(diff):.2f} points")
        
#         md_lines.append("\n### Model 4.1 Strengths")
#         strongest = perf_4_1.idxmax()
#         md_lines.append(f"- Strongest category: **{strongest}** ({perf_4_1[strongest]:.2f})")
        
#         md_lines.append("\n### Model Mini Strengths")
#         strongest_mini = perf_mini.idxmax()
#         md_lines.append(f"- Strongest category: **{strongest_mini}** ({perf_mini[strongest_mini]:.2f})")

#     md_lines.append("")
#     md_lines.append(f"![Chart]({task_name}_comparison_chart.png)")
    
#     with open(output_dir / f"{task_name}_analytics_report.md", "w", encoding="utf-8") as f:
#         f.write("\n".join(md_lines))

# def main():
#     tasks = ["lengthen", "shorten", "tone"]
    
#     all_dfs = []
    
#     for task in tasks:
#         data = load_results(task)
#         if not data:
#             continue
            
#         df = extract_scores(data, task)
#         all_dfs.append(df)
        
#         out_dir = RESULTS_DIR / task
#         out_dir.mkdir(exist_ok=True)
        
#         generate_charts(df, task, out_dir)
#         generate_report(df, task, out_dir)
#         print(f"Generated analytics for {task}")

#     # Global Aggregate Report
#     if all_dfs:
#         full_df = pd.concat(all_dfs)
#         global_summary = full_df.groupby(["Task", "Generator"])["Overall"].mean().unstack()
        
#         print("\nGlobal Summary:")
#         print(global_summary)
        
#         # Global Chart
#         plt.figure(figsize=(12, 6))
#         sns.barplot(data=full_df, x="Task", y="Overall", hue="Generator", palette="magma")
#         plt.title("Overall Performance Across All Tasks")
#         plt.ylim(0, 5.5)
#         plt.tight_layout()
#         plt.savefig(RESULTS_DIR / "global_comparison_chart.png")
#         plt.close()

# if __name__ == "__main__":
#     main()
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
sns.set_theme(style="whitegrid")

DATASET_DIR = Path("datasets_evaluator")
RESULTS_DIR = DATASET_DIR / "results3"

TASKS = ["lengthen", "shorten", "tone"]
METRICS = ["Faithfulness", "Completeness", "Robustness", "Overall"]

# -----------------------------
# LOAD RESULTS
# -----------------------------
def load_results(task):
    path = RESULTS_DIR / task / "cross_eval_results.json"
    if not path.exists():
        print(f"❌ Missing results for {task}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
# EXTRACT SCORES
# -----------------------------
def extract_scores(data, task):
    rows = []

    for item in data:
        def row(eval_obj, generator, judge):
            return {
                "Task": task,
                "Generator": generator,
                "Judge": judge,
                "Direction": f"{generator}_gen__{judge}_eval",
                "Faithfulness": eval_obj.get("faithfulness", {}).get("score", 0),
                "Completeness": eval_obj.get("completeness", {}).get("score", 0),
                "Robustness": eval_obj.get("robustness", {}).get("score", 0),
                "Overall": eval_obj.get("overall", {}).get("score", 0),
            }

        rows.append(row(item.get("evaluation_of_4_1_by_4_1", {}), "4.1", "4.1"))
        rows.append(row(item.get("evaluation_of_mini_by_4_1", {}), "Mini", "4.1"))

    return pd.DataFrame(rows)

# -----------------------------
# PER-DIRECTION ANALYTICS
# -----------------------------
def generate_direction_analytics(df, task):
    for direction, sub_df in df.groupby("Direction"):
        out_dir = RESULTS_DIR / task / direction
        out_dir.mkdir(parents=True, exist_ok=True)

        summary = sub_df[METRICS].mean()

        # Save data
        summary.to_json(out_dir / "metrics_summary.json", indent=2)
        summary.to_frame("Average Score").to_csv(out_dir / "metrics_table.csv")

        # Plot
        plt.figure(figsize=(7, 5))
        ax = sns.barplot(
            x=summary.index,
            y=summary.values,
            palette="viridis"
        )
        plt.ylim(0, 5.5)
        plt.title(f"{task.capitalize()} — {direction.replace('_', ' ')}")

        for c in ax.containers:
            ax.bar_label(c, fmt="%.2f")

        plt.tight_layout()
        plt.savefig(out_dir / "metric_bar_chart.png")
        plt.close()

        # Report
        md = []
        md.append(f"# {task.capitalize()} Analytics")
        md.append("")
        md.append(f"**Generator → Evaluator:** `{direction}`")
        md.append("")
        md.append("## Average Scores")
        md.append("")
        md.append(summary.to_frame("Score").to_markdown())
        md.append("")
        md.append("## Notes")
        md.append("- Cross-model evaluation (no self-judging)")
        md.append("- Scores averaged across full dataset")
        md.append("")
        md.append("![Chart](metric_bar_chart.png)")

        with open(out_dir / "analytics_report.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md))

# -----------------------------
# CROSS-DIRECTION COMPARISON
# -----------------------------
def generate_comparison(df, task):
    out_dir = RESULTS_DIR / task / "comparison"
    out_dir.mkdir(exist_ok=True)

    comp = df.groupby("Direction")["Overall"].mean().reset_index()

    plt.figure(figsize=(7, 5))
    ax = sns.barplot(
        data=comp,
        x="Direction",
        y="Overall",
        palette="magma"
    )
    plt.ylim(0, 5.5)
    plt.title(f"{task.capitalize()} — Cross-Direction Comparison")
    plt.xticks(rotation=20)

    for c in ax.containers:
        ax.bar_label(c, fmt="%.2f")

    plt.tight_layout()
    plt.savefig(out_dir / "cross_direction_comparison.png")
    plt.close()

    md = []
    md.append(f"# {task.capitalize()} — Cross Evaluation Comparison")
    md.append("")
    md.append("This compares **directional evaluations**:")
    md.append("- 4.1 → Mini")
    md.append("- Mini → 4.1")
    md.append("")
    md.append(comp.to_markdown(index=False))
    md.append("")
    md.append("![Chart](cross_direction_comparison.png)")

    with open(out_dir / "comparison_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

# -----------------------------
# MAIN
# -----------------------------
def main():
    all_dfs = []

    for task in TASKS:
        data = load_results(task)
        if not data:
            continue

        df = extract_scores(data, task)
        all_dfs.append(df)

        generate_direction_analytics(df, task)
        generate_comparison(df, task)

        print(f"✅ Analytics generated for {task}")

    # Global overview (optional)
    if all_dfs:
        full_df = pd.concat(all_dfs)
        summary = full_df.groupby(["Task", "Direction"])["Overall"].mean()
        print("\n📊 Global Summary\n")
        print(summary)

if __name__ == "__main__":
    main()
