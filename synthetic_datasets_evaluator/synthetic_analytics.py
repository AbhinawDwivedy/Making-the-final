# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from pathlib import Path

# # -----------------------------
# # CONFIG
# # -----------------------------
# sns.set_theme(style="whitegrid")

# BASE_DIR = Path(__file__).resolve().parent
# RESULTS_DIR = BASE_DIR / "synthetic_result"

# TASKS = ["lengthen", "shorten", "tone"]
# METRICS = ["Faithfulness", "Completeness", "Robustness", "Overall"]

# # -----------------------------
# # LOAD RESULTS
# # -----------------------------
# def load_results(task):
#     path = RESULTS_DIR / task / "cross_eval_results.json"
#     if not path.exists():
#         print(f"❌ Missing results for {task}")
#         return None
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)

# # -----------------------------
# # EXTRACT SCORES
# # -----------------------------
# def extract_scores(data, task):
#     rows = []

#     for item in data:
#         def row(eval_obj, generator, judge):
#             return {
#                 "Task": task,
#                 "Generator": generator,
#                 "Judge": judge,
#                 "Direction": f"{generator}_gen__{judge}_eval",
#                 "Faithfulness": eval_obj.get("faithfulness", {}).get("score", 0),
#                 "Completeness": eval_obj.get("completeness", {}).get("score", 0),
#                 "Robustness": eval_obj.get("robustness", {}).get("score", 0),
#                 "Overall": eval_obj.get("overall", {}).get("score", 0),
#             }

#         rows.append(row(item.get("evaluation_of_4_1_by_mini", {}), "4.1", "Mini"))
#         rows.append(row(item.get("evaluation_of_mini_by_4_1", {}), "Mini", "4.1"))

#     return pd.DataFrame(rows)

# # -----------------------------
# # PER-DIRECTION ANALYTICS
# # -----------------------------
# def generate_direction_analytics(df, task):
#     for direction, sub_df in df.groupby("Direction"):
#         out_dir = RESULTS_DIR / task / direction
#         out_dir.mkdir(parents=True, exist_ok=True)

#         summary = sub_df[METRICS].mean()

#         # Save data
#         summary.to_json(out_dir / "metrics_summary.json", indent=2)
#         summary.to_frame("Average Score").to_csv(out_dir / "metrics_table.csv")

#         # Plot
#         plt.figure(figsize=(7, 5))
#         ax = sns.barplot(
#             x=summary.index,
#             y=summary.values,
#             palette="viridis"
#         )
#         plt.ylim(0, 5.5)
#         plt.title(f"{task.capitalize()} — {direction.replace('_', ' ')}")

#         for c in ax.containers:
#             ax.bar_label(c, fmt="%.2f")

#         plt.tight_layout()
#         plt.savefig(out_dir / "metric_bar_chart.png")
#         plt.close()

#         # Report
#         md = []
#         md.append(f"# {task.capitalize()} Analytics")
#         md.append("")
#         md.append(f"**Generator → Evaluator:** `{direction}`")
#         md.append("")
#         md.append("## Average Scores")
#         md.append("")
#         md.append(summary.to_frame("Score").to_markdown())
#         md.append("")
#         md.append("## Notes")
#         md.append("- Cross-model evaluation (no self-judging)")
#         md.append("- Scores averaged across full dataset")
#         md.append("")
#         md.append("![Chart](metric_bar_chart.png)")

#         with open(out_dir / "analytics_report.md", "w", encoding="utf-8") as f:
#             f.write("\n".join(md))

# # -----------------------------
# # CROSS-DIRECTION COMPARISON
# # -----------------------------
# def generate_comparison(df, task):
#     out_dir = RESULTS_DIR / task / "comparison"
#     out_dir.mkdir(exist_ok=True)

#     comp = df.groupby("Direction")["Overall"].mean().reset_index()

#     plt.figure(figsize=(7, 5))
#     ax = sns.barplot(
#         data=comp,
#         x="Direction",
#         y="Overall",
#         palette="magma"
#     )
#     plt.ylim(0, 5.5)
#     plt.title(f"{task.capitalize()} — Cross-Direction Comparison")
#     plt.xticks(rotation=20)

#     for c in ax.containers:
#         ax.bar_label(c, fmt="%.2f")

#     plt.tight_layout()
#     plt.savefig(out_dir / "cross_direction_comparison.png")
#     plt.close()

#     md = []
#     md.append(f"# {task.capitalize()} — Cross Evaluation Comparison")
#     md.append("")
#     md.append("This compares **directional evaluations**:")
#     md.append("- 4.1 → Mini")
#     md.append("- Mini → 4.1")
#     md.append("")
#     md.append(comp.to_markdown(index=False))
#     md.append("")
#     md.append("![Chart](cross_direction_comparison.png)")

#     with open(out_dir / "comparison_report.md", "w", encoding="utf-8") as f:
#         f.write("\n".join(md))

# # -----------------------------
# # MAIN
# # -----------------------------
# def main():
#     all_dfs = []

#     for task in TASKS:
#         data = load_results(task)
#         if not data:
#             continue

#         df = extract_scores(data, task)
#         all_dfs.append(df)

#         generate_direction_analytics(df, task)
#         generate_comparison(df, task)

#         print(f"✅ Analytics generated for {task}")

#     # Global overview (optional)
#     if all_dfs:
#         full_df = pd.concat(all_dfs)
#         summary = full_df.groupby(["Task", "Direction"])["Overall"].mean()
#         print("\n📊 Global Summary\n")
#         print(summary)

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

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "synthetic_result"

TASKS = ["lengthen", "shorten", "tone"]
METRICS = ["Faithfulness", "Completeness", "Robustness", "Overall"]

# -----------------------------
# LOAD RESULTS
# -----------------------------
def load_results(task):
    path = RESULTS_DIR / task / "cross_eval_results.json"
    if not path.exists():
        print(f"❌ Missing results for {task}: {path}")
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
# EXTRACT SCORES
# -----------------------------
def extract_scores(data, task):
    rows = []

    for item in data:
        def make_row(eval_obj, generator, judge):
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

        # 4.1 generated → 4.1 evaluated
        rows.append(
            make_row(
                item.get("evaluation_of_4_1_by_4_1", {}),
                "4.1",
                "4.1"
            )
        )

        # Mini generated → 4.1 evaluated
        rows.append(
            make_row(
                item.get("evaluation_of_mini_by_4_1", {}),
                "Mini",
                "4.1"
            )
        )

    return pd.DataFrame(rows)

# -----------------------------
# PER-DIRECTION ANALYTICS
# -----------------------------
def generate_direction_analytics(df, task):
    for direction, sub_df in df.groupby("Direction"):
        out_dir = RESULTS_DIR / task / direction
        out_dir.mkdir(parents=True, exist_ok=True)

        summary = sub_df[METRICS].mean()

        # Save numeric data
        summary.to_json(out_dir / "metrics_summary.json", indent=2)
        summary.to_frame("Average Score").to_csv(out_dir / "metrics_table.csv")

        # Plot
        plt.figure(figsize=(7, 5))
        ax = sns.barplot(
            x=summary.index,
            y=summary.values
        )
        plt.ylim(0, 5.5)
        plt.title(f"{task.capitalize()} — {direction.replace('_', ' ')}")

        for c in ax.containers:
            ax.bar_label(c, fmt="%.2f")

        plt.tight_layout()
        plt.savefig(out_dir / "metric_bar_chart.png")
        plt.close()

        # Markdown report
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
        md.append("- Evaluation performed only by GPT-4.1")
        md.append("- Scores averaged across dataset")
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
        y="Overall"
    )
    plt.ylim(0, 5.5)
    plt.title(f"{task.capitalize()} — Cross Direction Comparison")
    plt.xticks(rotation=20)

    for c in ax.containers:
        ax.bar_label(c, fmt="%.2f")

    plt.tight_layout()
    plt.savefig(out_dir / "cross_direction_comparison.png")
    plt.close()

    md = []
    md.append(f"# {task.capitalize()} — Cross Evaluation Comparison")
    md.append("")
    md.append("Comparison of generation quality judged by GPT-4.1:")
    md.append("- 4.1 → 4.1")
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

    # Global summary
    if all_dfs:
        full_df = pd.concat(all_dfs)
        summary = full_df.groupby(["Task", "Direction"])["Overall"].mean()

        print("\n📊 GLOBAL SUMMARY\n")
        print(summary)

if __name__ == "__main__":
    main()
