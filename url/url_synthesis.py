
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