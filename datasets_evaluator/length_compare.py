# length_compare.py
import os
import json
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PATHS
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "length")

FIRST_EVAL_PATH = os.path.join(OUTPUT_DIR, "first_model_results.jsonl")
SECOND_EVAL_PATH = os.path.join(OUTPUT_DIR, "second_model_results.jsonl")

FIRST_DATA_PATH = os.path.join(OUTPUT_DIR, "first_model_data.jsonl")
SECOND_DATA_PATH = os.path.join(OUTPUT_DIR, "second_model_data.jsonl")

PLOT_DIR = os.path.join(OUTPUT_DIR, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

METRICS = ["faithfulness", "completeness", "robustness", "overall"]

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def avg_scores(rows):
    return {
        m: np.mean([r[m]["score"] for r in rows])
        for m in METRICS
    }


def extract_lengths(data_rows):
    return [
        (len(r["edited"]), r["id"])
        for r in data_rows
    ]


def extract_metric(rows, metric):
    return {
        r["id"]: r[metric]["score"]
        for r in rows
    }

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
first_eval = load_jsonl(FIRST_EVAL_PATH)
second_eval = load_jsonl(SECOND_EVAL_PATH)

first_data = load_jsonl(FIRST_DATA_PATH)
second_data = load_jsonl(SECOND_DATA_PATH)

# --------------------------------------------------
# AVERAGE SCORES + BAR CHART
# --------------------------------------------------
first_avg = avg_scores(first_eval)
second_avg = avg_scores(second_eval)

x = np.arange(len(METRICS))
width = 0.35

plt.figure()
plt.bar(x - width/2, [first_avg[m] for m in METRICS], width, label="First Model")
plt.bar(x + width/2, [second_avg[m] for m in METRICS], width, label="Second Model")

plt.xticks(x, METRICS)
plt.ylabel("Average Score")
plt.title("Average Evaluation Scores by Model")
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "avg_scores_bar.png"))
plt.close()

# --------------------------------------------------
# PER-METRIC DELTAS
# --------------------------------------------------
deltas = {
    m: second_avg[m] - first_avg[m]
    for m in METRICS
}

plt.figure()
plt.bar(METRICS, [deltas[m] for m in METRICS])
plt.axhline(0)

plt.ylabel("Score Delta (Second − First)")
plt.title("Per-Metric Score Deltas")

plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "metric_deltas.png"))
plt.close()

# --------------------------------------------------
# LENGTH vs FAITHFULNESS SCATTER
# --------------------------------------------------
first_lengths = extract_lengths(first_data)
second_lengths = extract_lengths(second_data)

first_faith = extract_metric(first_eval, "faithfulness")
second_faith = extract_metric(second_eval, "faithfulness")

plt.figure()

plt.scatter(
    [l for l, i in first_lengths],
    [first_faith[i] for l, i in first_lengths],
    label="First Model"
)

plt.scatter(
    [l for l, i in second_lengths],
    [second_faith[i] for l, i in second_lengths],
    label="Second Model"
)

plt.xlabel("Edited Text Length (chars)")
plt.ylabel("Faithfulness Score")
plt.title("Length vs Faithfulness")
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "length_vs_faithfulness.png"))
plt.close()

# --------------------------------------------------
# SUMMARY PRINT
# --------------------------------------------------
print("📊 Length Comparison Complete")
print("\nAverage Scores:")
for m in METRICS:
    print(f"{m:15s} | first={first_avg[m]:.3f} second={second_avg[m]:.3f} delta={deltas[m]:+.3f}")

print(f"\nPlots saved to: {PLOT_DIR}")
