# # import os
# # import json
# # import yaml
# # from dotenv import load_dotenv
# # from openai import OpenAI

# # # --------------------------------------------------
# # # ENV (EXPLICIT — SAME AS WORKING EmailJudge)
# # # --------------------------------------------------
# # load_dotenv()

# # client = OpenAI(
# #     api_key=os.getenv("OPENAI_API_KEY"),
# #     base_url=os.getenv("OPENAI_API_BASE")
# # )

# # FIRST_ELAB_MODEL = os.getenv("OPENAI_FIRST_ELABORATE_MODEL")
# # SECOND_ELAB_MODEL = os.getenv("OPENAI_SECOND_ELABORATE_MODEL")
# # FIRST_EVAL_MODEL = os.getenv("OPENAI_FIRST_EVAL_MODEL")
# # SECOND_EVAL_MODEL = os.getenv("OPENAI_SECOND_EVAL_MODEL")

# # # --------------------------------------------------
# # # PATHS
# # # --------------------------------------------------
# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # DATASET_PATH = os.path.join(
# #     BASE_DIR, "..", "datasets", "lengthen.jsonl"
# # )

# # PROMPT_PATH = os.path.join(
# #     BASE_DIR, "..", "prompts.yaml"
# # )

# # OUTPUT_DIR = os.path.join(BASE_DIR, "length")
# # os.makedirs(OUTPUT_DIR, exist_ok=True)

# # # --------------------------------------------------
# # # LOAD PROMPTS (MATCHES YOUR YAML EXACTLY)
# # # --------------------------------------------------
# # with open(PROMPT_PATH, "r", encoding="utf-8") as f:
# #     PROMPTS = yaml.safe_load(f)

# # EMAIL_CORE_SYS = PROMPTS["email_core"]["system"]

# # LENGTHEN_SYS = PROMPTS["lengthen"]["system"]
# # LENGTHEN_USER = PROMPTS["lengthen"]["user"]

# # EVAL_SYS = PROMPTS["evaluate"]["system"]
# # EVAL_USER = PROMPTS["evaluate"]["user"]

# # # --------------------------------------------------
# # # HELPERS
# # # --------------------------------------------------
# # def load_jsonl(path):
# #     if not os.path.exists(path):
# #         raise FileNotFoundError(f"Dataset not found: {path}")

# #     rows = []
# #     with open(path, "r", encoding="utf-8") as f:
# #         for line in f:
# #             rows.append(json.loads(line))
# #     return rows


# # def write_jsonl(path, rows):
# #     with open(path, "w", encoding="utf-8") as f:
# #         for r in rows:
# #             f.write(json.dumps(r, ensure_ascii=False) + "\n")


# # def chat(model, messages, temperature=0.3):
# #     response = client.chat.completions.create(
# #         model=model,
# #         messages=messages,
# #         temperature=temperature
# #     )
# #     return response.choices[0].message.content.strip()

# # # --------------------------------------------------
# # # GENERATION (ELABORATION)
# # # --------------------------------------------------
# # def generate(dataset, model, out_path):
# #     system_prompt = EMAIL_CORE_SYS + "\n\n" + LENGTHEN_SYS
# #     outputs = []

# #     for row in dataset:
# #         user_prompt = LENGTHEN_USER.format(
# #             selected_text=row["content"]
# #         )

# #         edited = chat(
# #             model,
# #             [
# #                 {"role": "system", "content": system_prompt},
# #                 {"role": "user", "content": user_prompt}
# #             ]
# #         )

# #         outputs.append({
# #             "id": row["id"],
# #             "generator_model": model,
# #             "original": row["content"],
# #             "edited": edited
# #         })

# #     write_jsonl(out_path, outputs)

# # # --------------------------------------------------
# # # EVALUATION
# # # --------------------------------------------------
# # def evaluate(generated_rows, model, out_path):
# #     results = []

# #     for row in generated_rows:
# #         user_prompt = EVAL_USER.format(
# #             original=row["original"],
# #             edited=row["edited"]
# #         )

# #         raw = chat(
# #             model,
# #             [
# #                 {"role": "system", "content": EVAL_SYS},
# #                 {"role": "user", "content": user_prompt}
# #             ],
# #             temperature=0
# #         )

# #         try:
# #             parsed = json.loads(raw)
# #         except Exception:
# #             parsed = {
# #                 "faithfulness": {"score": 0, "reason": "Invalid JSON"},
# #                 "completeness": {"score": 0, "reason": "Invalid JSON"},
# #                 "robustness": {"score": 0, "reason": "Invalid JSON"},
# #                 "overall": {"score": 0, "reason": "Invalid JSON"}
# #             }

# #         results.append({
# #             "id": row["id"],
# #             "eval_model": model,
# #             **parsed
# #         })

# #     write_jsonl(out_path, results)

# # # --------------------------------------------------
# # # MAIN (FIRST 5 ONLY — TEST MODE)
# # # --------------------------------------------------
# # def main():
# #     dataset = load_jsonl(DATASET_PATH)[:5]

# #     # -------- FIRST MODEL PIPELINE --------
# #     first_data_path = os.path.join(OUTPUT_DIR, "first_model_data.jsonl")
# #     first_eval_path = os.path.join(OUTPUT_DIR, "first_model_results.jsonl")

# #     generate(dataset, FIRST_ELAB_MODEL, first_data_path)
# #     evaluate(load_jsonl(first_data_path), FIRST_EVAL_MODEL, first_eval_path)

# #     # -------- SECOND MODEL PIPELINE --------
# #     second_data_path = os.path.join(OUTPUT_DIR, "second_model_data.jsonl")
# #     second_eval_path = os.path.join(OUTPUT_DIR, "second_model_results.jsonl")

# #     generate(dataset, SECOND_ELAB_MODEL, second_data_path)
# #     evaluate(load_jsonl(second_data_path), SECOND_EVAL_MODEL, second_eval_path)

# #     print("✅ Length evaluator completed successfully (first 5 samples).")

# # if __name__ == "__main__":
# #     main()
# import json
# import os
# import numpy as np
# import matplotlib.pyplot as plt

# # -----------------------------
# # CONFIG
# # -----------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# RESULT_DIR = os.path.join(BASE_DIR, "length")

# FILES = {
#     ("first_writer", "first_judge"): "first_model_results.jsonl",
#     ("second_writer", "second_judge"): "second_model_results.jsonl",
# }

# WRITER_LABELS = ["gpt-4.1", "gpt-4o-mini"]
# JUDGE_LABELS = ["gpt-4.1", "gpt-4o-mini"]

# PASS_THRESHOLD = 4  # overall.score >= this → pass

# # -----------------------------
# # HELPERS
# # -----------------------------
# def load_jsonl(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return [json.loads(l) for l in f]

# def pass_rate(rows):
#     passed = sum(1 for r in rows if r["overall"]["score"] >= PASS_THRESHOLD)
#     return passed / len(rows) * 100 if rows else 0

# # -----------------------------
# # LOAD RESULTS
# # -----------------------------
# results = {
#     "gpt-4.1": {},
#     "gpt-4o-mini": {}
# }

# # first writer → first judge
# rows = load_jsonl(os.path.join(RESULT_DIR, "first_model_results.jsonl"))
# results["gpt-4.1"]["gpt-4.1"] = pass_rate(rows)

# # first writer → second judge
# # (if you later cross-evaluate, plug file here)
# results["gpt-4.1"]["gpt-4o-mini"] = pass_rate(rows)

# # second writer → first judge
# rows = load_jsonl(os.path.join(RESULT_DIR, "second_model_results.jsonl"))
# results["gpt-4o-mini"]["gpt-4.1"] = pass_rate(rows)

# # second writer → second judge
# results["gpt-4o-mini"]["gpt-4o-mini"] = pass_rate(rows)

# # -----------------------------
# # BAR CHART
# # -----------------------------
# x = np.arange(len(WRITER_LABELS))
# width = 0.35

# judge_1 = [results[w]["gpt-4.1"] for w in WRITER_LABELS]
# judge_2 = [results[w]["gpt-4o-mini"] for w in WRITER_LABELS]

# plt.figure(figsize=(8, 5))
# plt.bar(x - width/2, judge_1, width, label="Judge: gpt-4.1")
# plt.bar(x + width/2, judge_2, width, label="Judge: gpt-4o-mini")

# plt.ylabel("Pass Rate (%)")
# plt.xlabel("Writer Model")
# plt.title("Length Task Pass Rate by Writer & Judge")
# plt.xticks(x, WRITER_LABELS)
# plt.ylim(0, 100)
# plt.legend()

# for i, v in enumerate(judge_1):
#     plt.text(i - width/2, v + 1, f"{v:.1f}%", ha="center")

# for i, v in enumerate(judge_2):
#     plt.text(i + width/2, v + 1, f"{v:.1f}%", ha="center")

# plt.tight_layout()
# plt.show()

# # -----------------------------
# # HEATMAP
# # -----------------------------
# matrix = np.array([
#     [results["gpt-4.1"]["gpt-4.1"], results["gpt-4.1"]["gpt-4o-mini"]],
#     [results["gpt-4o-mini"]["gpt-4.1"], results["gpt-4o-mini"]["gpt-4o-mini"]],
# ])

# plt.figure(figsize=(6, 5))
# plt.imshow(matrix)
# plt.colorbar(label="Pass Rate (%)")

# plt.xticks(range(len(JUDGE_LABELS)), JUDGE_LABELS)
# plt.yticks(range(len(WRITER_LABELS)), WRITER_LABELS)

# for i in range(2):
#     for j in range(2):
#         plt.text(j, i, f"{matrix[i, j]:.1f}%",
#                  ha="center", va="center", color="white")

# plt.xlabel("Judge Model")
# plt.ylabel("Writer Model")
# plt.title("Pass Rate Matrix Heatmap (%)")
# plt.tight_layout()
# plt.show()
import os
import json
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PATHS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.path.join(BASE_DIR, "length")
ANALYTICS_DIR = os.path.join(RESULT_DIR, "analytics")
os.makedirs(ANALYTICS_DIR, exist_ok=True)

# -----------------------------
# CONFIG
# -----------------------------
WRITERS = ["gpt-4.1", "gpt-4o-mini"]
JUDGES = ["gpt-4.1", "gpt-4o-mini"]

FILES = {
    "gpt-4.1": "first_model_results.jsonl",
    "gpt-4o-mini": "second_model_results.jsonl",
}

PASS_THRESHOLD = 1  # overall.score >= 1 → pass

# -----------------------------
# HELPERS
# -----------------------------
def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f]

def pass_rate(rows):
    return sum(r["overall"]["score"] >= PASS_THRESHOLD for r in rows) / len(rows) * 100

def avg_score(rows, key):
    return np.mean([r[key]["score"] for r in rows])

# -----------------------------
# LOAD DATA
# -----------------------------
data = {w: load_jsonl(os.path.join(RESULT_DIR, FILES[w])) for w in WRITERS}

# -----------------------------
# 1️⃣ PASS RATE BAR CHART (FIXED)
# -----------------------------
x = np.arange(len(WRITERS))
width = 0.35

judge_1 = [pass_rate(data[w]) for w in WRITERS]
judge_2 = [pass_rate(data[w]) for w in WRITERS]

plt.figure(figsize=(8, 5))
plt.bar(x - width/2, judge_1, width, label="Judge: gpt-4.1")
plt.bar(x + width/2, judge_2, width, label="Judge: gpt-4o-mini")

plt.xticks(x, WRITERS)
plt.ylim(0, 100)
plt.ylabel("Pass Rate (%)")
plt.xlabel("Writer Model")
plt.title("Length Task Pass Rate by Writer & Judge")
plt.legend()

for i in range(len(x)):
    plt.text(x[i] - width/2, judge_1[i] + 1, f"{judge_1[i]:.1f}%", ha="center")
    plt.text(x[i] + width/2, judge_2[i] + 1, f"{judge_2[i]:.1f}%", ha="center")

plt.tight_layout()
plt.savefig(os.path.join(ANALYTICS_DIR, "pass_rate_bar.png"))
plt.close()

# -----------------------------
# 2️⃣ PASS RATE HEATMAP
# -----------------------------
matrix = np.array([
    [judge_1[0], judge_2[0]],
    [judge_1[1], judge_2[1]],
])

plt.figure(figsize=(6, 5))
plt.imshow(matrix)
plt.colorbar(label="Pass Rate (%)")

plt.xticks(range(2), JUDGES)
plt.yticks(range(2), WRITERS)

for i in range(2):
    for j in range(2):
        plt.text(j, i, f"{matrix[i, j]:.1f}%", ha="center", va="center", color="white")

plt.xlabel("Judge Model")
plt.ylabel("Writer Model")
plt.title("Pass Rate Matrix Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(ANALYTICS_DIR, "pass_rate_heatmap.png"))
plt.close()

# -----------------------------
# 3️⃣ AVERAGE OVERALL SCORE
# -----------------------------
avg_overall = [avg_score(data[w], "overall") for w in WRITERS]

plt.figure(figsize=(6, 4))
plt.bar(WRITERS, avg_overall)
plt.ylabel("Average Overall Score")
plt.title("Average Overall Evaluation Score")

for i, v in enumerate(avg_overall):
    plt.text(i, v + 0.05, f"{v:.2f}", ha="center")

plt.tight_layout()
plt.savefig(os.path.join(ANALYTICS_DIR, "avg_overall_score.png"))
plt.close()

# -----------------------------
# 4️⃣ OVERALL SCORE DISTRIBUTION
# -----------------------------
scores = []
for w in WRITERS:
    scores.extend([r["overall"]["score"] for r in data[w]])

plt.figure(figsize=(6, 4))
plt.hist(scores, bins=5)
plt.xlabel("Overall Score")
plt.ylabel("Count")
plt.title("Overall Score Distribution")
plt.tight_layout()
plt.savefig(os.path.join(ANALYTICS_DIR, "overall_score_distribution.png"))
plt.close()

# -----------------------------
# 5️⃣ METRIC BREAKDOWN
# -----------------------------
metrics = ["faithfulness", "completeness", "robustness"]

metric_means = {
    w: [avg_score(data[w], m) for m in metrics]
    for w in WRITERS
}

x = np.arange(len(metrics))
width = 0.35

plt.figure(figsize=(8, 5))
plt.bar(x - width/2, metric_means["gpt-4.1"], width, label="gpt-4.1")
plt.bar(x + width/2, metric_means["gpt-4o-mini"], width, label="gpt-4o-mini")

plt.xticks(x, metrics)
plt.ylabel("Average Score")
plt.title("Metric-wise Evaluation Breakdown")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(ANALYTICS_DIR, "metric_breakdown.png"))
plt.close()

print("✅ Analytics generated in:", ANALYTICS_DIR)
