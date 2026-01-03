
# import os
# import json
# import yaml
# from openai import OpenAI
# from pathlib import Path
# from dotenv import load_dotenv
# import asyncio
# from typing import List, Dict, Any

# load_dotenv()

# # Configuration
# MODELS = {
#     "4.1": os.getenv("OPENAI_MODEL2", "gpt-4.1"),    # "High-end"
#     "mini": os.getenv("OPENAI_MODEL1", "gpt-4o-mini") # "Efficient"
# }

# ITEMS_DIR = Path("datasets")
# EVAL_DIR = Path("datasets_evaluator")
# RESULTS_DIR = EVAL_DIR / "results"
# LIMIT = 5  # Process only the first 5 items

# def load_prompts():
#     with open(EVAL_DIR / "data_prompts.yaml", "r", encoding="utf-8") as f:
#         return yaml.safe_load(f)

# PROMPTS = load_prompts()

# class ModelClient:
#     def __init__(self, model_name: str, model_id: str):
#         self.client = OpenAI(
#             api_key=os.getenv("OPENAI_API_KEY"),
#             base_url=os.getenv("OPENAI_API_BASE")
#         )
#         self.model_name = model_name
#         self.model_id = model_id

#     def generate(self, system_prompt: str, user_prompt: str) -> str:
#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model_id,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 temperature=0.7
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             print(f"Error generating with {self.model_name}: {e}")
#             return ""

#     def evaluate(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model_id,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 temperature=0,
#                 response_format={"type": "json_object"}
#             )
#             return json.loads(response.choices[0].message.content)
#         except Exception as e:
#             print(f"Error evaluating with {self.model_name}: {e}")
#             return {}

# def process_task_generation(task_name: str, data: List[Dict], items_to_process: int):
#     print(f"--- Generating Responses for {task_name.upper()} ---")
    
#     prompt_config = PROMPTS.get(task_name)
#     if not prompt_config:
#         print(f"No prompt config found for {task_name}")
#         return

#     # Use selection prompts if 'selected_text' key is in prompt config, usually prompt keys match task names
#     # But for 'lengthen' etc, the keys in yaml are 'lengthen', 'shorten', 'tone'.
#     # For selection tasks, keys are 'lengthen_selection', etc. 
#     # The dataset keys guide this. If dataset has 'selected_text' and 'full_email' it might be selection mode.
#     # However, prompts.yaml has 'lengthen', 'shorten', 'tone' which use {selected_text} placeholder for full email sometimes or actual selection.
#     # Let's inspect the `data_prompts.yaml` structure again.
#     # It has 'lengthen', 'shorten', 'tone' using {selected_text} as the input variable.
    
#     if task_name not in PROMPTS:
#          # Map dataset names to prompt keys if needed. 
#          # The datasets are lengthen.jsonl, shorten.jsonl, tone.jsonl
#          # The prompt keys are lengthen, shorten, tone.
#          pass
         
#     results = []
    
#     client_4_1 = ModelClient("4.1", MODELS["4.1"])
#     client_mini = ModelClient("mini", MODELS["mini"])

#     for i, item in enumerate(data[:items_to_process]):
#         print(f"Processing item {i+1}/{items_to_process}")
        
#         # Determine content key
#         # Based on typical structure, input might be in 'email', 'text', or 'selected_text'
#         # Let's check the yaml placeholders: {selected_text}
#         # In previously seen code, user was passing the whole email as selected_text for full email ops.
#         # We will assume the input text is in a field called 'text' or 'input' or 'selected_text' in the jsonl.
#         # Need to check dataset structure. For now, try 'original_text' or 'text'.
        
#         input_text = item.get("content") or item.get("text") or item.get("email") or item.get("selected_text")
#         if not input_text:
#             print(f"Skipping item {i}, no text found: {item.keys()}")
#             continue
            
#         # Format Prompts
#         # tone requires 'tone' arg
#         target_tone = item.get("target_tone") # For tone task
        
#         system_tmpl = PROMPTS[task_name]["system"]
#         user_tmpl = PROMPTS[task_name]["user"]
        
#         fmt_args = {"selected_text": input_text}
#         if task_name == "tone":
#              if not target_tone:
#                  target_tone = "professional" # fallback
#              fmt_args["tone"] = target_tone
        
#         system_prompt = system_tmpl.format(**fmt_args)
#         user_prompt = user_tmpl.format(**fmt_args)

#         # 4.1 Gen
#         resp_4_1 = client_4_1.generate(system_prompt, user_prompt)
        
#         # Mini Gen
#         resp_mini = client_mini.generate(system_prompt, user_prompt)
        
#         results.append({
#             "original_id": i,
#             "original_text": input_text,
#             "target_tone": target_tone,
#             "response_4_1": resp_4_1,
#             "response_mini": resp_mini
#         })
        
#     return results

# def process_task_evaluation(task_name: str, generated_results: List[Dict]):
#     print(f"--- Evaluating Responses for {task_name.upper()} ---")
    
#     eval_sys_tmpl = PROMPTS["evaluate"]["system"]
#     eval_usr_tmpl = PROMPTS["evaluate"]["user"]
    
#     client_judge_mini = ModelClient("mini", MODELS["mini"]) # Mini judges 4.1
#     client_judge_4_1 = ModelClient("4.1", MODELS["4.1"])    # 4.1 judges Mini
    
#     final_data = []

#     for item in generated_results:
#         original = item["original_text"]
        
#         # 1. Mini evaluates 4.1
#         # "4.1 will write it and mini will evaluate it"
#         resp_4_1 = item["response_4_1"]
#         eval_prompt_user = eval_usr_tmpl.format(original=original, edited=resp_4_1)
#         score_4_1 = client_judge_mini.evaluate(eval_sys_tmpl, eval_prompt_user)
        
#         # 2. 4.1 evaluates Mini
#         # "mini will write... and the 4.1 will evaluate that"
#         resp_mini = item["response_mini"]
#         eval_prompt_user_mini = eval_usr_tmpl.format(original=original, edited=resp_mini)
#         score_mini = client_judge_4_1.evaluate(eval_sys_tmpl, eval_prompt_user_mini)

#         item["evaluation_of_4_1_by_mini"] = score_4_1
#         item["evaluation_of_mini_by_4_1"] = score_mini
        
#         final_data.append(item)
        
#     return final_data

# def main():
#     if not RESULTS_DIR.exists():
#         RESULTS_DIR.mkdir(parents=True)

#     tasks = ["lengthen", "shorten", "tone"]
    
#     for task in tasks:
#         jsonl_path = ITEMS_DIR / f"{task}.jsonl"
#         if not jsonl_path.exists():
#             print(f"Dataset not found: {jsonl_path}")
#             continue
            
#         with open(jsonl_path, "r", encoding="utf-8") as f:
#             data = [json.loads(line) for line in f]
            
#         # Generation
#         gen_results = process_task_generation(task, data, LIMIT)
        
#         # Evaluation
#         if gen_results:
#             final_results = process_task_evaluation(task, gen_results)
            
#             # Save
#             out_dir = RESULTS_DIR / task
#             out_dir.mkdir(exist_ok=True)
            
#             out_file = out_dir / "cross_eval_results.json"
#             with open(out_file, "w", encoding="utf-8") as f:
#                 json.dump(final_results, f, indent=2)
                
#             print(f"Saved results to {out_file}")

# if __name__ == "__main__":
#     main()
import os
import json
import yaml
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

# Configuration
MODELS = {
    "4.1": os.getenv("OPENAI_MODEL2", "gpt-4.1"),     # High-end
    "mini": os.getenv("OPENAI_MODEL1", "gpt-4o-mini") # Efficient
}

ITEMS_DIR = Path("datasets")
EVAL_DIR = Path("datasets_evaluator")
RESULTS_DIR = EVAL_DIR / "results"
LIMIT = 50  # Change to 50 when needed

def load_prompts():
    with open(EVAL_DIR / "data_prompts.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

PROMPTS = load_prompts()

class ModelClient:
    def __init__(self, model_name: str, model_id: str):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.model_name = model_name
        self.model_id = model_id

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating with {self.model_name}: {e}")
            return ""

    def evaluate(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error evaluating with {self.model_name}: {e}")
            return {}

def process_task_generation(task_name: str, data: List[Dict], items_to_process: int):
    print(f"--- Generating Responses for {task_name.upper()} ---")

    prompt_config = PROMPTS.get(task_name)
    if not prompt_config:
        print(f"No prompt config found for {task_name}")
        return

    results = []

    client_4_1 = ModelClient("4.1", MODELS["4.1"])
    client_mini = ModelClient("mini", MODELS["mini"])

    for i, item in enumerate(data[:items_to_process]):
        print(f"Processing item {i+1}/{items_to_process}")

        input_text = (
            item.get("content")
            or item.get("text")
            or item.get("email")
            or item.get("selected_text")
        )

        if not input_text:
            print(f"Skipping item {i}, no text found")
            continue

        system_tmpl = PROMPTS[task_name]["system"]
        user_tmpl = PROMPTS[task_name]["user"]

        fmt_args = {"selected_text": input_text}
        target_tone = None

        # ✅ UPDATED TONE LOGIC (ONLY CHANGE)
        if task_name == "tone":
            if i < 20:
                target_tone = "professional"
            elif i < 35:
                target_tone = "friendly"
            else:
                target_tone = "sympathetic"

            fmt_args["tone"] = target_tone
        else:
            target_tone = item.get("target_tone")

        system_prompt = system_tmpl.format(**fmt_args)
        user_prompt = user_tmpl.format(**fmt_args)

        resp_4_1 = client_4_1.generate(system_prompt, user_prompt)
        resp_mini = client_mini.generate(system_prompt, user_prompt)

        results.append({
            "original_id": i,
            "original_text": input_text,
            "target_tone": target_tone,
            "response_4_1": resp_4_1,
            "response_mini": resp_mini
        })

    return results

def process_task_evaluation(task_name: str, generated_results: List[Dict]):
    print(f"--- Evaluating Responses for {task_name.upper()} ---")

    eval_sys_tmpl = PROMPTS["evaluate"]["system"]
    eval_usr_tmpl = PROMPTS["evaluate"]["user"]

    client_judge_mini = ModelClient("mini", MODELS["mini"])
    client_judge_4_1 = ModelClient("4.1", MODELS["4.1"])

    final_data = []

    for item in generated_results:
        original = item["original_text"]

        resp_4_1 = item["response_4_1"]
        eval_user_4_1 = eval_usr_tmpl.format(
            original=original,
            edited=resp_4_1
        )
        score_4_1 = client_judge_mini.evaluate(eval_sys_tmpl, eval_user_4_1)

        resp_mini = item["response_mini"]
        eval_user_mini = eval_usr_tmpl.format(
            original=original,
            edited=resp_mini
        )
        score_mini = client_judge_4_1.evaluate(eval_sys_tmpl, eval_user_mini)

        item["evaluation_of_4_1_by_mini"] = score_4_1
        item["evaluation_of_mini_by_4_1"] = score_mini

        final_data.append(item)

    return final_data

def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    tasks = ["lengthen", "shorten", "tone"]

    for task in tasks:
        jsonl_path = ITEMS_DIR / f"{task}.jsonl"
        if not jsonl_path.exists():
            print(f"Dataset not found: {jsonl_path}")
            continue

        with open(jsonl_path, "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]

        gen_results = process_task_generation(task, data, LIMIT)

        if gen_results:
            final_results = process_task_evaluation(task, gen_results)

            out_dir = RESULTS_DIR / task
            out_dir.mkdir(exist_ok=True)

            out_file = out_dir / "cross_eval_results.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(final_results, f, indent=2)

            print(f"Saved results to {out_file}")

if __name__ == "__main__":
    main()
