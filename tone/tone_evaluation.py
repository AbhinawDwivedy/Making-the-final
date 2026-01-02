# # # # import os
# # # # import json
# # # # import yaml
# # # # import asyncio
# # # # from openai import AsyncOpenAI
# # # # from dotenv import load_dotenv

# # # # # Load environment variables
# # # # load_dotenv(dotenv_path=".env", override=True)

# # # # # Configuration from env or defaults
# # # # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # # # OPENAI_FIRST_TONE_MODEL = os.getenv("OPENAI_FIRST_TONE_MODEL", "gpt-4o-mini")
# # # # OPENAI_SECOND_TONE_MODEL = os.getenv("OPENAI_SECOND_TONE_MODEL", "gpt-4.1")
# # # # OPENAI_FIRST_EVAL_MODEL = os.getenv("OPENAI_FIRST_EVAL_MODEL", "gpt-4.1")
# # # # OPENAI_SECOND_EVAL_MODEL = os.getenv("OPENAI_SECOND_EVAL_MODEL", "gpt-4o-mini")

# # # # DATA_FILE = "tone/tone_synthetic.jsonl"
# # # # PROMPTS_FILE = "tone/tone_prompts.yaml"
# # # # RESULTS_FILE = "tone/evaluation_results.json"

# # # # client = AsyncOpenAI(
# # # #     api_key=OPENAI_API_KEY,
# # # #     base_url=os.getenv("OPENAI_API_BASE")
# # # # )

# # # # def load_prompts():
# # # #     with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
# # # #         return yaml.safe_load(f)

# # # # def load_data():
# # # #     data = []
# # # #     with open(DATA_FILE, "r", encoding="utf-8") as f:
# # # #         for line in f:
# # # #             if line.strip():
# # # #                 data.append(json.loads(line))
# # # #     return data

# # # # async def generate_rewrite(model, prompt_system, prompt_user, email_content, target_tone):
# # # #     try:
# # # #         response = await client.chat.completions.create(
# # # #             model=model,
# # # #             messages=[
# # # #                 {"role": "system", "content": prompt_system},
# # # #                 {"role": "user", "content": prompt_user.format(tone=target_tone, selected_text=email_content)}
# # # #             ],
# # # #             temperature=0.7
# # # #         )
# # # #         return response.choices[0].message.content
# # # #     except Exception as e:
# # # #         print(f"Error generating rewrite with {model}: {e}")
# # # #         return None

# # # # async def evaluate_rewrite(model, prompt_system, prompt_user, original_email, edited_email):
# # # #     try:
# # # #         response = await client.chat.completions.create(
# # # #             model=model,
# # # #             messages=[
# # # #                 {"role": "system", "content": prompt_system},
# # # #                 {"role": "user", "content": prompt_user.format(original=original_email, edited=edited_email)}
# # # #             ],
# # # #             temperature=0.0,
# # # #             response_format={"type": "json_object"}
# # # #         )
# # # #         return json.loads(response.choices[0].message.content)
# # # #     except Exception as e:
# # # #         print(f"Error evaluating with {model}: {e}")
# # # #         return None

# # # # async def run_batch(data, prompts, generator_model, judge_model, results_dict):
# # # #     total_items = min(len(data), 75)
# # # #     print(f"\n--- Starting Batch: Generator={generator_model}, Judge={judge_model} ---")
    
# # # #     for i in range(total_items):
# # # #         item = data[i]
# # # #         item_id = item.get("id")
        
# # # #         # Determine tone based on index
# # # #         if i < 25:
# # # #             target_tone = "Professional"
# # # #         elif i < 50:
# # # #             target_tone = "Friendly"
# # # #         else:
# # # #             target_tone = "Sympathetic"

# # # #         original_content = item.get("content") or item.get("email")
# # # #         if not original_content:
# # # #             continue

# # # #         # Initialize result entry if not exists
# # # #         if item_id not in results_dict:
# # # #             results_dict[item_id] = {
# # # #                 "id": item_id,
# # # #                 "original_content": original_content,
# # # #                 "target_tone": target_tone,
# # # #                 "models": {}
# # # #             }

# # # #         print(f"Processing Item {i} (ID: {item_id}) - {target_tone}")

# # # #         # 1. Generate
# # # #         edited_content = await generate_rewrite(
# # # #             model=generator_model,
# # # #             prompt_system=prompts["tone"]["system"],
# # # #             prompt_user=prompts["tone"]["user"],
# # # #             email_content=original_content,
# # # #             target_tone=target_tone
# # # #         )

# # # #         if not edited_content:
# # # #             results_dict[item_id]["models"][generator_model] = {"error": "Generation failed"}
# # # #             continue

# # # #         # 2. Evaluate
# # # #         eval_result = await evaluate_rewrite(
# # # #             model=judge_model,
# # # #             prompt_system=prompts["evaluate"]["system"],
# # # #             prompt_user=prompts["evaluate"]["user"],
# # # #             original_email=original_content,
# # # #             edited_email=edited_content
# # # #         )

# # # #         # Store results
# # # #         results_dict[item_id]["models"][generator_model] = {
# # # #             "edited_content": edited_content,
# # # #             "evaluation": eval_result,
# # # #             "judge_model": judge_model
# # # #         }

# # # # def analyze_results(results_dict):
# # # #     metrics = {
# # # #         OPENAI_FIRST_TONE_MODEL: {"faithfulness": [], "completeness": [], "robustness": [], "overall": []},
# # # #         OPENAI_SECOND_TONE_MODEL: {"faithfulness": [], "completeness": [], "robustness": [], "overall": []}
# # # #     }

# # # #     observations = []

# # # #     for item_id, result in results_dict.items():
# # # #         for model_name, model_data in result["models"].items():
# # # #             if "error" in model_data:
# # # #                 continue
            
# # # #             eval_data = model_data.get("evaluation", {})
# # # #             if not eval_data:
# # # #                 continue

# # # #             for metric in ["faithfulness", "completeness", "robustness", "overall"]:
# # # #                 score = eval_data.get(metric, {}).get("score", 0)
# # # #                 metrics[model_name][metric].append(score)

# # # #     report_lines = []
# # # #     report_lines.append("# Tone Synthesis Evaluation Report")
# # # #     report_lines.append("\n## Quantitative Metrics")
# # # #     report_lines.append(f"Comparison between **{OPENAI_FIRST_TONE_MODEL}** and **{OPENAI_SECOND_TONE_MODEL}**.")
# # # #     report_lines.append("\n| Model | Avg Faithfulness | Avg Completeness | Avg Robustness | **Avg Overall** |")
# # # #     report_lines.append("|---|---|---|---|---|")

# # # #     winner = None
# # # #     best_score = -1

# # # #     for model_name, scores in metrics.items():
# # # #         if not scores["overall"]:
# # # #             report_lines.append(f"| {model_name} | N/A | N/A | N/A | N/A |")
# # # #             continue

# # # #         avg_f = sum(scores["faithfulness"]) / len(scores["faithfulness"])
# # # #         avg_c = sum(scores["completeness"]) / len(scores["completeness"])
# # # #         avg_r = sum(scores["robustness"]) / len(scores["robustness"])
# # # #         avg_o = sum(scores["overall"]) / len(scores["overall"])

# # # #         if avg_o > best_score:
# # # #             best_score = avg_o
# # # #             winner = model_name
        
# # # #         report_lines.append(f"| {model_name} | {avg_f:.2f} | {avg_c:.2f} | {avg_r:.2f} | **{avg_o:.2f}** |")

# # # #     report_lines.append(f"\n## Conclusion\nBased on the Average Overall Score, the winner is: **{winner}**")

# # # #     report_lines.append("\n## Qualitative Observations")
# # # #     report_lines.append("(This section would be populated by manual review or advanced extraction of 'reason' fields from the JSON logs. For now, please review 'tone/evaluation_results.json' for specific failure modes.)")
    
# # # #     # Simple error logging
# # # #     errors = []
# # # #     for item_id, result in results_dict.items():
# # # #         for model_name, model_data in result["models"].items():
# # # #             if "error" in model_data:
# # # #                 errors.append(f"Item {item_id} - {model_name}: {model_data['error']}")
    
# # # #     if errors:
# # # #         report_lines.append("\n### Technical Issues Identified")
# # # #         for err in errors:
# # # #             report_lines.append(f"- {err}")

# # # #     return "\n".join(report_lines)

# # # # async def main():
# # # #     prompts = load_prompts()
# # # #     data = load_data()
    
# # # #     # Ensure directory exists
# # # #     os.makedirs("tone", exist_ok=True)

# # # #     results_dict = {}
    
# # # #     # Load existing results to resume
# # # #     if os.path.exists(RESULTS_FILE):
# # # #         print(f"Resuming from {RESULTS_FILE}...")
# # # #         with open(RESULTS_FILE, "r", encoding="utf-8") as f:
# # # #             for line in f:
# # # #                 if line.strip():
# # # #                     item = json.loads(line)
# # # #                     results_dict[item["id"]] = item

# # # #     async def run_batch_incremental(data, prompts, generator_model, judge_model, results_dict):
# # # #         total_items = min(len(data), 75)
# # # #         print(f"\n--- Starting Batch: Generator={generator_model}, Judge={judge_model} ---")
        
# # # #         for i in range(total_items):
# # # #             item = data[i]
# # # #             item_id = item.get("id")
            
# # # #             # Init result if needed
# # # #             if item_id not in results_dict:
# # # #                  original_content = item.get("content") or item.get("email")
# # # #                  if not original_content: continue
                 
# # # #                  # Determine tone
# # # #                  if i < 25: target_tone = "Professional"
# # # #                  elif i < 50: target_tone = "Friendly"
# # # #                  else: target_tone = "Sympathetic"
                 
# # # #                  results_dict[item_id] = {
# # # #                     "id": item_id,
# # # #                     "original_content": original_content,
# # # #                     "target_tone": target_tone,
# # # #                     "models": {}
# # # #                 }

# # # #             # Check if this model pair is already done successfully
# # # #             if generator_model in results_dict[item_id]["models"]:
# # # #                 if "error" not in results_dict[item_id]["models"][generator_model]:
# # # #                     # Already processed successfully
# # # #                     continue
# # # #                 else:
# # # #                     print(f"Retrying Item {i} (ID: {item_id}) - {target_tone} for {generator_model} due to previous error.")

# # # #             target_tone = results_dict[item_id]["target_tone"]
# # # #             original_content = results_dict[item_id]["original_content"]

# # # #             print(f"Processing Item {i} (ID: {item_id}) - {target_tone}")

# # # #             # 1. Generate
# # # #             edited_content = await generate_rewrite(
# # # #                 model=generator_model,
# # # #                 prompt_system=prompts["tone"]["system"],
# # # #                 prompt_user=prompts["tone"]["user"],
# # # #                 email_content=original_content,
# # # #                 target_tone=target_tone
# # # #             )

# # # #             if not edited_content:
# # # #                 results_dict[item_id]["models"][generator_model] = {"error": "Generation failed"}
# # # #             else:
# # # #                 # 2. Evaluate
# # # #                 eval_result = await evaluate_rewrite(
# # # #                     model=judge_model,
# # # #                     prompt_system=prompts["evaluate"]["system"],
# # # #                     prompt_user=prompts["evaluate"]["user"],
# # # #                     original_email=original_content,
# # # #                     edited_email=edited_content
# # # #                 )

# # # #                 # Store result
# # # #                 results_dict[item_id]["models"][generator_model] = {
# # # #                     "edited_content": edited_content,
# # # #                     "evaluation": eval_result,
# # # #                     "judge_model": judge_model
# # # #                 }
            
# # # #             # Save IMMEDIATELY to file (append mode) logic is tricky because JSONL.
# # # #             # Easiest way to "update" a line in JSONL is hard. 
# # # #             # Actually, standard pattern is: valid JSONL has one object per line. If we just append freely, we might have duplicate IDs if we restart?
# # # #             # Better: Write to a temp file or just rewrite the whole file every N items? 
# # # #             # Or: append "updates" and compact later?
# # # #             # Let's rewrite the whole file every item for safety (performance hit negligible for 75 items).
            
# # # #             with open(RESULTS_FILE, "w", encoding="utf-8") as f:
# # # #                  sorted_ids = sorted(results_dict.keys(), key=lambda x: int(x) if isinstance(x, int) or x.isdigit() else x)
# # # #                  for uid in sorted_ids:
# # # #                      f.write(json.dumps(results_dict[uid]) + "\n")

# # # #     # Batch 1: Mini generates, 4.1 judges
# # # #     await run_batch_incremental(
# # # #         data, 
# # # #         prompts, 
# # # #         generator_model=OPENAI_FIRST_TONE_MODEL, 
# # # #         judge_model=OPENAI_FIRST_EVAL_MODEL, 
# # # #         results_dict=results_dict
# # # #     )

# # # #     # Batch 2: 4.1 generates, Mini judges
# # # #     await run_batch_incremental(
# # # #         data, 
# # # #         prompts, 
# # # #         generator_model=OPENAI_SECOND_TONE_MODEL, 
# # # #         judge_model=OPENAI_SECOND_EVAL_MODEL, 
# # # #         results_dict=results_dict
# # # #     )

# # # #     # Generate and write report
# # # #     print("\nGenerating report...")
# # # #     report_content = analyze_results(results_dict)
    
# # # #     with open("tone/tone_report.md", "w", encoding="utf-8") as f:
# # # #         f.write(report_content)
    
# # # #     print("Report generated: tone/tone_report.md")
# # # #     print("Evaluation complete.")

# # # # if __name__ == "__main__":
# # # #     asyncio.run(main())
# # # import os
# # # import json
# # # import yaml
# # # import asyncio
# # # from dotenv import load_dotenv
# # # from openai import AsyncOpenAI

# # # # --------------------------------------------------
# # # # ENV & CLIENT
# # # # --------------------------------------------------
# # # load_dotenv()

# # # client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # # GEN_MODEL_1 = os.getenv("OPENAI_FIRST_TONE_MODEL")
# # # GEN_MODEL_2 = os.getenv("OPENAI_SECOND_TONE_MODEL")
# # # JUDGE_MODEL_1 = os.getenv("OPENAI_FIRST_EVAL_MODEL")
# # # JUDGE_MODEL_2 = os.getenv("OPENAI_SECOND_EVAL_MODEL")

# # # DATA_FILE = "tone/tone_synthetic.jsonl"
# # # PROMPTS_FILE = "tone/tone_prompts.yaml"

# # # RESULTS_FILE = "tone/evaluation_results.jsonl"
# # # METRICS_FILE = "tone/evaluation_metrics.json"
# # # REPORT_FILE = "tone/evaluation_report.md"


# # # # --------------------------------------------------
# # # # LOADERS
# # # # --------------------------------------------------
# # # def load_data():
# # #     with open(DATA_FILE, "r", encoding="utf-8") as f:
# # #         return [json.loads(line) for line in f if line.strip()]

# # # def load_prompts():
# # #     with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
# # #         return yaml.safe_load(f)


# # # # --------------------------------------------------
# # # # CORE FUNCTIONS
# # # # --------------------------------------------------
# # # async def rewrite_email(model, system_prompt, user_prompt, email, target_tone):
# # #     response = await client.responses.create(
# # #         model=model,
# # #         input=[
# # #             {"role": "system", "content": system_prompt},
# # #             {
# # #                 "role": "user",
# # #                 "content": user_prompt.format(
# # #                     tone=target_tone,
# # #                     selected_text=email
# # #                 )
# # #             }
# # #         ],
# # #         temperature=0.7
# # #     )
# # #     return response.output_text


# # # async def judge_email(model, system_prompt, user_prompt, original, rewritten):
# # #     response = await client.responses.create(
# # #         model=model,
# # #         input=[
# # #             {"role": "system", "content": system_prompt},
# # #             {
# # #                 "role": "user",
# # #                 "content": user_prompt.format(
# # #                     original=original,
# # #                     edited=rewritten
# # #                 )
# # #             }
# # #         ],
# # #         temperature=0
# # #     )
# # #     return json.loads(response.output_text)


# # # # --------------------------------------------------
# # # # EVALUATION LOOP
# # # # --------------------------------------------------
# # # async def run_evaluation(generator_model, judge_model, data, prompts):
# # #     results = []

# # #     for idx, item in enumerate(data[:75]):
# # #         if idx < 25:
# # #             target_tone = "Professional"
# # #         elif idx < 50:
# # #             target_tone = "Friendly"
# # #         else:
# # #             target_tone = "Sympathetic"

# # #         rewritten = await rewrite_email(
# # #             generator_model,
# # #             prompts["tone"]["system"],
# # #             prompts["tone"]["user"],
# # #             item["content"],
# # #             target_tone
# # #         )

# # #         evaluation = await judge_email(
# # #             judge_model,
# # #             prompts["evaluate"]["system"],
# # #             prompts["evaluate"]["user"],
# # #             item["content"],
# # #             rewritten
# # #         )

# # #         results.append({
# # #             "id": item["id"],
# # #             "target_tone": target_tone,
# # #             "generator_model": generator_model,
# # #             "judge_model": judge_model,
# # #             "evaluation": evaluation
# # #         })

# # #     return results


# # # # --------------------------------------------------
# # # # METRICS & REPORT
# # # # --------------------------------------------------
# # # def compute_metrics(results):
# # #     metrics = {}

# # #     for r in results:
# # #         model = r["generator_model"]
# # #         metrics.setdefault(model, {"overall": []})
# # #         metrics[model]["overall"].append(
# # #             r["evaluation"]["overall"]["score"]
# # #         )

# # #     for model in metrics:
# # #         scores = metrics[model]["overall"]
# # #         metrics[model]["average_overall"] = sum(scores) / len(scores)

# # #     return metrics


# # # def write_report(metrics):
# # #     lines = [
# # #         "# Tone Evaluation Report\n",
# # #         "## Objective",
# # #         "Evaluate how well LLMs rewrite unprofessional emails into the intended tone.\n",
# # #         "## Observations"
# # #     ]

# # #     for model, data in metrics.items():
# # #         lines.append(
# # #             f"- **{model}** achieved an average overall score of **{data['average_overall']:.2f}**."
# # #         )

# # #     winner = max(metrics, key=lambda m: metrics[m]["average_overall"])
# # #     lines.append(
# # #         f"\n## Conclusion\nThe better performing model overall was **{winner}**."
# # #     )

# # #     with open(REPORT_FILE, "w", encoding="utf-8") as f:
# # #         f.write("\n".join(lines))


# # # # --------------------------------------------------
# # # # MAIN
# # # # --------------------------------------------------
# # # async def main():
# # #     data = load_data()
# # #     prompts = load_prompts()

# # #     all_results = []

# # #     all_results += await run_evaluation(
# # #         GEN_MODEL_1, JUDGE_MODEL_1, data, prompts
# # #     )

# # #     all_results += await run_evaluation(
# # #         GEN_MODEL_2, JUDGE_MODEL_2, data, prompts
# # #     )

# # #     with open(RESULTS_FILE, "w", encoding="utf-8") as f:
# # #         for r in all_results:
# # #             f.write(json.dumps(r) + "\n")

# # #     metrics = compute_metrics(all_results)

# # #     with open(METRICS_FILE, "w", encoding="utf-8") as f:
# # #         json.dump(metrics, f, indent=2)

# # #     write_report(metrics)

# # #     print("Tone evaluation complete.")


# # # if __name__ == "__main__":
# # #     asyncio.run(main())
# # import os
# # import json
# # import yaml
# # import asyncio
# # from collections import defaultdict
# # from dotenv import load_dotenv
# # from openai import AsyncOpenAI

# # # --------------------------------------------------
# # # ENV SETUP
# # # --------------------------------------------------
# # load_dotenv()

# # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

# # GEN_MODEL_1 = os.getenv("OPENAI_FIRST_TONE_MODEL", "gpt-4o-mini")
# # GEN_MODEL_2 = os.getenv("OPENAI_SECOND_TONE_MODEL", "gpt-4.1")

# # JUDGE_MODEL_1 = os.getenv("OPENAI_FIRST_EVAL_MODEL", "gpt-4.1")
# # JUDGE_MODEL_2 = os.getenv("OPENAI_SECOND_EVAL_MODEL", "gpt-4o-mini")

# # DATA_FILE = "tone/tone_synthetic.jsonl"
# # PROMPTS_FILE = "tone/tone_prompts.yaml"
# # RESULTS_FILE = "tone/tone_results.jsonl"
# # REPORT_FILE = "tone/tone_report.md"

# # client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

# # # --------------------------------------------------
# # # LOADERS
# # # --------------------------------------------------
# # def load_data():
# #     with open(DATA_FILE, "r", encoding="utf-8") as f:
# #         return [json.loads(line) for line in f if line.strip()]

# # def load_prompts():
# #     with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
# #         return yaml.safe_load(f)

# # def target_tone(index):
# #     if index < 25:
# #         return "Professional"
# #     elif index < 50:
# #         return "Friendly"
# #     return "Sympathetic"

# # # --------------------------------------------------
# # # LLM CALLS (SIMPLE & STABLE)
# # # --------------------------------------------------
# # async def rewrite_email(model, system_prompt, user_prompt, content, tone):
# #     res = await client.chat.completions.create(
# #         model=model,
# #         messages=[
# #             {"role": "system", "content": system_prompt},
# #             {
# #                 "role": "user",
# #                 "content": user_prompt.format(
# #                     selected_text=content,
# #                     tone=tone
# #                 )
# #             }
# #         ],
# #         temperature=0.7
# #     )
# #     return res.choices[0].message.content.strip()

# # async def judge_email(model, system_prompt, user_prompt, original, edited):
# #     res = await client.chat.completions.create(
# #         model=model,
# #         messages=[
# #             {"role": "system", "content": system_prompt},
# #             {
# #                 "role": "user",
# #                 "content": user_prompt.format(
# #                     original=original,
# #                     edited=edited
# #                 )
# #             }
# #         ],
# #         temperature=0,
# #         response_format={"type": "json_object"}
# #     )
# #     return json.loads(res.choices[0].message.content)

# # # --------------------------------------------------
# # # EVALUATION LOOP
# # # --------------------------------------------------
# # async def run_evaluation(gen_model, judge_model, data, prompts):
# #     results = []

# #     for i, item in enumerate(data[:75]):
# #         tone = target_tone(i)
# #         original = item["content"]

# #         rewritten = await rewrite_email(
# #             gen_model,
# #             prompts["tone"]["system"],
# #             prompts["tone"]["user"],
# #             original,
# #             tone
# #         )

# #         evaluation = await judge_email(
# #             judge_model,
# #             prompts["evaluate"]["system"],
# #             prompts["evaluate"]["user"],
# #             original,
# #             rewritten
# #         )

# #         correct = evaluation.get("overall", {}).get("score", 0) >= 3

# #         results.append({
# #             "id": item["id"],
# #             "target_tone": tone,
# #             "gen_model": gen_model,
# #             "judge_model": judge_model,
# #             "correct": correct,
# #             "scores": evaluation
# #         })

# #         print(f"[{gen_model} → {judge_model}] {i+1}/75 done")

# #     return results

# # # --------------------------------------------------
# # # REPORT GENERATION (AUTO, DATA-DRIVEN)
# # # --------------------------------------------------
# # def generate_report(results):
# #     tone_stats = defaultdict(lambda: {"correct": 0, "total": 0})
# #     gen_stats = defaultdict(lambda: {"correct": 0, "total": 0})
# #     judge_stats = defaultdict(lambda: {"yes": 0, "total": 0})

# #     for r in results:
# #         tone = r["target_tone"]
# #         gen = r["gen_model"]
# #         judge = r["judge_model"]

# #         tone_stats[tone]["total"] += 1
# #         gen_stats[gen]["total"] += 1
# #         judge_stats[judge]["total"] += 1

# #         if r["correct"]:
# #             tone_stats[tone]["correct"] += 1
# #             gen_stats[gen]["correct"] += 1
# #             judge_stats[judge]["yes"] += 1

# #     lines = []
# #     lines.append("# Tone Evaluation Report\n")

# #     lines.append("## Accuracy by Tone\n")
# #     for tone, s in tone_stats.items():
# #         acc = s["correct"] / s["total"]
# #         lines.append(f"- **{tone}**: {acc:.2%} ({s['correct']}/{s['total']})")

# #     lines.append("\n## Generator Model Comparison\n")
# #     for gen, s in gen_stats.items():
# #         acc = s["correct"] / s["total"]
# #         lines.append(f"- **{gen}**: {acc:.2%}")

# #     best_gen = max(gen_stats.items(), key=lambda x: x[1]["correct"] / x[1]["total"])
# #     lines.append(f"\n**Best Generator:** {best_gen[0]}")

# #     lines.append("\n## Judge Strictness\n")
# #     for judge, s in judge_stats.items():
# #         rate = s["yes"] / s["total"]
# #         lines.append(f"- **{judge}** approval rate: {rate:.2%}")

# #     strict = min(judge_stats.items(), key=lambda x: x[1]["yes"] / x[1]["total"])
# #     lenient = max(judge_stats.items(), key=lambda x: x[1]["yes"] / x[1]["total"])

# #     lines.append(f"\n- **Stricter Judge:** {strict[0]}")
# #     lines.append(f"- **More Lenient Judge:** {lenient[0]}")

# #     return "\n".join(lines)

# # # --------------------------------------------------
# # # MAIN
# # # --------------------------------------------------
# # async def main():
# #     os.makedirs("tone", exist_ok=True)

# #     data = load_data()
# #     prompts = load_prompts()

# #     all_results = []

# #     all_results += await run_evaluation(GEN_MODEL_1, JUDGE_MODEL_1, data, prompts)
# #     all_results += await run_evaluation(GEN_MODEL_2, JUDGE_MODEL_2, data, prompts)

# #     with open(RESULTS_FILE, "w", encoding="utf-8") as f:
# #         for r in all_results:
# #             f.write(json.dumps(r) + "\n")

# #     report = generate_report(all_results)
# #     with open(REPORT_FILE, "w", encoding="utf-8") as f:
# #         f.write(report)

# #     print("\nEvaluation complete.")
# #     print(f"- Results: {RESULTS_FILE}")
# #     print(f"- Report: {REPORT_FILE}")

# # if __name__ == "__main__":
# #     asyncio.run(main())
# import os
# import json
# import yaml
# import asyncio
# from collections import defaultdict
# from dotenv import load_dotenv
# from openai import AsyncOpenAI

# # --------------------------------------------------
# # ENV SETUP
# # --------------------------------------------------
# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

# GEN_MODEL_1 = os.getenv("OPENAI_FIRST_TONE_MODEL", "gpt-4o-mini")
# GEN_MODEL_2 = os.getenv("OPENAI_SECOND_TONE_MODEL", "gpt-4.1")

# JUDGE_MODEL_1 = os.getenv("OPENAI_FIRST_EVAL_MODEL", "gpt-4.1")
# JUDGE_MODEL_2 = os.getenv("OPENAI_SECOND_EVAL_MODEL", "gpt-4o-mini")

# DATA_FILE = "tone/tone_synthetic.jsonl"
# PROMPTS_FILE = "tone/tone_prompts.yaml"
# RESULTS_FILE = "tone/tone_results.jsonl"
# REPORT_FILE = "tone/tone_report.md"

# # 🔒 SAFE TEST LIMIT
# MAX_ITEMS = 10

# client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

# # --------------------------------------------------
# # LOADERS
# # --------------------------------------------------
# def load_data():
#     with open(DATA_FILE, "r", encoding="utf-8") as f:
#         return [json.loads(line) for line in f if line.strip()]

# def load_prompts():
#     with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
#         return yaml.safe_load(f)

# def target_tone(index):
#     if index < 3:
#         return "Professional"
#     elif index < 6:
#         return "Friendly"
#     return "Sympathetic"

# # --------------------------------------------------
# # LLM CALLS (STABLE)
# # --------------------------------------------------
# async def rewrite_email(model, system_prompt, user_prompt, content, tone):
#     res = await client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {
#                 "role": "user",
#                 "content": user_prompt.format(
#                     selected_text=content,
#                     tone=tone
#                 )
#             }
#         ],
#         temperature=0.7
#     )
#     return res.choices[0].message.content.strip()

# async def judge_email(model, system_prompt, user_prompt, original, edited):
#     res = await client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {
#                 "role": "user",
#                 "content": user_prompt.format(
#                     original=original,
#                     edited=edited
#                 )
#             }
#         ],
#         temperature=0,
#         response_format={"type": "json_object"}
#     )
#     return json.loads(res.choices[0].message.content)

# # --------------------------------------------------
# # EVALUATION LOOP (10 ITEMS ONLY)
# # --------------------------------------------------
# async def run_evaluation(gen_model, judge_model, data, prompts):
#     results = []

#     for i, item in enumerate(data[:MAX_ITEMS]):
#         tone = target_tone(i)
#         original = item["content"]

#         rewritten = await rewrite_email(
#             gen_model,
#             prompts["tone"]["system"],
#             prompts["tone"]["user"],
#             original,
#             tone
#         )

#         evaluation = await judge_email(
#             judge_model,
#             prompts["evaluate"]["system"],
#             prompts["evaluate"]["user"],
#             original,
#             rewritten
#         )

#         correct = evaluation.get("overall", {}).get("score", 0) >= 3

#         results.append({
#             "id": item["id"],
#             "target_tone": tone,
#             "gen_model": gen_model,
#             "judge_model": judge_model,
#             "correct": correct,
#             "scores": evaluation
#         })

#         print(f"[{gen_model} → {judge_model}] {i+1}/{MAX_ITEMS} done")

#     return results

# # --------------------------------------------------
# # REPORT (DATA-DRIVEN, NO MANUAL TEXT)
# # --------------------------------------------------
# def generate_report(results):
#     tone_stats = defaultdict(lambda: {"correct": 0, "total": 0})
#     gen_stats = defaultdict(lambda: {"correct": 0, "total": 0})

#     for r in results:
#         tone_stats[r["target_tone"]]["total"] += 1
#         gen_stats[r["gen_model"]]["total"] += 1

#         if r["correct"]:
#             tone_stats[r["target_tone"]]["correct"] += 1
#             gen_stats[r["gen_model"]]["correct"] += 1

#     lines = ["# Tone Evaluation Report (10-Sample Dry Run)\n"]

#     lines.append("## Accuracy by Tone")
#     for tone, s in tone_stats.items():
#         acc = s["correct"] / s["total"]
#         lines.append(f"- **{tone}**: {acc:.2%}")

#     lines.append("\n## Generator Accuracy")
#     for gen, s in gen_stats.items():
#         acc = s["correct"] / s["total"]
#         lines.append(f"- **{gen}**: {acc:.2%}")

#     return "\n".join(lines)

# # --------------------------------------------------
# # MAIN
# # --------------------------------------------------
# async def main():
#     os.makedirs("tone", exist_ok=True)

#     data = load_data()
#     prompts = load_prompts()

#     all_results = []
#     all_results += await run_evaluation(GEN_MODEL_1, JUDGE_MODEL_1, data, prompts)
#     all_results += await run_evaluation(GEN_MODEL_2, JUDGE_MODEL_2, data, prompts)

#     with open(RESULTS_FILE, "w", encoding="utf-8") as f:
#         for r in all_results:
#             f.write(json.dumps(r) + "\n")

#     report = generate_report(all_results)
#     with open(REPORT_FILE, "w", encoding="utf-8") as f:
#         f.write(report)

#     print("\n✅ DRY RUN COMPLETE (10 items)")
#     print(f"- Results: {RESULTS_FILE}")
#     print(f"- Report: {REPORT_FILE}")

# if __name__ == "__main__":
#     asyncio.run(main())
import os
import json
import yaml
import asyncio
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai import AsyncOpenAI

# --------------------------------------------------
# ENV SETUP
# --------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

GEN_MODEL_1 = os.getenv("OPENAI_FIRST_TONE_MODEL", "gpt-4o-mini")
GEN_MODEL_2 = os.getenv("OPENAI_SECOND_TONE_MODEL", "gpt-4.1")

JUDGE_MODEL_1 = os.getenv("OPENAI_FIRST_EVAL_MODEL", "gpt-4.1")
JUDGE_MODEL_2 = os.getenv("OPENAI_SECOND_EVAL_MODEL", "gpt-4o-mini")

DATA_FILE = "tone/tone_synthetic.jsonl"
PROMPTS_FILE = "tone/tone_prompts.yaml"
RESULTS_FILE = "tone/tone_results.jsonl"
REPORT_FILE = "tone/tone_report.md"
CSV_FILE = "tone/tone_results.csv"

MAX_ITEMS = 10

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE
)

# --------------------------------------------------
# LOADERS
# --------------------------------------------------
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def load_prompts():
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def target_tone(index):
    if index < 3:
        return "Professional"
    elif index < 6:
        return "Friendly"
    return "Sympathetic"

# --------------------------------------------------
# LLM CALLS (NEW SDK – FIXED)
# --------------------------------------------------
async def rewrite_email(model, system_prompt, user_prompt, content, tone):
    res = await client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_prompt.format(
                    selected_text=content,
                    tone=tone
                )
            }
        ],
        temperature=0.7
    )
    return res.output_text.strip()

async def judge_email(model, system_prompt, user_prompt, original, edited):
    res = await client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_prompt.format(
                    original=original,
                    edited=edited
                )
            }
        ],
        temperature=0
    )
    return json.loads(res.output_text)

# --------------------------------------------------
# EVALUATION LOOP
# --------------------------------------------------
async def run_evaluation(gen_model, judge_model, data, prompts):
    results = []

    for i, item in enumerate(data[:MAX_ITEMS]):
        tone = target_tone(i)
        original = item["content"]

        rewritten = await rewrite_email(
            gen_model,
            prompts["tone"]["system"],
            prompts["tone"]["user"],
            original,
            tone
        )

        evaluation = await judge_email(
            judge_model,
            prompts["evaluate"]["system"],
            prompts["evaluate"]["user"],
            original,
            rewritten
        )

        score = evaluation.get("overall", {}).get("score", 0)
        correct = score >= 3

        results.append({
            "id": item["id"],
            "target_tone": tone,
            "gen_model": gen_model,
            "judge_model": judge_model,
            "original": original,
            "rewritten": rewritten,
            "correct": correct,
            "scores": evaluation
        })

        print(f"[{gen_model} → {judge_model}] {i+1}/{MAX_ITEMS} done")

    return results

# --------------------------------------------------
# CSV + REPORT
# --------------------------------------------------
def save_csv(results):
    keys = ["id", "target_tone", "gen_model", "judge_model", "correct", "original", "rewritten", "scores"]
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in results:
            row = r.copy()
            row["scores"] = json.dumps(row["scores"])
            writer.writerow(row)

def generate_report(results):
    tone_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    gen_scores = defaultdict(list)
    judge_scores = defaultdict(list)

    for r in results:
        tone_stats[r["target_tone"]]["total"] += 1
        if r["correct"]:
            tone_stats[r["target_tone"]]["correct"] += 1

        gen_scores[r["gen_model"]].append(r["scores"]["overall"]["score"])
        judge_scores[r["judge_model"]].append(r["scores"]["overall"]["score"])

    lines = ["# Tone Evaluation Report\n"]

    lines.append("## Accuracy by Tone")
    for tone, s in tone_stats.items():
        acc = (s["correct"] / s["total"]) * 100
        lines.append(f"- **{tone}**: {acc:.1f}%")

    lines.append("\n## Average Score by Generation Model")
    for gen, scores in gen_scores.items():
        lines.append(f"- **{gen}**: {sum(scores)/len(scores):.2f}")

    lines.append("\n## Average Score by Judge Model")
    for judge, scores in judge_scores.items():
        lines.append(f"- **{judge}**: {sum(scores)/len(scores):.2f}")

    lines.append("\n## Results Table")
    lines.append("| ID | Tone | Gen | Judge | Correct | Score |")
    lines.append("|----|------|-----|-------|--------|-------|")

    for r in results:
        score = r["scores"]["overall"]["score"]
        lines.append(
            f"| {r['id']} | {r['target_tone']} | {r['gen_model']} | "
            f"{r['judge_model']} | {r['correct']} | {score} |"
        )

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return tone_stats, gen_scores, judge_scores

# --------------------------------------------------
# GRAPHS
# --------------------------------------------------
def plot_graphs(tone_stats, gen_scores, judge_scores):
    os.makedirs("tone", exist_ok=True)

    # Accuracy by tone
    plt.figure()
    tones = list(tone_stats.keys())
    accs = [(v["correct"]/v["total"])*100 for v in tone_stats.values()]
    plt.bar(tones, accs)
    plt.title("Accuracy by Tone")
    plt.ylabel("Accuracy (%)")
    plt.savefig("tone/accuracy_by_tone.png")
    plt.close()

    # Avg score by gen
    plt.figure()
    gens = list(gen_scores.keys())
    gen_avg = [sum(v)/len(v) for v in gen_scores.values()]
    plt.bar(gens, gen_avg)
    plt.title("Avg Score by Gen Model")
    plt.savefig("tone/avg_score_gen_model.png")
    plt.close()

    # Avg score by judge
    plt.figure()
    judges = list(judge_scores.keys())
    judge_avg = [sum(v)/len(v) for v in judge_scores.values()]
    plt.bar(judges, judge_avg)
    plt.title("Avg Score by Judge Model")
    plt.savefig("tone/avg_score_judge_model.png")
    plt.close()

# --------------------------------------------------
# MAIN
# --------------------------------------------------
async def main():
    os.makedirs("tone", exist_ok=True)

    data = load_data()
    prompts = load_prompts()

    all_results = []
    all_results += await run_evaluation(GEN_MODEL_1, JUDGE_MODEL_1, data, prompts)
    all_results += await run_evaluation(GEN_MODEL_2, JUDGE_MODEL_2, data, prompts)

    print("TOTAL RESULTS:", len(all_results))

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        for r in all_results:
            f.write(json.dumps(r) + "\n")

    save_csv(all_results)
    tone_stats, gen_scores, judge_scores = generate_report(all_results)
    plot_graphs(tone_stats, gen_scores, judge_scores)

    print("\n✅ DONE – results + report generated")

if __name__ == "__main__":
    asyncio.run(main())
