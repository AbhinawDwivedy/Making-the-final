# # # # # # import os
# # # # # # import json
# # # # # # import re
# # # # # # import yaml
# # # # # # from dotenv import load_dotenv
# # # # # # from openai import OpenAI
# # # # # # from tqdm import tqdm

# # # # # # load_dotenv()

# # # # # # # Load prompts
# # # # # # with open("url_prompts.yaml", "r", encoding="utf-8") as f:
# # # # # #     prompts = yaml.safe_load(f)


# # # # # # class URLEmailEditor:
# # # # # #     """Handles email editing operations (shorten, lengthen, tone)"""
    
# # # # # #     def __init__(self, model):
# # # # # #         self.client = OpenAI(
# # # # # #             api_key=os.getenv("OPENAI_API_KEY"),
# # # # # #             base_url=os.getenv("OPENAI_API_BASE")
# # # # # #         )
# # # # # #         self.model = model

# # # # # #     def _call_api(self, messages):
# # # # # #         r = self.client.chat.completions.create(
# # # # # #             model=self.model,
# # # # # #             messages=messages,
# # # # # #             temperature=0.7
# # # # # #         )
# # # # # #         return r.choices[0].message.content

# # # # # #     def edit_email(self, action, email_text, tone=None):
# # # # # #         """Apply editing action to email"""
# # # # # #         args = {
# # # # # #             "selected_text": email_text,
# # # # # #             "tone": tone if tone else ""
# # # # # #         }
        
# # # # # #         system = prompts[action]["system"].format(**args)
# # # # # #         user = prompts[action]["user"].format(**args)
        
# # # # # #         return self._call_api([
# # # # # #             {"role": "system", "content": system},
# # # # # #             {"role": "user", "content": user}
# # # # # #         ])


# # # # # # class URLEvaluator:
# # # # # #     """Evaluates URL preservation in edited emails"""
    
# # # # # #     def __init__(self, model):
# # # # # #         self.client = OpenAI(
# # # # # #             api_key=os.getenv("OPENAI_API_KEY"),
# # # # # #             base_url=os.getenv("OPENAI_API_BASE")
# # # # # #         )
# # # # # #         self.model = model

# # # # # #     def extract_urls(self, text):
# # # # # #         """Extract all URLs from text using regex"""
# # # # # #         url_pattern = r'https?://[^\s\)\]\>\,\;]+'
# # # # # #         urls = re.findall(url_pattern, text)
# # # # # #         return urls

# # # # # #     def evaluate(self, original, edited):
# # # # # #         """Evaluate URL preservation using LLM judge"""
# # # # # #         system = prompts["evaluate_comprehensive"]["system"]
# # # # # #         user = prompts["evaluate_comprehensive"]["user"].format(
# # # # # #             original=original,
# # # # # #             edited=edited
# # # # # #         )
        
# # # # # #         r = self.client.chat.completions.create(
# # # # # #             model=self.model,
# # # # # #             messages=[
# # # # # #                 {"role": "system", "content": system},
# # # # # #                 {"role": "user", "content": user}
# # # # # #             ],
# # # # # #             temperature=0
# # # # # #         )
        
# # # # # #         try:
# # # # # #             return json.loads(r.choices[0].message.content)
# # # # # #         except json.JSONDecodeError as e:
# # # # # #             print(f"⚠️  JSON parsing error: {e}")
# # # # # #             print(f"Raw response: {r.choices[0].message.content}")
# # # # # #             return None

# # # # # #     def simple_url_check(self, original, edited):
# # # # # #         """Simple programmatic URL preservation check"""
# # # # # #         original_urls = self.extract_urls(original)
# # # # # #         edited_urls = self.extract_urls(edited)
        
# # # # # #         missing = [url for url in original_urls if url not in edited_urls]
# # # # # #         extra = [url for url in edited_urls if url not in original_urls]
# # # # # #         preserved = [url for url in original_urls if url in edited_urls]
        
# # # # # #         preservation_rate = len(preserved) / len(original_urls) if original_urls else 1.0
        
# # # # # #         return {
# # # # # #             "original_url_count": len(original_urls),
# # # # # #             "edited_url_count": len(edited_urls),
# # # # # #             "preserved_count": len(preserved),
# # # # # #             "missing_count": len(missing),
# # # # # #             "preservation_rate": preservation_rate,
# # # # # #             "original_urls": original_urls,
# # # # # #             "edited_urls": edited_urls,
# # # # # #             "missing_urls": missing,
# # # # # #             "extra_urls": extra
# # # # # #         }


# # # # # # def main():
# # # # # #     import argparse
# # # # # #     parser = argparse.ArgumentParser(description="Evaluate URL preservation in email edits.")
# # # # # #     parser.add_argument("--input", default="url_dataset.jsonl", help="Input dataset file")
# # # # # #     parser.add_argument("--output", default="url_results.jsonl", help="Output results file")
# # # # # #     parser.add_argument("--model", default="gpt-4.1", help="Model to use for editing (gpt-4.1, gpt-4o-mini, etc.)")
# # # # # #     parser.add_argument("--eval-model", default=None, help="Model for evaluation (defaults to same as --model)")
# # # # # #     args = parser.parse_args()

# # # # # #     # Load dataset
# # # # # #     print(f"📂 Loading dataset from {args.input}...")
# # # # # #     dataset = []
# # # # # #     with open(args.input, "r", encoding="utf-8") as f:
# # # # # #         for line in f:
# # # # # #             dataset.append(json.loads(line))
    
# # # # # #     print(f"✅ Loaded {len(dataset)} samples\n")

# # # # # #     # Initialize editor and evaluator with specified models
# # # # # #     edit_model = args.model
# # # # # #     eval_model = args.eval_model if args.eval_model else args.model
    
# # # # # #     print(f"🤖 Editor Model: {edit_model}")
# # # # # #     print(f"⚖️  Evaluator Model: {eval_model}\n")
    
# # # # # #     editor = URLEmailEditor(edit_model)
# # # # # #     evaluator = URLEvaluator(eval_model)

# # # # # #     results = []
    
# # # # # #     print("🔄 Processing samples...\n")
    
# # # # # #     for sample in tqdm(dataset, desc="Evaluating", unit="email"):
# # # # # #         try:
# # # # # #             # Edit the email based on action
# # # # # #             action = sample["action"]
# # # # # #             tone = sample.get("tone_type")
            
# # # # # #             edited_email = editor.edit_email(
# # # # # #                 action,
# # # # # #                 sample["original_email"],
# # # # # #                 tone
# # # # # #             )
            
# # # # # #             # Evaluate URL preservation (LLM-based)
# # # # # #             llm_eval = evaluator.evaluate(
# # # # # #                 sample["original_email"],
# # # # # #                 edited_email
# # # # # #             )
            
# # # # # #             # Simple programmatic check
# # # # # #             simple_check = evaluator.simple_url_check(
# # # # # #                 sample["original_email"],
# # # # # #                 edited_email
# # # # # #             )
            
# # # # # #             result = {
# # # # # #                 "id": sample["id"],
# # # # # #                 "action": action,
# # # # # #                 "tone_type": tone,
# # # # # #                 "original_email": sample["original_email"],
# # # # # #                 "edited_email": edited_email,
# # # # # #                 "llm_evaluation": llm_eval,
# # # # # #                 "simple_check": simple_check
# # # # # #             }
            
# # # # # #             results.append(result)
            
# # # # # #             # Write incrementally
# # # # # #             with open(args.output, "a", encoding="utf-8") as f:
# # # # # #                 f.write(json.dumps(result, ensure_ascii=False) + "\n")
                
# # # # # #         except Exception as e:
# # # # # #             print(f"\n❌ Error processing sample {sample['id']}: {e}")
# # # # # #             continue

# # # # # #     print(f"\n✅ Evaluation complete → {args.output}")
    
# # # # # #     # Generate summary statistics
# # # # # #     print("\n" + "="*50)
# # # # # #     print("📊 SUMMARY STATISTICS")
# # # # # #     print("="*50)
    
# # # # # #     total = len(results)
    
# # # # # #     # By action
# # # # # #     action_stats = {}
# # # # # #     for result in results:
# # # # # #         action = result["action"]
# # # # # #         if action not in action_stats:
# # # # # #             action_stats[action] = {
# # # # # #                 "count": 0,
# # # # # #                 "perfect_preservation": 0,
# # # # # #                 "avg_url_preservation": 0,
# # # # # #                 "avg_overall": 0
# # # # # #             }
        
# # # # # #         action_stats[action]["count"] += 1
        
# # # # # #         if result["simple_check"]["preservation_rate"] == 1.0:
# # # # # #             action_stats[action]["perfect_preservation"] += 1
        
# # # # # #         if result["llm_evaluation"]:
# # # # # #             action_stats[action]["avg_url_preservation"] += result["llm_evaluation"]["url_preservation"]["score"]
# # # # # #             action_stats[action]["avg_overall"] += result["llm_evaluation"]["overall"]["score"]
    
# # # # # #     for action, stats in action_stats.items():
# # # # # #         count = stats["count"]
# # # # # #         print(f"\n{action.upper()}:")
# # # # # #         print(f"  Samples: {count}")
# # # # # #         print(f"  Perfect URL Preservation: {stats['perfect_preservation']}/{count} ({stats['perfect_preservation']/count*100:.1f}%)")
# # # # # #         if count > 0:
# # # # # #             print(f"  Avg URL Preservation Score: {stats['avg_url_preservation']/count:.2f}/5")
# # # # # #             print(f"  Avg Overall Score: {stats['avg_overall']/count:.2f}/5")
    
# # # # # #     print("\n" + "="*50)


# # # # # # if __name__ == "__main__":
# # # # # #     main()
# # # # # import os
# # # # # import json
# # # # # import yaml
# # # # # import pandas as pd
# # # # # import matplotlib.pyplot as plt
# # # # # import seaborn as sns
# # # # # from dotenv import load_dotenv
# # # # # from openai import OpenAI
# # # # # from tqdm import tqdm

# # # # # load_dotenv()

# # # # # # ======================================================
# # # # # # 1. SETUP & CONFIGURATION
# # # # # # ======================================================
# # # # # # Ensure prompts file exists
# # # # # if not os.path.exists("url_prompts.yaml"):
# # # # #     raise FileNotFoundError("❌ Missing 'url_prompts.yaml'. Please ensure this file is in the directory.")

# # # # # with open("url_prompts.yaml", "r", encoding="utf-8") as f:
# # # # #     PROMPTS = yaml.safe_load(f)

# # # # # def get_client():
# # # # #     return OpenAI(
# # # # #         api_key=os.getenv("OPENAI_API_KEY"),
# # # # #         base_url=os.getenv("OPENAI_API_BASE")
# # # # #     )

# # # # # # ======================================================
# # # # # # 2. EVALUATOR CLASS (THE JUDGE)
# # # # # # ======================================================
# # # # # class URLLLMEvaluator:
# # # # #     def __init__(self, model):
# # # # #         self.client = get_client()
# # # # #         self.model = model

# # # # #     def evaluate(self, original, edited):
# # # # #         system = PROMPTS["evaluate"]["system"]
# # # # #         user = PROMPTS["evaluate"]["user"].format(original=original, edited=edited)

# # # # #         try:
# # # # #             response = self.client.chat.completions.create(
# # # # #                 model=self.model,
# # # # #                 messages=[
# # # # #                     {"role": "system", "content": system},
# # # # #                     {"role": "user", "content": user}
# # # # #                 ],
# # # # #                 temperature=0
# # # # #             )
# # # # #             content = response.choices[0].message.content
# # # # #             return json.loads(content)
# # # # #         except Exception as e:
# # # # #             # Silently fail or log error so the loop continues
# # # # #             # print(f"⚠️ Error on sample: {e}") 
# # # # #             return None

# # # # # # ======================================================
# # # # # # 3. ANALYTICS ENGINE (CHARTS & REPORTS)
# # # # # # ======================================================
# # # # # class URLAnalytics:
# # # # #     def __init__(self, df):
# # # # #         self.df = df
# # # # #         self.output_dir = "analytics_output"
# # # # #         os.makedirs(self.output_dir, exist_ok=True)

# # # # #     def run_full_analysis(self):
# # # # #         """Orchestrates the generation of all visuals and text reports."""
# # # # #         print(f"\n📈 Starting Analytics Generation in '{self.output_dir}'...")
        
# # # # #         # Set visual style
# # # # #         sns.set_theme(style="whitegrid")
        
# # # # #         # 1. Generate Visuals
# # # # #         self._plot_action_performance()
# # # # #         self._plot_score_distribution()
# # # # #         self._plot_correlations()
        
# # # # #         # 2. Generate Text Report
# # # # #         self._save_markdown_report()
        
# # # # #         print(f"✅ Analytics Complete. Report saved to {self.output_dir}/summary_report.md")

# # # # #     def _plot_action_performance(self):
# # # # #         """Bar chart showing which actions break URLs the most."""
# # # # #         plt.figure(figsize=(12, 6))
# # # # #         sns.barplot(data=self.df, x="action", y="url_score", hue="judge_model", errorbar=None)
# # # # #         plt.title("URL Preservation Score by Email Action")
# # # # #         plt.ylabel("Avg Score (0-5)")
# # # # #         plt.xlabel("Action Type")
# # # # #         plt.xticks(rotation=45)
# # # # #         plt.tight_layout()
# # # # #         plt.savefig(f"{self.output_dir}/url_by_action.png")
# # # # #         plt.close()

# # # # #     def _plot_score_distribution(self):
# # # # #         """Density plot to see if judges are consistent (e.g., all 5s or mixed)."""
# # # # #         plt.figure(figsize=(10, 5))
# # # # #         for model in self.df["judge_model"].unique():
# # # # #             subset = self.df[self.df["judge_model"] == model]
# # # # #             # Handle cases with single value (no variance)
# # # # #             if len(subset) > 1 and subset["url_score"].nunique() > 1:
# # # # #                 sns.kdeplot(data=subset, x="url_score", label=model, fill=True, alpha=0.3)
# # # # #             else:
# # # # #                 # Fallback to histogram if KDE fails
# # # # #                 plt.hist(subset["url_score"], alpha=0.3, label=model, bins=5)
        
# # # # #         plt.title("URL Score Distribution (Consistency Check)")
# # # # #         plt.xlabel("Score")
# # # # #         plt.legend()
# # # # #         plt.savefig(f"{self.output_dir}/score_distribution.png")
# # # # #         plt.close()

# # # # #     def _plot_correlations(self):
# # # # #         """Heatmap to see if URL preservation links to other metrics."""
# # # # #         plt.figure(figsize=(8, 6))
# # # # #         cols = ["url_score", "faithfulness", "completeness", "overall"]
# # # # #         # Select only numeric columns that exist in DF
# # # # #         valid_cols = [c for c in cols if c in self.df.columns]
        
# # # # #         if len(valid_cols) > 1:
# # # # #             sns.heatmap(self.df[valid_cols].corr(), annot=True, cmap="YlGnBu", fmt=".2f")
# # # # #             plt.title("Metric Correlation Heatmap")
# # # # #             plt.tight_layout()
# # # # #             plt.savefig(f"{self.output_dir}/metric_correlation.png")
# # # # #         plt.close()

# # # # #     def _save_markdown_report(self):
# # # # #         """Writes the summary statistics to a Markdown file."""
# # # # #         # Define "Preserved" as score >= 4
# # # # #         self.df['preserved'] = self.df['url_score'] >= 4
# # # # #         pass_rates = self.df.groupby("judge_model")['preserved'].mean() * 100
        
# # # # #         # Identify weakest actions (risk analysis)
# # # # #         weakest = self.df.groupby("action")["url_score"].mean().sort_values().head(3)

# # # # #         # Build Report String
# # # # #         report = [
# # # # #             "# 🛡️ URL Preservation Analytics Report",
# # # # #             f"\n## 🎯 Pass Rate Summary (Score ≥ 4)",
# # # # #             "Percentage of emails where URLs were correctly preserved:",
# # # # #         ]
        
# # # # #         for model, rate in pass_rates.items():
# # # # #             report.append(f"- **{model}**: {rate:.1f}% passing")

# # # # #         report.append("\n## 📊 Mean Scores by Judge")
# # # # #         summary_table = self.df.groupby("judge_model")[["url_score", "faithfulness", "overall"]].mean()
# # # # #         report.append(summary_table.to_markdown())

# # # # #         report.append("\n## ⚠️ Risk Analysis")
# # # # #         report.append("The following actions are most likely to result in URL corruption:")
# # # # #         for action, score in weakest.items():
# # # # #             report.append(f"- **{action}**: (Average Score: {score:.2f})")
            
# # # # #         # Write to file
# # # # #         with open(f"{self.output_dir}/summary_report.md", "w", encoding="utf-8") as f:
# # # # #             f.write("\n".join(report))

# # # # # # ======================================================
# # # # # # 4. PIPELINE RUNNER
# # # # # # ======================================================
# # # # # def run_evaluation_pipeline(input_file, tasks):
# # # # #     """
# # # # #     Runs the LLM evaluation for each model in 'tasks' and returns a unified DataFrame.
# # # # #     """
# # # # #     all_rows = []
    
# # # # #     # Load input data
# # # # #     with open(input_file, "r", encoding="utf-8") as f:
# # # # #         samples = [json.loads(line) for line in f]

# # # # #     # Iterate through models (Sequential Execution)
# # # # #     for model_name, output_path in tasks:
# # # # #         print(f"\n⚖️  Evaluating with judge: {model_name}")
# # # # #         evaluator = URLLLMEvaluator(model_name)
        
# # # # #         current_model_rows = []
        
# # # # #         # Run inference loop
# # # # #         for sample in tqdm(samples, desc=f"Processing {model_name}"):
# # # # #             eval_result = evaluator.evaluate(
# # # # #                 sample["original_email"],
# # # # #                 sample["edited_email"]
# # # # #             )
            
# # # # #             if eval_result:
# # # # #                 record = {
# # # # #                     "id": sample["id"],
# # # # #                     "action": sample["action"],
# # # # #                     "gen_model": sample["model"],
# # # # #                     "judge_model": model_name,
# # # # #                     # Safely get nested scores, default to 0 if missing
# # # # #                     "url_score": eval_result.get("url_preservation", {}).get("score", 0),
# # # # #                     "faithfulness": eval_result.get("faithfulness", {}).get("score", 0),
# # # # #                     "completeness": eval_result.get("completeness", {}).get("score", 0),
# # # # #                     "overall": eval_result.get("overall", {}).get("score", 0)
# # # # #                 }
# # # # #                 current_model_rows.append(record)
# # # # #                 all_rows.append(record)

# # # # #         # Save individual JSONL results for safety
# # # # #         with open(output_path, "w", encoding="utf-8") as out:
# # # # #             for r in current_model_rows:
# # # # #                 out.write(json.dumps(r) + "\n")
                
# # # # #     return pd.DataFrame(all_rows)

# # # # # # ======================================================
# # # # # # 5. MAIN EXECUTION
# # # # # # ======================================================
# # # # # def main():
# # # # #     INPUT_FILE = "edited_emails.jsonl"
    
# # # # #     # Define your judges here. 
# # # # #     # It will run 4.1 first, finish it, then run mini.
# # # # #     evaluation_tasks = [
# # # # #         ("gpt-4.1", "results_41.jsonl"),
# # # # #         ("gpt-4o-mini", "results_mini.jsonl")
# # # # #     ]

# # # # #     # 1. Run Evaluation
# # # # #     if not os.path.exists(INPUT_FILE):
# # # # #         print(f"❌ Error: Input file '{INPUT_FILE}' not found.")
# # # # #         return

# # # # #     final_df = run_evaluation_pipeline(INPUT_FILE, evaluation_tasks)

# # # # #     if final_df.empty:
# # # # #         print("❌ No results generated. Check API keys or input file.")
# # # # #         return

# # # # #     # 2. Save Combined Metrics CSV
# # # # #     csv_filename = "final_metrics_data.csv"
# # # # #     final_df.to_csv(csv_filename, index=False)
# # # # #     print(f"\n💾 Raw data saved to '{csv_filename}'")

# # # # #     # 3. Trigger Analytics
# # # # #     analytics = URLAnalytics(final_df)
# # # # #     analytics.run_full_analysis()

# # # # # if __name__ == "__main__":
# # # # #     main()
# # # # import os
# # # # import json
# # # # import yaml
# # # # import pandas as pd
# # # # import matplotlib.pyplot as plt
# # # # import seaborn as sns
# # # # from dotenv import load_dotenv
# # # # from openai import OpenAI
# # # # from tqdm import tqdm

# # # # load_dotenv()

# # # # # ======================================================
# # # # # 0. CONFIG & PATHS
# # # # # ======================================================
# # # # BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # # # FILES = {
# # # #     # INPUT: Your raw dataset
# # # #     "raw_dataset": os.path.join(BASE_DIR, "url_dataset_ai_randomized.jsonl"),
    
# # # #     # CONFIG: Prompts
# # # #     "prompts": os.path.join(BASE_DIR, "same_prompts.yaml"),
    
# # # #     # OUTPUTS: Where we save things
# # # #     "edited_output": os.path.join(BASE_DIR, "edited_emails_generated.jsonl"),
# # # #     "results_41": os.path.join(BASE_DIR, "results_41.jsonl"),
# # # #     "results_mini": os.path.join(BASE_DIR, "results_mini.jsonl"),
# # # #     "final_csv": os.path.join(BASE_DIR, "final_metrics_data.csv"),
# # # #     "analytics_dir": os.path.join(BASE_DIR, "analytics_output")
# # # # }

# # # # # Ensure prompts exist
# # # # if not os.path.exists(FILES["prompts"]):
# # # #     print("⚠️ Error: 'url_prompts.yaml' not found in this folder.")
# # # #     exit()

# # # # with open(FILES["prompts"], "r", encoding="utf-8") as f:
# # # #     PROMPTS = yaml.safe_load(f)

# # # # def get_client():
# # # #     return OpenAI(
# # # #         api_key=os.getenv("OPENAI_API_KEY"),
# # # #         base_url=os.getenv("OPENAI_API_BASE")
# # # #     )

# # # # # ======================================================
# # # # # STAGE 1: GENERATE EDITED EMAILS (The Fix)
# # # # # ======================================================
# # # # def ensure_edited_data_exists():
# # # #     """
# # # #     Checks if we have edited emails. If not, it generates them 
# # # #     from 'url_dataset_ai_randomized.jsonl'.
# # # #     """
# # # #     if os.path.exists(FILES["edited_output"]):
# # # #         print(f"✅ Found existing edited data: {FILES['edited_output']}")
# # # #         return

# # # #     print(f"⚡ Generating edited emails from: {FILES['raw_dataset']}")
    
# # # #     if not os.path.exists(FILES["raw_dataset"]):
# # # #         print(f"❌ Error: Raw dataset '{FILES['raw_dataset']}' not found!")
# # # #         exit()

# # # #     client = get_client()
    
# # # #     # System prompt for rewriting (you can tweak this)
# # # #     SYSTEM_PROMPT = "You are an AI assistant. Rewrite the user's email to be more professional and concise. IMPORTANT: You must preserve all URLs exactly as they appear in the original text."

# # # #     with open(FILES["raw_dataset"], "r", encoding="utf-8") as f_in, \
# # # #          open(FILES["edited_output"], "w", encoding="utf-8") as f_out:
        
# # # #         lines = f_in.readlines()
        
# # # #         for line in tqdm(lines, desc="Generating Edits"):
# # # #             data = json.loads(line)
# # # #             original = data.get("content", "")
            
# # # #             if not original: continue

# # # #             try:
# # # #                 # Call LLM to rewrite the email
# # # #                 response = client.chat.completions.create(
# # # #                     model="gpt-4o-mini",  # Using Mini for speed/cost
# # # #                     messages=[
# # # #                         {"role": "system", "content": SYSTEM_PROMPT},
# # # #                         {"role": "user", "content": original}
# # # #                     ],
# # # #                     temperature=0.7
# # # #                 )
# # # #                 edited_content = response.choices[0].message.content

# # # #                 # Save the pair (Original + Edited)
# # # #                 record = {
# # # #                     "id": data.get("id", "unknown"),
# # # #                     "action": data.get("action", "rewrite"), # Default action if missing
# # # #                     "model": "gpt-4o-mini",
# # # #                     "original_email": original,
# # # #                     "edited_email": edited_content
# # # #                 }
# # # #                 f_out.write(json.dumps(record) + "\n")
            
# # # #             except Exception as e:
# # # #                 print(f"⚠️ Failed to generate edit for ID {data.get('id')}: {e}")

# # # #     print("✅ Generation complete. Proceeding to evaluation...")

# # # # # ======================================================
# # # # # STAGE 2: EVALUATION LOOP
# # # # # ======================================================
# # # # class URLLLMEvaluator:
# # # #     def __init__(self, model):
# # # #         self.client = get_client()
# # # #         self.model = model

# # # #     def evaluate(self, original, edited):
# # # #         system = PROMPTS["evaluate"]["system"]
# # # #         user = PROMPTS["evaluate"]["user"].format(original=original, edited=edited)

# # # #         try:
# # # #             response = self.client.chat.completions.create(
# # # #                 model=self.model,
# # # #                 messages=[
# # # #                     {"role": "system", "content": system},
# # # #                     {"role": "user", "content": user}
# # # #                 ],
# # # #                 temperature=0
# # # #             )
# # # #             content = response.choices[0].message.content
# # # #             # Clean up potential markdown formatting from LLM response
# # # #             if content.startswith("```"):
# # # #                 content = content.replace("```json", "").replace("```", "")
# # # #             return json.loads(content)
# # # #         except Exception:
# # # #             return None

# # # # def run_evaluation_pipeline(tasks):
# # # #     all_rows = []
    
# # # #     # Load the newly generated data
# # # #     with open(FILES["edited_output"], "r", encoding="utf-8") as f:
# # # #         samples = [json.loads(line) for line in f]

# # # #     for model_name, output_path in tasks:
# # # #         print(f"\n⚖️  Evaluating with Judge: {model_name}")
# # # #         evaluator = URLLLMEvaluator(model_name)
        
# # # #         with open(output_path, "w", encoding="utf-8") as out:
# # # #             for sample in tqdm(samples, desc=f"Judging {model_name}"):
# # # #                 eval_result = evaluator.evaluate(
# # # #                     sample["original_email"],
# # # #                     sample["edited_email"]
# # # #                 )
                
# # # #                 if eval_result:
# # # #                     record = {
# # # #                         "id": sample["id"],
# # # #                         "action": sample["action"],
# # # #                         "judge_model": model_name,
# # # #                         "url_score": eval_result.get("url_preservation", {}).get("score", 0),
# # # #                         "faithfulness": eval_result.get("faithfulness", {}).get("score", 0),
# # # #                         "overall": eval_result.get("overall", {}).get("score", 0)
# # # #                     }
# # # #                     all_rows.append(record)
# # # #                     out.write(json.dumps(record) + "\n")
    
# # # #     return pd.DataFrame(all_rows)

# # # # # ======================================================
# # # # # STAGE 3: ANALYTICS
# # # # # ======================================================
# # # # class URLAnalytics:
# # # #     def __init__(self, df):
# # # #         self.df = df
# # # #         self.output_dir = FILES["analytics_dir"]
# # # #         os.makedirs(self.output_dir, exist_ok=True)

# # # #     def run_full_analysis(self):
# # # #         print(f"\n📈 Generating Analytics in '{self.output_dir}'...")
# # # #         sns.set_theme(style="whitegrid")
        
# # # #         # 1. Bar Chart
# # # #         plt.figure(figsize=(10, 6))
# # # #         sns.barplot(data=self.df, x="action", y="url_score", hue="judge_model", errorbar=None)
# # # #         plt.title("URL Preservation by Action")
# # # #         plt.tight_layout()
# # # #         plt.savefig(os.path.join(self.output_dir, "url_by_action.png"))
# # # #         plt.close()

# # # #         # 2. Markdown Report
# # # #         self.df['preserved'] = self.df['url_score'] >= 4
# # # #         pass_rates = self.df.groupby("judge_model")['preserved'].mean() * 100
        
# # # #         report = ["# 🛡️ URL Preservation Report\n"]
# # # #         report.append("## 🎯 Pass Rates (Score >= 4)")
# # # #         for model, rate in pass_rates.items():
# # # #             report.append(f"- **{model}**: {rate:.1f}%")

# # # #         report.append("\n## 📊 Data Summary")
# # # #         report.append(self.df.groupby("judge_model")[["url_score", "faithfulness"]].mean().to_markdown())

# # # #         with open(os.path.join(self.output_dir, "summary_report.md"), "w", encoding="utf-8") as f:
# # # #             f.write("\n".join(report))
            
# # # #         print("✅ Analytics generated.")

# # # # # ======================================================
# # # # # MAIN
# # # # # ======================================================
# # # # def main():
# # # #     # 1. Generate edits if they don't exist
# # # #     ensure_edited_data_exists()

# # # #     # 2. Run Judges
# # # #     tasks = [
# # # #         ("gpt-4.1", FILES["results_41"]),
# # # #         ("gpt-4o-mini", FILES["results_mini"])
# # # #     ]
# # # #     final_df = run_evaluation_pipeline(tasks)

# # # #     # 3. Analytics
# # # #     if not final_df.empty:
# # # #         final_df.to_csv(FILES["final_csv"], index=False)
# # # #         analytics = URLAnalytics(final_df)
# # # #         analytics.run_full_analysis()
# # # #     else:
# # # #         print("❌ No results found.")

# # # # if __name__ == "__main__":
# # # #     main()
# # # import os
# # # import json
# # # import yaml
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # import seaborn as sns
# # # from dotenv import load_dotenv
# # # from openai import OpenAI
# # # from tqdm import tqdm

# # # load_dotenv()

# # # # ======================================================
# # # # 0. CONFIG & PATHS
# # # # ======================================================
# # # BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # # FILES = {
# # #     "raw_dataset": os.path.join(BASE_DIR, "url_dataset_ai_randomized.jsonl"),
# # #     "prompts": os.path.join(BASE_DIR, "same_prompts.yaml"),  # Your specific prompt file
    
# # #     # GENERATION OUTPUTS
# # #     "edited_by_mini": os.path.join(BASE_DIR, "edited_by_mini.jsonl"),
# # #     "edited_by_41": os.path.join(BASE_DIR, "edited_by_41.jsonl"),
    
# # #     # EVALUATION OUTPUTS
# # #     "results_mini_judges_41": os.path.join(BASE_DIR, "results_mini_judges_41.jsonl"),
# # #     "results_41_judges_mini": os.path.join(BASE_DIR, "results_41_judges_mini.jsonl"),
    
# # #     # ANALYTICS OUTPUTS
# # #     "final_csv": os.path.join(BASE_DIR, "cross_eval_metrics.csv"),
# # #     "analytics_dir": os.path.join(BASE_DIR, "analytics_output")
# # # }

# # # # Ensure prompts exist
# # # if not os.path.exists(FILES["prompts"]):
# # #     print(f"❌ Error: '{FILES['prompts']}' not found. Please ensure the file exists.")
# # #     exit()

# # # with open(FILES["prompts"], "r", encoding="utf-8") as f:
# # #     PROMPTS = yaml.safe_load(f)

# # # def get_client():
# # #     return OpenAI(
# # #         api_key=os.getenv("OPENAI_API_KEY"),
# # #         base_url=os.getenv("OPENAI_API_BASE")
# # #     )

# # # # ======================================================
# # # # STAGE 1: GENERATION (The Writers)
# # # # ======================================================
# # # def generate_dataset(writer_model, output_file):
# # #     """
# # #     Generates edited emails using 'writer_model' and saves to 'output_file'.
# # #     Skipped if file already exists to save time/cost.
# # #     """
# # #     if os.path.exists(output_file):
# # #         print(f"✅ Found existing data by {writer_model}: {output_file}")
# # #         return

# # #     print(f"✍️  {writer_model} is writing emails now...")
    
# # #     if not os.path.exists(FILES["raw_dataset"]):
# # #         print(f"❌ Error: Raw dataset missing at {FILES['raw_dataset']}")
# # #         exit()

# # #     client = get_client()
# # #     SYSTEM_PROMPT = "You are an AI assistant. Rewrite the email to be professional. IMPORTANT: Preserve all URLs exactly."

# # #     with open(FILES["raw_dataset"], "r", encoding="utf-8") as f_in, \
# # #          open(output_file, "w", encoding="utf-8") as f_out:
        
# # #         lines = f_in.readlines()
# # #         for line in tqdm(lines, desc=f"Writing ({writer_model})"):
# # #             data = json.loads(line)
# # #             original = data.get("content", "")
            
# # #             if not original: continue

# # #             try:
# # #                 # Note: Adjust model name if your API expects specific versions
# # #                 response = client.chat.completions.create(
# # #                     model=writer_model,
# # #                     messages=[
# # #                         {"role": "system", "content": SYSTEM_PROMPT},
# # #                         {"role": "user", "content": original}
# # #                     ],
# # #                     temperature=0.7
# # #                 )
# # #                 edited_content = response.choices[0].message.content

# # #                 record = {
# # #                     "id": data.get("id"),
# # #                     "action": data.get("action", "rewrite"),
# # #                     "writer_model": writer_model,
# # #                     "original_email": original,
# # #                     "edited_email": edited_content
# # #                 }
# # #                 f_out.write(json.dumps(record) + "\n")
            
# # #             except Exception as e:
# # #                 print(f"⚠️ Write error for {writer_model}: {e}")

# # # # ======================================================
# # # # STAGE 2: EVALUATION (The Judges)
# # # # ======================================================
# # # class URLLLMEvaluator:
# # #     def __init__(self, model):
# # #         self.client = get_client()
# # #         self.model = model

# # #     def evaluate(self, original, edited):
# # #         if "evaluate" not in PROMPTS:
# # #             print("❌ Error: 'evaluate' key missing in prompt yaml.")
# # #             return None
            
# # #         system = PROMPTS["evaluate"]["system"]
# # #         user = PROMPTS["evaluate"]["user"].format(original=original, edited=edited)

# # #         try:
# # #             response = self.client.chat.completions.create(
# # #                 model=self.model,
# # #                 messages=[
# # #                     {"role": "system", "content": system},
# # #                     {"role": "user", "content": user}
# # #                 ],
# # #                 temperature=0
# # #             )
# # #             content = response.choices[0].message.content
# # #             # Cleanup markdown if present
# # #             if content.startswith("```"):
# # #                 content = content.replace("```json", "").replace("```", "")
# # #             return json.loads(content)
# # #         except Exception:
# # #             return None

# # # def run_cross_evaluation():
# # #     all_rows = []
    
# # #     # PAIR CONFIGURATION: (Input File, Judge Model, Output File)
# # #     tasks = [
# # #         # Pair A: 4.1 Writes -> Mini Judges
# # #         (FILES["edited_by_41"],   "gpt-4o-mini", FILES["results_mini_judges_41"]),
        
# # #         # Pair B: Mini Writes -> 4.1 Judges
# # #         (FILES["edited_by_mini"], "gpt-4.1",     FILES["results_41_judges_mini"])
# # #     ]

# # #     for input_path, judge_model, output_path in tasks:
# # #         # Infer writer from filename for labeling
# # #         writer_model = "gpt-4.1" if "41" in input_path else "gpt-4o-mini"
        
# # #         # Create a clean label for charts
# # #         pair_label = f"Writer: {writer_model}\nJudge: {judge_model}"
        
# # #         print(f"\n⚖️  Running Pair: {pair_label.replace('\n', ' -> ')}")
        
# # #         if not os.path.exists(input_path):
# # #             print(f"⚠️ Warning: Input file {input_path} missing. Skipping this pair.")
# # #             continue

# # #         evaluator = URLLLMEvaluator(judge_model)
        
# # #         with open(input_path, "r", encoding="utf-8") as f_in, \
# # #              open(output_path, "w", encoding="utf-8") as f_out:
            
# # #             samples = [json.loads(line) for line in f_in]
            
# # #             for sample in tqdm(samples, desc="Judging"):
# # #                 eval_result = evaluator.evaluate(
# # #                     sample["original_email"],
# # #                     sample["edited_email"]
# # #                 )
                
# # #                 if eval_result:
# # #                     record = {
# # #                         "id": sample.get("id"),
# # #                         "action": sample.get("action", "unknown"),
# # #                         "writer_model": writer_model,
# # #                         "judge_model": judge_model,
# # #                         "pair_name": pair_label,
# # #                         "url_score": eval_result.get("url_preservation", {}).get("score", 0),
# # #                         "faithfulness": eval_result.get("faithfulness", {}).get("score", 0),
# # #                         "overall": eval_result.get("overall", {}).get("score", 0)
# # #                     }
# # #                     all_rows.append(record)
# # #                     f_out.write(json.dumps(record) + "\n")
    
# # #     return pd.DataFrame(all_rows)

# # # # ======================================================
# # # # STAGE 3: ADVANCED ANALYTICS (Expanded)
# # # # ======================================================
# # # class URLAnalytics:
# # #     def __init__(self, df):
# # #         self.df = df
# # #         self.output_dir = FILES["analytics_dir"]
# # #         os.makedirs(self.output_dir, exist_ok=True)
        
# # #         # Define Pass criteria (Score >= 4)
# # #         self.df['passed'] = self.df['url_score'] >= 4

# # #     def run_full_analysis(self):
# # #         print(f"\n📈 Generating Advanced Analytics in '{self.output_dir}'...")
# # #         sns.set_theme(style="whitegrid")
        
# # #         # 1. Main Pass Rate Comparison (Bar Chart)
# # #         self.plot_pass_rate_comparison()
        
# # #         # 2. Score Distribution (Violin Plot)
# # #         self.plot_score_distribution()
        
# # #         # 3. Failure Analysis Heatmap (Writer vs Action)
# # #         self.plot_failure_heatmap()
        
# # #         # 4. Correlation Plot (Faithfulness vs URL Score)
# # #         self.plot_correlation()

# # #         # 5. Generate Text Report
# # #         self._generate_markdown_report()
# # #         print("✅ Analytics generated.")

# # #     def plot_pass_rate_comparison(self):
# # #         """Generates a bar chart showing % of safe URLs for each pair."""
# # #         plt.figure(figsize=(8, 6))
        
# # #         # Group by pair and calculate mean of boolean 'passed'
# # #         pass_data = self.df.groupby("pair_name")['passed'].mean().reset_index()
# # #         pass_data['passed'] *= 100  # Convert to percentage
        
# # #         ax = sns.barplot(
# # #             data=pass_data, 
# # #             x="pair_name", 
# # #             y="passed", 
# # #             hue="pair_name",
# # #             palette="viridis",
# # #             legend=False
# # #         )
        
# # #         # Add labels on bars
# # #         for container in ax.containers:
# # #             ax.bar_label(container, fmt='%.1f%%', padding=3, fontsize=12, weight='bold')
            
# # #         plt.title("URL Safety Pass Rate (Score >= 4)", fontsize=14)
# # #         plt.ylabel("Pass Rate (%)")
# # #         plt.xlabel("")
# # #         plt.ylim(0, 110)
# # #         plt.tight_layout()
# # #         plt.savefig(os.path.join(self.output_dir, "1_pass_rate_comparison.png"))
# # #         plt.close()

# # #     def plot_score_distribution(self):
# # #         """Generates a violin plot to show the density of scores (1-5)."""
# # #         plt.figure(figsize=(10, 6))
# # #         sns.violinplot(
# # #             data=self.df, 
# # #             x="pair_name", 
# # #             y="url_score", 
# # #             palette="muted",
# # #             cut=0  # Don't extend past min/max scores
# # #         )
# # #         sns.stripplot(
# # #             data=self.df, 
# # #             x="pair_name", 
# # #             y="url_score", 
# # #             color="black", 
# # #             alpha=0.3, 
# # #             jitter=True
# # #         )
# # #         plt.title("Distribution of URL Scores (Violin Plot)", fontsize=14)
# # #         plt.ylabel("URL Score (1-5)")
# # #         plt.xlabel("")
# # #         plt.tight_layout()
# # #         plt.savefig(os.path.join(self.output_dir, "2_score_distribution.png"))
# # #         plt.close()

# # #     def plot_failure_heatmap(self):
# # #         """Shows average scores broken down by Action and Writer."""
# # #         # Pivot table: Rows=Action, Cols=Writer, Values=URL Score
# # #         pivot = self.df.pivot_table(
# # #             index="action", 
# # #             columns="writer_model", 
# # #             values="url_score", 
# # #             aggfunc="mean"
# # #         )
        
# # #         plt.figure(figsize=(8, 6))
# # #         sns.heatmap(pivot, annot=True, cmap="RdYlGn", vmin=1, vmax=5, fmt=".2f")
# # #         plt.title("Average URL Score by Action & Writer", fontsize=14)
# # #         plt.tight_layout()
# # #         plt.savefig(os.path.join(self.output_dir, "3_failure_heatmap.png"))
# # #         plt.close()

# # #     def plot_correlation(self):
# # #         """Shows if high URL scores correlate with high Faithfulness."""
# # #         plt.figure(figsize=(8, 6))
# # #         # Add a tiny bit of jitter so dots don't overlap perfectly
# # #         sns.regplot(
# # #             data=self.df,
# # #             x="url_score",
# # #             y="faithfulness",
# # #             x_jitter=0.1,
# # #             y_jitter=0.1,
# # #             scatter_kws={'alpha':0.5},
# # #             line_kws={'color':'red'}
# # #         )
# # #         plt.title("Correlation: URL Safety vs. Email Faithfulness", fontsize=14)
# # #         plt.xlabel("URL Preservation Score")
# # #         plt.ylabel("Faithfulness Score")
# # #         plt.tight_layout()
# # #         plt.savefig(os.path.join(self.output_dir, "4_correlation_plot.png"))
# # #         plt.close()

# # #     def _generate_markdown_report(self):
# # #         pass_rates = self.df.groupby("pair_name")['passed'].mean() * 100
# # #         avg_scores = self.df.groupby("pair_name")[["url_score", "faithfulness", "overall"]].mean()
        
# # #         report = [
# # #             "# 🛡️ Cross-Evaluation Analytics Report",
# # #             "\n## 🏆 Executive Summary",
# # #             "This report compares two setups: **Mini writing (judged by 4.1)** vs **4.1 writing (judged by Mini)**.\n"
# # #         ]
        
# # #         report.append("### 1. Pass Rate Comparison (Score >= 4)")
# # #         for pair, rate in pass_rates.items():
# # #             icon = "✅" if rate > 90 else "⚠️" if rate > 70 else "❌"
# # #             clean_name = pair.replace("\n", " -> ")
# # #             report.append(f"- **{clean_name}**: {icon} **{rate:.1f}%**")

# # #         report.append("\n### 2. Detailed Metrics Table")
# # #         report.append(avg_scores.to_markdown())
        
# # #         report.append("\n### 3. Insights")
# # #         report.append("- **If Writer A > Writer B:** Writer A is better at following instructions to keep URLs safe.")
# # #         report.append("- **If Judge A's scores are lower:** Judge A is likely stricter or catching subtle errors the other judge missed.")

# # #         with open(os.path.join(self.output_dir, "summary_report.md"), "w", encoding="utf-8") as f:
# # #             f.write("\n".join(report))

# # # # ======================================================
# # # # MAIN ORCHESTRATOR
# # # # ======================================================
# # # def main():
# # #     print("🚀 Starting Advanced Cross-Evaluation Pipeline...")
    
# # #     # 1. Generate Datasets (Writers)
# # #     # Ensure both models generate their versions of the emails
# # #     generate_dataset("gpt-4o-mini", FILES["edited_by_mini"])
# # #     generate_dataset("gpt-4.1", FILES["edited_by_41"]) 

# # #     # 2. Run Cross-Evaluation (Judges)
# # #     final_df = run_cross_evaluation()

# # #     if final_df.empty:
# # #         print("❌ No evaluation results found. Check your API keys and files.")
# # #         return

# # #     # 3. Save & Analyze
# # #     final_df.to_csv(FILES["final_csv"], index=False)
# # #     print(f"\n💾 Results saved to '{FILES['final_csv']}'")
    
# # #     analytics = URLAnalytics(final_df)
# # #     analytics.run_full_analysis()
    
# # #     print("\n✅ Pipeline Complete! Open 'analytics_output/' to see your new graphs.")

# # # if __name__ == "__main__":
# # #     main()
# # import os
# # import json
# # import yaml
# # import pandas as pd
# # from dotenv import load_dotenv
# # from openai import OpenAI
# # from tqdm import tqdm

# # load_dotenv()

# # # ======================================================
# # # CONFIG & PATHS
# # # ======================================================
# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # FILES = {
# #     "raw_dataset": os.path.join(BASE_DIR, "url_dataset_ai_randomized.jsonl"),
# #     "prompts": os.path.join(BASE_DIR, "same_prompts.yaml"),
    
# #     # 1. WRITTEN EMAILS
# #     "written_mini": os.path.join(BASE_DIR, "emails_written_by_mini.jsonl"),
# #     "written_41":   os.path.join(BASE_DIR, "emails_written_by_41.jsonl"),
    
# #     # 2. INDIVIDUAL EVALUATION RESULTS
# #     "eval_w_mini_j_mini": os.path.join(BASE_DIR, "results_writer_mini_judge_mini.jsonl"),
# #     "eval_w_mini_j_41":   os.path.join(BASE_DIR, "results_writer_mini_judge_41.jsonl"),
# #     "eval_w_41_j_mini":   os.path.join(BASE_DIR, "results_writer_41_judge_mini.jsonl"),
# #     "eval_w_41_j_41":     os.path.join(BASE_DIR, "results_writer_41_judge_41.jsonl"),

# #     # 3. MASTER CSV
# #     "final_csv": os.path.join(BASE_DIR, "full_matrix_metrics.csv"),
# # }

# # # TEST LIMIT - Set to None to run all
# # TEST_LIMIT = 5 

# # if not os.path.exists(FILES["prompts"]):
# #     print(f"❌ Error: '{FILES['prompts']}' not found.")
# #     exit()

# # with open(FILES["prompts"], "r", encoding="utf-8") as f:
# #     PROMPTS = yaml.safe_load(f)

# # def get_client():
# #     return OpenAI(
# #         api_key=os.getenv("OPENAI_API_KEY"),
# #         base_url=os.getenv("OPENAI_API_BASE")
# #     )

# # # ======================================================
# # # STAGE 1: GENERATION (The Writers)
# # # ======================================================
# # def generate_dataset(writer_model, output_file, limit=None):
# #     print(f"\n✍️  [GENERATION] Writer: {writer_model}")
    
# #     # FOR TESTING: If limiting, we likely want to overwrite to ensure a clean test
# #     mode = "w"
# #     if limit:
# #         print(f"   ⚠️ TEST MODE: Limiting to first {limit} records only.")

# #     if not os.path.exists(FILES["raw_dataset"]):
# #         print("❌ Error: Raw dataset missing.")
# #         exit()

# #     client = get_client()
# #     SYSTEM_PROMPT = "You are an AI assistant. Rewrite the email to be professional. IMPORTANT: Preserve all URLs exactly."

# #     processed_count = 0
    
# #     with open(FILES["raw_dataset"], "r", encoding="utf-8") as f_in, \
# #          open(output_file, mode, encoding="utf-8") as f_out:
        
# #         lines = f_in.readlines()
        
# #         # SLICE THE DATA IF LIMIT EXISTS
# #         if limit:
# #             lines = lines[:limit]

# #         for line in tqdm(lines, desc=f"   Writing ({writer_model})"):
# #             data = json.loads(line)
# #             original = data.get("content", "")
# #             if not original: continue

# #             try:
# #                 response = client.chat.completions.create(
# #                     model=writer_model,
# #                     messages=[
# #                         {"role": "system", "content": SYSTEM_PROMPT},
# #                         {"role": "user", "content": original}
# #                     ],
# #                     temperature=0.7
# #                 )
# #                 edited_content = response.choices[0].message.content
                
# #                 record = {
# #                     "id": data.get("id"),
# #                     "writer_model": writer_model,
# #                     "original_email": original,
# #                     "edited_email": edited_content
# #                 }
# #                 f_out.write(json.dumps(record) + "\n")
# #                 processed_count += 1
            
# #             except Exception as e:
# #                 print(f"   ⚠️ Write error for {writer_model}: {e}")
    
# #     print(f"   ✅ Finished writing {processed_count} emails.")

# # # ======================================================
# # # STAGE 2: EVALUATION (The Judges)
# # # ======================================================
# # class URLLLMEvaluator:
# #     def __init__(self, model):
# #         self.client = get_client()
# #         self.model = model

# #     def evaluate(self, original, edited):
# #         if "evaluate" not in PROMPTS: return None
# #         system = PROMPTS["evaluate"]["system"]
# #         user = PROMPTS["evaluate"]["user"].format(original=original, edited=edited)

# #         try:
# #             response = self.client.chat.completions.create(
# #                 model=self.model,
# #                 messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
# #                 temperature=0
# #             )
# #             content = response.choices[0].message.content
# #             if content.startswith("```"):
# #                 content = content.replace("```json", "").replace("```", "")
# #             return json.loads(content)
# #         except Exception:
# #             return None

# # def run_evaluation_task(input_file, output_file, writer_name, judge_name, limit=None):
# #     print(f"\n⚖️  [JUDGING] Writer: {writer_name} | Judge: {judge_name}")
    
# #     if limit:
# #         print(f"   ⚠️ TEST MODE: Limiting evaluation to first {limit} records.")

# #     # We overwrite in test mode to ensure we see fresh results
# #     mode = "w"

# #     evaluator = URLLLMEvaluator(judge_name)
# #     csv_rows = []
    
# #     if not os.path.exists(input_file):
# #         print(f"   ❌ Input file missing: {input_file}")
# #         return []

# #     with open(input_file, "r", encoding="utf-8") as f_in, \
# #          open(output_file, mode, encoding="utf-8") as f_out:
        
# #         samples = [json.loads(line) for line in f_in]
        
# #         # SLICE DATA IF LIMIT EXISTS
# #         if limit:
# #             samples = samples[:limit]
        
# #         for sample in tqdm(samples, desc="    Evaluating"):
# #             eval_result = evaluator.evaluate(sample["original_email"], sample["edited_email"])
            
# #             if eval_result:
# #                 # 1. JSONL Record
# #                 detailed_record = {
# #                     "id": sample.get("id"),
# #                     "writer_model": writer_name,
# #                     "judge_model": judge_name,
# #                     "original_email": sample["original_email"],
# #                     "edited_email": sample["edited_email"],
# #                     "scores": {
# #                         "url_score": eval_result.get("url_preservation", {}).get("score", 0),
# #                         "faithfulness": eval_result.get("faithfulness", {}).get("score", 0),
# #                         "explanation": eval_result.get("url_preservation", {}).get("explanation", "")
# #                     }
# #                 }
# #                 f_out.write(json.dumps(detailed_record) + "\n")
                
# #                 # 2. CSV Record
# #                 csv_rows.append({
# #                     "id": sample.get("id"),
# #                     "writer_model": writer_name,
# #                     "judge_model": judge_name,
# #                     "pair_label": f"Writer:{writer_name}\nJudge:{judge_name}",
# #                     "url_score": detailed_record["scores"]["url_score"],
# #                     "faithfulness": detailed_record["scores"]["faithfulness"],
# #                     "original_email": sample["original_email"],
# #                     "edited_email": sample["edited_email"]
# #                 })
    
# #     return csv_rows

# # # ======================================================
# # # MAIN
# # # ======================================================
# # def main():
# #     print(f"🚀 INITIALIZING 2x2 MATRIX (TEST LIMIT: {TEST_LIMIT} items)")
    
# #     # 1. GENERATE (Writers)
# #     # We pass the TEST_LIMIT here
# #     generate_dataset("gpt-4o-mini", FILES["written_mini"], limit=TEST_LIMIT)
# #     generate_dataset("gpt-4.1",     FILES["written_41"],   limit=TEST_LIMIT) 

# #     # 2. EVALUATE (Judges)
# #     all_csv_data = []

# #     # Pair 1: Mini writes, Mini judges
# #     data_1 = run_evaluation_task(FILES["written_mini"], FILES["eval_w_mini_j_mini"], "gpt-4o-mini", "gpt-4o-mini", limit=TEST_LIMIT)
# #     all_csv_data.extend(data_1)

# #     # Pair 2: Mini writes, 4.1 judges
# #     data_2 = run_evaluation_task(FILES["written_mini"], FILES["eval_w_mini_j_41"], "gpt-4o-mini", "gpt-4.1", limit=TEST_LIMIT)
# #     all_csv_data.extend(data_2)

# #     # Pair 3: 4.1 writes, Mini judges
# #     data_3 = run_evaluation_task(FILES["written_41"], FILES["eval_w_41_j_mini"], "gpt-4.1", "gpt-4o-mini", limit=TEST_LIMIT)
# #     all_csv_data.extend(data_3)

# #     # Pair 4: 4.1 writes, 4.1 judges
# #     data_4 = run_evaluation_task(FILES["written_41"], FILES["eval_w_41_j_41"], "gpt-4.1", "gpt-4.1", limit=TEST_LIMIT)
# #     all_csv_data.extend(data_4)

# #     # 3. SAVE MASTER CSV
# #     if all_csv_data:
# #         print(f"\n💾 Saving Master Data (Test Run) to: {FILES['final_csv']}")
# #         df = pd.DataFrame(all_csv_data)
# #         df.to_csv(FILES["final_csv"], index=False)
# #         print("✅ SUCCESS: Test run complete.")
# #         print("👉 NOW RUN: python url_compare.py")
# #     else:
# #         print("❌ No data collected.")

# # if __name__ == "__main__":
# #     main()
# import os
# import json
# import yaml
# import pandas as pd
# from dotenv import load_dotenv
# from openai import OpenAI
# from tqdm import tqdm

# load_dotenv()

# # ======================================================
# # CONFIG & PATHS
# # ======================================================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# FILES = {
#     "raw_dataset": os.path.join(BASE_DIR, "url_dataset_ai_randomized.jsonl"),
#     "prompts": os.path.join(BASE_DIR, "same_prompts.yaml"),
    
#     # 1. WRITTEN EMAILS
#     "written_mini": os.path.join(BASE_DIR, "emails_written_by_mini.jsonl"),
#     "written_41":   os.path.join(BASE_DIR, "emails_written_by_41.jsonl"),
    
#     # 2. INDIVIDUAL EVALUATION RESULTS
#     "eval_w_mini_j_mini": os.path.join(BASE_DIR, "results_writer_mini_judge_mini.jsonl"),
#     "eval_w_mini_j_41":   os.path.join(BASE_DIR, "results_writer_mini_judge_41.jsonl"),
#     "eval_w_41_j_mini":   os.path.join(BASE_DIR, "results_writer_41_judge_mini.jsonl"),
#     "eval_w_41_j_41":     os.path.join(BASE_DIR, "results_writer_41_judge_41.jsonl"),

#     # 3. MASTER CSV
#     "final_csv": os.path.join(BASE_DIR, "full_matrix_metrics.csv"),
# }

# # TEST LIMIT - Set to None to run all
# TEST_LIMIT = None 

# if not os.path.exists(FILES["prompts"]):
#     print(f"❌ Error: '{FILES['prompts']}' not found.")
#     exit()

# with open(FILES["prompts"], "r", encoding="utf-8") as f:
#     PROMPTS = yaml.safe_load(f)

# def get_client():
#     return OpenAI(
#         api_key=os.getenv("OPENAI_API_KEY"),
#         base_url=os.getenv("OPENAI_API_BASE")
#     )

# # ======================================================
# # STAGE 1: GENERATION (The Writers)
# # ======================================================
# def generate_dataset(writer_model, output_file, limit=None):
#     print(f"\n✍️  [GENERATION] Writer: {writer_model}")
    
#     # Using write mode 'w' to overwrite old files and ensure a fresh start
#     mode = "w"
#     if limit:
#         print(f"   ⚠️ TEST MODE: Limiting to first {limit} records only.")

#     if not os.path.exists(FILES["raw_dataset"]):
#         print("❌ Error: Raw dataset missing.")
#         exit()

#     client = get_client()
#     SYSTEM_PROMPT = "You are an AI assistant. Rewrite the email to be professional. IMPORTANT: Preserve all URLs exactly."

#     processed_count = 0
    
#     with open(FILES["raw_dataset"], "r", encoding="utf-8") as f_in, \
#          open(output_file, mode, encoding="utf-8") as f_out:
        
#         lines = f_in.readlines()
        
#         # SLICE THE DATA IF LIMIT EXISTS
#         if limit:
#             lines = lines[:limit]

#         for line in tqdm(lines, desc=f"   Writing ({writer_model})"):
#             data = json.loads(line)
#             original = data.get("content", "")
#             if not original: continue

#             try:
#                 response = client.chat.completions.create(
#                     model=writer_model,
#                     messages=[
#                         {"role": "system", "content": SYSTEM_PROMPT},
#                         {"role": "user", "content": original}
#                     ],
#                     temperature=0.7
#                 )
#                 edited_content = response.choices[0].message.content
                
#                 record = {
#                     "id": data.get("id"),
#                     "writer_model": writer_model,
#                     "original_email": original,
#                     "edited_email": edited_content
#                 }
#                 f_out.write(json.dumps(record) + "\n")
#                 processed_count += 1
            
#             except Exception as e:
#                 print(f"   ⚠️ Write error for {writer_model}: {e}")
    
#     print(f"   ✅ Finished writing {processed_count} emails.")

# # ======================================================
# # STAGE 2: EVALUATION (The Judges)
# # ======================================================
# class URLLLMEvaluator:
#     def __init__(self, model):
#         self.client = get_client()
#         self.model = model

#     def evaluate(self, original, edited):
#         if "evaluate" not in PROMPTS: return None
#         system = PROMPTS["evaluate"]["system"]
#         user = PROMPTS["evaluate"]["user"].format(original=original, edited=edited)

#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
#                 temperature=0
#             )
#             content = response.choices[0].message.content
#             if content.startswith("```"):
#                 content = content.replace("```json", "").replace("```", "")
#             return json.loads(content)
#         except Exception:
#             return None

# def run_evaluation_task(input_file, output_file, writer_name, judge_name, limit=None):
#     print(f"\n⚖️  [JUDGING] Writer: {writer_name} | Judge: {judge_name}")
    
#     if limit:
#         print(f"   ⚠️ TEST MODE: Limiting evaluation to first {limit} records.")

#     # Always overwrite 'w' to ensure fresh data
#     mode = "w"

#     evaluator = URLLLMEvaluator(judge_name)
#     csv_rows = []
    
#     if not os.path.exists(input_file):
#         print(f"   ❌ Input file missing: {input_file}")
#         return []

#     with open(input_file, "r", encoding="utf-8") as f_in, \
#          open(output_file, mode, encoding="utf-8") as f_out:
        
#         samples = [json.loads(line) for line in f_in]
        
#         # SLICE DATA IF LIMIT EXISTS
#         if limit:
#             samples = samples[:limit]
        
#         for sample in tqdm(samples, desc="    Evaluating"):
#             eval_result = evaluator.evaluate(sample["original_email"], sample["edited_email"])
            
#             if eval_result:
#                 # 1. JSONL Record
#                 detailed_record = {
#                     "id": sample.get("id"),
#                     "writer_model": writer_name,
#                     "judge_model": judge_name,
#                     "original_email": sample["original_email"],
#                     "edited_email": sample["edited_email"],
#                     "scores": {
#                         "url_score": eval_result.get("url_preservation", {}).get("score", 0),
#                         "faithfulness": eval_result.get("faithfulness", {}).get("score", 0),
#                         "explanation": eval_result.get("url_preservation", {}).get("explanation", "")
#                     }
#                 }
#                 f_out.write(json.dumps(detailed_record) + "\n")
                
#                 # 2. CSV Record
#                 csv_rows.append({
#                     "id": sample.get("id"),
#                     "writer_model": writer_name,
#                     "judge_model": judge_name,
#                     "pair_label": f"Writer:{writer_name}\nJudge:{judge_name}",
#                     "url_score": detailed_record["scores"]["url_score"],
#                     "faithfulness": detailed_record["scores"]["faithfulness"],
#                     "original_email": sample["original_email"],
#                     "edited_email": sample["edited_email"]
#                 })
    
#     return csv_rows

# # ======================================================
# # MAIN
# # ======================================================
# def main():
#     print(f"🚀 INITIALIZING 2x2 MATRIX (Full Run - No Limit)")
    
#     # 1. GENERATE (Writers)
#     generate_dataset("gpt-4o-mini", FILES["written_mini"], limit=TEST_LIMIT)
#     generate_dataset("gpt-4.1",     FILES["written_41"],   limit=TEST_LIMIT) 

#     # 2. EVALUATE (Judges)
#     all_csv_data = []

#     # Pair 1: Mini writes, Mini judges
#     data_1 = run_evaluation_task(FILES["written_mini"], FILES["eval_w_mini_j_mini"], "gpt-4o-mini", "gpt-4o-mini", limit=TEST_LIMIT)
#     all_csv_data.extend(data_1)

#     # Pair 2: Mini writes, 4.1 judges
#     data_2 = run_evaluation_task(FILES["written_mini"], FILES["eval_w_mini_j_41"], "gpt-4o-mini", "gpt-4.1", limit=TEST_LIMIT)
#     all_csv_data.extend(data_2)

#     # Pair 3: 4.1 writes, Mini judges
#     data_3 = run_evaluation_task(FILES["written_41"], FILES["eval_w_41_j_mini"], "gpt-4.1", "gpt-4o-mini", limit=TEST_LIMIT)
#     all_csv_data.extend(data_3)

#     # Pair 4: 4.1 writes, 4.1 judges
#     data_4 = run_evaluation_task(FILES["written_41"], FILES["eval_w_41_j_41"], "gpt-4.1", "gpt-4.1", limit=TEST_LIMIT)
#     all_csv_data.extend(data_4)

#     # 3. SAVE MASTER CSV
#     if all_csv_data:
#         print(f"\n💾 Saving Master Data to: {FILES['final_csv']}")
#         df = pd.DataFrame(all_csv_data)
#         df.to_csv(FILES["final_csv"], index=False)
#         print("✅ SUCCESS: Full evaluation complete.")
#         print("👉 NOW RUN: python url_compare.py")
#     else:
#         print("❌ No data collected.")

# if __name__ == "__main__":
#     main()
import os
import json
import yaml
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

load_dotenv()

# ======================================================
# CONFIG & PATHS
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "raw_dataset": os.path.join(BASE_DIR, "url_dataset_ai_randomized.jsonl"),
    "prompts": os.path.join(BASE_DIR, "same_prompts.yaml"),
    
    # 1. WRITTEN EMAILS
    "written_mini": os.path.join(BASE_DIR, "emails_written_by_mini.jsonl"),
    "written_41":   os.path.join(BASE_DIR, "emails_written_by_41.jsonl"),
    
    # 2. INDIVIDUAL EVALUATION RESULTS
    "eval_w_mini_j_mini": os.path.join(BASE_DIR, "results_writer_mini_judge_mini.jsonl"),
    "eval_w_mini_j_41":   os.path.join(BASE_DIR, "results_writer_mini_judge_41.jsonl"),
    "eval_w_41_j_mini":   os.path.join(BASE_DIR, "results_writer_41_judge_mini.jsonl"),
    "eval_w_41_j_41":     os.path.join(BASE_DIR, "results_writer_41_judge_41.jsonl"),

    # 3. MASTER CSV
    "final_csv": os.path.join(BASE_DIR, "full_matrix_metrics.csv"),
}

# TEST LIMIT - Set to None to run all emails
TEST_LIMIT = None 

# LOAD PROMPTS
if not os.path.exists(FILES["prompts"]):
    print(f"❌ Error: '{FILES['prompts']}' not found.")
    exit()

with open(FILES["prompts"], "r", encoding="utf-8") as f:
    PROMPTS = yaml.safe_load(f)

def get_client():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE")
    )

# ======================================================
# STAGE 1: GENERATION (The Writers)
# ======================================================
def generate_dataset(writer_model, output_file, limit=None):
    print(f"\n✍️  [GENERATION] Writer: {writer_model}")
    
    # --- CRITICAL FIX: Use the strict prompt from YAML ---
    if "email_core" in PROMPTS:
        SYSTEM_PROMPT = PROMPTS["email_core"]["system"]
    else:
        # Fallback only if YAML is broken
        SYSTEM_PROMPT = "You are an AI assistant. Rewrite professionally. CRITICAL: Preserve all URLs exactly."

    mode = "w"
    if limit:
        print(f"   ⚠️ TEST MODE: Limiting to first {limit} records only.")

    if not os.path.exists(FILES["raw_dataset"]):
        print("❌ Error: Raw dataset missing.")
        exit()

    client = get_client()
    processed_count = 0
    
    with open(FILES["raw_dataset"], "r", encoding="utf-8") as f_in, \
         open(output_file, mode, encoding="utf-8") as f_out:
        
        lines = f_in.readlines()
        
        if limit:
            lines = lines[:limit]

        for line in tqdm(lines, desc=f"   Writing ({writer_model})"):
            data = json.loads(line)
            original = data.get("content", "")
            if not original: continue

            try:
                response = client.chat.completions.create(
                    model=writer_model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": original}
                    ],
                    temperature=0.7
                )
                edited_content = response.choices[0].message.content
                
                record = {
                    "id": data.get("id"),
                    "writer_model": writer_model,
                    "original_email": original,
                    "edited_email": edited_content
                }
                f_out.write(json.dumps(record) + "\n")
                processed_count += 1
            
            except Exception as e:
                print(f"   ⚠️ Write error for {writer_model}: {e}")
    
    print(f"   ✅ Finished writing {processed_count} emails.")

# ======================================================
# STAGE 2: EVALUATION (The Judges)
# ======================================================
class URLLLMEvaluator:
    def __init__(self, model):
        self.client = get_client()
        self.model = model

    def evaluate(self, original, edited):
        if "evaluate" not in PROMPTS: return None
        
        # Load Judge Prompts
        system = PROMPTS["evaluate"]["system"]
        user = PROMPTS["evaluate"]["user"].format(original=original, edited=edited)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0
            )
            content = response.choices[0].message.content
            
            # Clean Markdown formatting if present
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "")
            
            return json.loads(content)
        except Exception:
            return None

def run_evaluation_task(input_file, output_file, writer_name, judge_name, limit=None):
    print(f"\n⚖️  [JUDGING] Writer: {writer_name} | Judge: {judge_name}")
    
    if limit:
        print(f"   ⚠️ TEST MODE: Limiting evaluation to first {limit} records.")

    mode = "w"
    evaluator = URLLLMEvaluator(judge_name)
    csv_rows = []
    
    if not os.path.exists(input_file):
        print(f"   ❌ Input file missing: {input_file}")
        return []

    with open(input_file, "r", encoding="utf-8") as f_in, \
         open(output_file, mode, encoding="utf-8") as f_out:
        
        samples = [json.loads(line) for line in f_in]
        
        if limit:
            samples = samples[:limit]
        
        for sample in tqdm(samples, desc="    Evaluating"):
            eval_result = evaluator.evaluate(sample["original_email"], sample["edited_email"])
            
            if eval_result:
                # 1. JSONL Record
                detailed_record = {
                    "id": sample.get("id"),
                    "writer_model": writer_name,
                    "judge_model": judge_name,
                    "original_email": sample["original_email"],
                    "edited_email": sample["edited_email"],
                    "scores": {
                        "url_score": eval_result.get("url_preservation", {}).get("score", 0),
                        "faithfulness": eval_result.get("faithfulness", {}).get("score", 0),
                        "completeness": eval_result.get("completeness", {}).get("score", 0),
                        "robustness": eval_result.get("robustness", {}).get("score", 0),
                        "overall": eval_result.get("overall", {}).get("score", 0),
                        "explanation": eval_result.get("url_preservation", {}).get("reason", "")
                    }
                }
                f_out.write(json.dumps(detailed_record) + "\n")
                
                # 2. CSV Record
                csv_rows.append({
                    "id": sample.get("id"),
                    "writer_model": writer_name,
                    "judge_model": judge_name,
                    "pair_label": f"Writer:{writer_name}\nJudge:{judge_name}",
                    "url_score": detailed_record["scores"]["url_score"],
                    "faithfulness": detailed_record["scores"]["faithfulness"],
                    "overall": detailed_record["scores"]["overall"],
                    "original_email": sample["original_email"],
                    "edited_email": sample["edited_email"]
                })
    
    return csv_rows

# ======================================================
# MAIN
# ======================================================
def main():
    print(f"🚀 INITIALIZING 2x2 MATRIX (Full Run)")
    
    # 1. GENERATE (Writers)
    # Ensure 'gpt-4.1' is the correct model name in your API, otherwise change to 'gpt-4o' or 'gpt-4-turbo'
    generate_dataset("gpt-4o-mini", FILES["written_mini"], limit=TEST_LIMIT)
    generate_dataset("gpt-4.1",     FILES["written_41"],   limit=TEST_LIMIT) 

    # 2. EVALUATE (Judges)
    all_csv_data = []

    # Pair 1: Mini writes, Mini judges
    data_1 = run_evaluation_task(FILES["written_mini"], FILES["eval_w_mini_j_mini"], "gpt-4o-mini", "gpt-4o-mini", limit=TEST_LIMIT)
    all_csv_data.extend(data_1)

    # Pair 2: Mini writes, 4.1 judges
    data_2 = run_evaluation_task(FILES["written_mini"], FILES["eval_w_mini_j_41"], "gpt-4o-mini", "gpt-4.1", limit=TEST_LIMIT)
    all_csv_data.extend(data_2)

    # Pair 3: 4.1 writes, Mini judges
    data_3 = run_evaluation_task(FILES["written_41"], FILES["eval_w_41_j_mini"], "gpt-4.1", "gpt-4o-mini", limit=TEST_LIMIT)
    all_csv_data.extend(data_3)

    # Pair 4: 4.1 writes, 4.1 judges
    data_4 = run_evaluation_task(FILES["written_41"], FILES["eval_w_41_j_41"], "gpt-4.1", "gpt-4.1", limit=TEST_LIMIT)
    all_csv_data.extend(data_4)

    # 3. SAVE MASTER CSV
    if all_csv_data:
        print(f"\n💾 Saving Master Data to: {FILES['final_csv']}")
        df = pd.DataFrame(all_csv_data)
        df.to_csv(FILES["final_csv"], index=False)
        print("✅ SUCCESS: Full evaluation complete.")
        print("👉 NOW RUN: python url_compare.py")
    else:
        print("❌ No data collected.")

if __name__ == "__main__":
    main()