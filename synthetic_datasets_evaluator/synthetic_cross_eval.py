
# import os
# import json
# import yaml
# from openai import OpenAI
# from pathlib import Path
# from dotenv import load_dotenv
# from typing import List, Dict, Any

# load_dotenv()

# # Configuration
# MODELS = {
#     "4.1": os.getenv("OPENAI_MODEL2", "gpt-4.1"),     # High-end
#     "mini": os.getenv("OPENAI_MODEL1", "gpt-4o-mini") # Efficient
# }

# BASE_DIR = Path(__file__).resolve().parent
# ITEMS_DIR = BASE_DIR.parent / "synthetic_datasets"
# EVAL_DIR = BASE_DIR
# RESULTS_DIR = EVAL_DIR / "synthetic_result"
# LIMIT = 50  # Change to 50 when needed

# def load_prompts():
#     with open(EVAL_DIR / "synthetic_data_prompts.yaml", "r", encoding="utf-8") as f:
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

#     results = []

#     client_4_1 = ModelClient("4.1", MODELS["4.1"])
#     client_mini = ModelClient("mini", MODELS["mini"])

#     for i, item in enumerate(data[:items_to_process]):
#         print(f"Processing item {i+1}/{items_to_process}")

#         input_text = (
#             item.get("content")
#             or item.get("text")
#             or item.get("email")
#             or item.get("selected_text")
#         )

#         if not input_text:
#             print(f"Skipping item {i}, no text found")
#             continue

#         system_tmpl = PROMPTS[task_name]["system"]
#         user_tmpl = PROMPTS[task_name]["user"]

#         fmt_args = {"selected_text": input_text}
#         target_tone = None

#         # ✅ UPDATED TONE LOGIC (ONLY CHANGE)
#         if task_name == "tone":
#             if i < 20:
#                 target_tone = "professional"
#             elif i < 35:
#                 target_tone = "friendly"
#             else:
#                 target_tone = "sympathetic"

#             fmt_args["tone"] = target_tone
#         else:
#             target_tone = item.get("target_tone")

#         system_prompt = system_tmpl.format(**fmt_args)
#         user_prompt = user_tmpl.format(**fmt_args)

#         resp_4_1 = client_4_1.generate(system_prompt, user_prompt)
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

#     client_judge_mini = ModelClient("mini", MODELS["mini"])
#     client_judge_4_1 = ModelClient("4.1", MODELS["4.1"])

#     final_data = []

#     for item in generated_results:
#         original = item["original_text"]

#         resp_4_1 = item["response_4_1"]
#         eval_user_4_1 = eval_usr_tmpl.format(
#             original=original,
#             edited=resp_4_1
#         )
#         score_4_1 = client_judge_mini.evaluate(eval_sys_tmpl, eval_user_4_1)

#         resp_mini = item["response_mini"]
#         eval_user_mini = eval_usr_tmpl.format(
#             original=original,
#             edited=resp_mini
#         )
#         score_mini = client_judge_4_1.evaluate(eval_sys_tmpl, eval_user_mini)

#         item["evaluation_of_4_1_by_mini"] = score_4_1
#         item["evaluation_of_mini_by_4_1"] = score_mini

#         final_data.append(item)

#     return final_data

# def main():
#     RESULTS_DIR.mkdir(parents=True, exist_ok=True)

#     tasks = {
#         "lengthen": "synthetic_length.jsonl",
#         "shorten": "synthetic_shorten.jsonl",
#         "tone": "synthetic_tone.jsonl"
#     }

#     for task_name, filename in tasks.items():
#         jsonl_path = ITEMS_DIR / filename
#         if not jsonl_path.exists():
#             print(f"Dataset not found: {jsonl_path}")
#             continue

#         with open(jsonl_path, "r", encoding="utf-8") as f:
#             data = [json.loads(line) for line in f]

#         gen_results = process_task_generation(task_name, data, LIMIT)

#         if gen_results:
#             final_results = process_task_evaluation(task_name, gen_results)

#             out_dir = RESULTS_DIR / task_name
#             out_dir.mkdir(exist_ok=True)

#             out_file = out_dir / "cross_eval_results.json"
#             with open(out_file, "w", encoding="utf-8") as f:
#                 json.dump(final_results, f, indent=2)

#             print(f"Saved results to {out_file}")

# if __name__ == "__main__":
# #     main()
import os
import json
import yaml
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
MODELS = {
    "4.1": os.getenv("OPENAI_MODEL2", "gpt-4.1"),     # High-end
    "mini": os.getenv("OPENAI_MODEL1", "gpt-4o-mini") # Efficient
}

BASE_DIR = Path(__file__).resolve().parent
ITEMS_DIR = BASE_DIR.parent / "synthetic_datasets"
EVAL_DIR = BASE_DIR
RESULTS_DIR = EVAL_DIR / "synthetic_result"
LIMIT = 25  # change to 50 if needed

# --------------------------------------------------
# LOAD PROMPTS
# --------------------------------------------------
def load_prompts():
    try:
        with open(EVAL_DIR / "synthetic_data_prompts.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: synthetic_data_prompts.yaml not found")
        return {}

PROMPTS = load_prompts()

# --------------------------------------------------
# MODEL CLIENT
# --------------------------------------------------
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
                temperature=0.4
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

# --------------------------------------------------
# GENERATION
# --------------------------------------------------
def process_task_generation(task_name: str, data: List[Dict], items_to_process: int):
    print(f"--- Generating Responses for {task_name.upper()} ---")

    if task_name not in PROMPTS:
        print(f"No prompt config found for {task_name}")
        return []

    results = []

    client_4_1 = ModelClient("4.1", MODELS["4.1"])
    client_mini = ModelClient("mini", MODELS["mini"])

    for i, item in enumerate(data[:items_to_process]):
        print(f"Processing item {i+1}/{items_to_process}")

        if item is None:
            print(f"Skipping item {i+1}: null entry")
            continue

        input_text = (
            item.get("content")
            or item.get("text")
            or item.get("email")
            or item.get("selected_text")
        )

        if not input_text:
            print(f"Skipping item {i+1}: no text found")
            continue

        system_tmpl = PROMPTS[task_name]["system"]
        user_tmpl = PROMPTS[task_name]["user"]

        fmt_args = {"selected_text": input_text}
        target_tone = None

        # Tone logic (unchanged)
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

# --------------------------------------------------
# EVALUATION (4.1 judges both)
# --------------------------------------------------
def process_task_evaluation(task_name: str, generated_results: List[Dict]):
    print(f"--- Evaluating Responses for {task_name.upper()} ---")

    eval_sys_tmpl = PROMPTS["evaluate"]["system"]
    eval_usr_tmpl = PROMPTS["evaluate"]["user"]

    client_judge_4_1 = ModelClient("4.1", MODELS["4.1"])

    final_data = []

    for item in generated_results:
        original = item["original_text"]

        # 4.1 evaluates 4.1
        eval_user_4_1 = eval_usr_tmpl.format(
            original=original,
            edited=item["response_4_1"]
        )
        score_4_1 = client_judge_4_1.evaluate(eval_sys_tmpl, eval_user_4_1)

        # 4.1 evaluates mini
        eval_user_mini = eval_usr_tmpl.format(
            original=original,
            edited=item["response_mini"]
        )
        score_mini = client_judge_4_1.evaluate(eval_sys_tmpl, eval_user_mini)

        item["evaluation_of_4_1_by_4_1"] = score_4_1
        item["evaluation_of_mini_by_4_1"] = score_mini

        final_data.append(item)

    return final_data

# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    tasks = {
        "lengthen": "synthetic_length.jsonl",
        "shorten": "synthetic_shorten.jsonl",
        "tone": "synthetic_tone.jsonl"
    }

    for task_name, filename in tasks.items():
        jsonl_path = ITEMS_DIR / filename

        if not jsonl_path.exists():
            print(f"Dataset not found: {jsonl_path}")
            continue

        with open(jsonl_path, "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]

        gen_results = process_task_generation(task_name, data, LIMIT)

        if gen_results:
            final_results = process_task_evaluation(task_name, gen_results)

            out_dir = RESULTS_DIR / task_name
            out_dir.mkdir(exist_ok=True)

            out_file = out_dir / "cross_eval_results.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(final_results, f, indent=2)

            print(f"Saved results to {out_file}")

if __name__ == "__main__":
    main()
