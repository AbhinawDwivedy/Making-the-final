"""
Scenario 1: Selected Text Preservation - Evaluation
Evaluates whether models correctly edit ONLY the selected portion
while preserving surrounding text.
"""

import os
import json
import yaml
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

load_dotenv()

# Load prompts
with open("selected_text_prompts.yaml", "r", encoding="utf-8") as f:
    prompts = yaml.safe_load(f)


class SelectionEditor:
    """Applies editing actions to selected text portions."""
    
    def __init__(self, model):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.model = model

    def _call_api(self, messages, temperature=0.7):
        """Internal API call method."""
        r = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return r.choices[0].message.content.strip()

    def edit_selection(self, action, full_email, selected_text, tone=None):
        """
        Edit only the selected portion of the email.
        
        Args:
            action: One of ['shorten_selection', 'lengthen_selection', 'tone_selection']
            full_email: Complete email for context
            selected_text: The portion to be edited
            tone: Tone type (required for tone_selection)
        
        Returns:
            Edited version of the selected text only
        """
        args = {
            "selected_text_core": prompts["selected_text_core"]["system"],
            "full_email": full_email,
            "selected_text": selected_text,
            "tone": tone if tone else ""
        }
        
        system = prompts[action]["system"].format(**args)
        user = prompts[action]["user"].format(**args)
        
        return self._call_api([
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ])


class SelectionEvaluator:
    """Evaluates selection boundary preservation."""
    
    def __init__(self, model):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.model = model

    def _call_api(self, messages):
        """Internal API call with temperature=0 for consistency."""
        r = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0
        )
        return r.choices[0].message.content

    def evaluate_comprehensive(self, full_email, selected_text, model_output, action):
        """
        Comprehensive evaluation of selection editing.
        
        Returns:
            Dict with scores for selection_boundary, edit_quality, 
            faithfulness, completeness, and overall
        """
        system = prompts["evaluate_comprehensive_selection"]["system"]
        user = prompts["evaluate_comprehensive_selection"]["user"].format(
            full_email=full_email,
            selected_text=selected_text,
            model_output=model_output,
            action=action
        )
        
        try:
            response = self._call_api([
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ])
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing error: {e}")
            print(f"Raw response: {response}")
            return None

    def simple_boundary_check(self, before, selection, after, model_output):
        """
        Simple programmatic check of boundary preservation.
        
        Args:
            before: Text before selection
            selection: Original selected text
            after: Text after selection
            model_output: Model's edited output
        
        Returns:
            Dict with boundary preservation metrics
        """
        # The model should return ONLY the edited selection
        # It should NOT include the before/after portions
        
        contains_before = before.strip() in model_output
        contains_after = after.strip() in model_output
        
        # Good: model returned only edited selection
        # Bad: model returned full email with edits
        correctly_scoped = not (contains_before or contains_after)
        
        return {
            "correctly_scoped": correctly_scoped,
            "contains_before_text": contains_before,
            "contains_after_text": contains_after,
            "output_length": len(model_output),
            "selection_length": len(selection)
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Evaluate Scenario 1: Selected Text Preservation"
    )
    parser.add_argument("--dataset", type=str, 
                        default="selected_text_dataset.jsonl",
                        help="Input dataset file")
    parser.add_argument("--model", type=str, required=True,
                        help="Model to test (e.g., gpt-4.1, gpt-4o-mini)")
    parser.add_argument("--output", type=str, 
                        default="selected_text_results_{model}.jsonl",
                        help="Output results file")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit number of samples to process")
    args = parser.parse_args()

    # Auto-format output filename
    if "{model}" in args.output:
        args.output = args.output.format(model=args.model)

    # Load dataset
    print(f"📂 Loading dataset: {args.dataset}")
    samples = []
    with open(args.dataset, "r", encoding="utf-8") as f:
        for line in f:
            samples.append(json.loads(line))
            if args.limit and len(samples) >= args.limit:
                break

    print(f"✅ Loaded {len(samples)} samples\n")

    # Initialize
    eval_model = os.getenv("EVALUATE_MODEL", "gpt-4.1")
    editor = SelectionEditor(args.model)
    evaluator = SelectionEvaluator(eval_model)

    print(f"🤖 Testing Model: {args.model}")
    print(f"⚖️  Evaluator Model: {eval_model}")
    print(f"💾 Output: {args.output}\n")

    # Process samples
    results = []
    with open(args.output, "w", encoding="utf-8") as out_file:
        for sample in tqdm(samples, desc="Evaluating", unit="sample"):
            try:
                # Edit the selection
                edited_selection = editor.edit_selection(
                    action=sample["action"],
                    full_email=sample["full_email"],
                    selected_text=sample["selected_text"],
                    tone=sample.get("tone_type")
                )

                # Reconstruct full email with edited selection
                reconstructed_email = (
                    f"{sample['before_selection']}\n"
                    f"{edited_selection}\n"
                    f"{sample['after_selection']}"
                )

                # Simple boundary check
                boundary_check = evaluator.simple_boundary_check(
                    sample["before_selection"],
                    sample["selected_text"],
                    sample["after_selection"],
                    edited_selection
                )

                # Comprehensive LLM evaluation
                llm_eval = evaluator.evaluate_comprehensive(
                    full_email=sample["full_email"],
                    selected_text=sample["selected_text"],
                    model_output=edited_selection,
                    action=sample["action"]
                )

                # Compile result
                result = {
                    "id": sample["id"],
                    "model": args.model,
                    "action": sample["action"],
                    "tone_type": sample.get("tone_type"),
                    "original_selection": sample["selected_text"],
                    "edited_selection": edited_selection,
                    "reconstructed_email": reconstructed_email,
                    "boundary_check": boundary_check,
                    "evaluation": llm_eval
                }

                results.append(result)
                out_file.write(json.dumps(result, ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"\n⚠️  Error processing sample {sample['id']}: {e}")
                continue

    # Summary statistics
    print(f"\n{'='*60}")
    print("📊 EVALUATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total Samples: {len(results)}")
    
    if results:
        # Boundary check stats
        correctly_scoped = sum(1 for r in results if r["boundary_check"]["correctly_scoped"])
        print(f"\n🎯 Boundary Preservation:")
        print(f"  Correctly Scoped: {correctly_scoped}/{len(results)} ({correctly_scoped/len(results)*100:.1f}%)")
        
        # Average scores
        if all(r["evaluation"] for r in results):
            avg_scores = {}
            metrics = ["selection_boundary_preservation", "edit_quality", 
                      "faithfulness", "completeness", "overall"]
            
            for metric in metrics:
                scores = [r["evaluation"][metric]["score"] for r in results 
                         if r["evaluation"]]
                avg_scores[metric] = sum(scores) / len(scores) if scores else 0
            
            print(f"\n📈 Average Scores:")
            for metric, score in avg_scores.items():
                print(f"  {metric}: {score:.2f}/5")

    print(f"\n✅ Results saved to: {args.output}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
