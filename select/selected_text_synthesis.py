"""
Scenario 1: Selected Text Preservation - Data Synthesis
Generates emails with clearly marked selected portions for testing
whether models edit only the selected text.
"""

import os
import json
import random
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

load_dotenv()


class SelectedTextEmailGenerator:
    """Generates emails with selected portions for Scenario 1 testing."""
    
    def __init__(self, model_name):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.model = model_name

    def _call_api(self, messages, temperature=0.8):
        """Internal API call method."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    def generate_full_email(self, topic, persona, tone, length):
        """Generate a complete email."""
        prompt = (
            "You are an email writing assistant.\n\n"
            f"Topic: {topic}\n"
            f"Author persona: {persona}\n"
            f"Tone: {tone}\n"
            f"Target length: approximately {length} words\n\n"
            "Generate a well-structured professional email with:\n"
            "- A greeting (e.g., 'Hi [Name],' or 'Dear Team,')\n"
            "- 2-3 body paragraphs with clear content\n"
            "- A closing (e.g., 'Best regards,' or 'Thanks,')\n"
            "- A signature line\n\n"
            "Make sure each paragraph is distinct and meaningful.\n"
            "Return only the email content."
        )
        return self._call_api([{"role": "user", "content": prompt}])

    def extract_selection(self, full_email):
        """
        Extract a meaningful middle portion from the email.
        Returns: (before, selection, after) tuple
        """
        lines = [line for line in full_email.split('\n') if line.strip()]
        
        if len(lines) < 5:
            # If email is too short, select middle line
            mid = len(lines) // 2
            return (
                '\n'.join(lines[:mid]),
                lines[mid],
                '\n'.join(lines[mid+1:])
            )
        
        # For longer emails, select middle paragraphs (avoid greeting/closing)
        # Typically: greeting is first 1-2 lines, closing is last 1-2 lines
        start_idx = min(2, len(lines) // 4)
        end_idx = max(len(lines) - 2, len(lines) * 3 // 4)
        
        selected_lines = lines[start_idx:int(end_idx)]
        
        # Take 1-3 consecutive lines as selection
        selection_length = random.randint(1, min(3, len(selected_lines)))
        selection_start = random.randint(0, len(selected_lines) - selection_length)
        
        actual_selection_start = start_idx + selection_start
        actual_selection_end = actual_selection_start + selection_length
        
        return (
            '\n'.join(lines[:actual_selection_start]),
            '\n'.join(lines[actual_selection_start:actual_selection_end]),
            '\n'.join(lines[actual_selection_end:])
        )


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate Scenario 1 dataset for selected text preservation testing."
    )
    parser.add_argument("--count", type=int, default=50, 
                        help="Number of samples to generate")
    parser.add_argument("--output", type=str, default="selected_text_dataset.jsonl",
                        help="Output file path")
    args = parser.parse_args()

    # Configuration
    personas = [
        "a marketing manager",
        "a product manager",
        "a customer support lead",
        "a sales executive",
        "an HR manager",
        "a project coordinator",
        "a team leader",
        "a consultant",
        "an account manager",
        "a CEO"
    ]

    tones = [
        "professional",
        "friendly",
        "formal",
        "persuasive",
        "empathetic",
        "urgent",
        "diplomatic"
    ]

    topics = [
        "Requesting feedback on a proposal",
        "Following up after a meeting",
        "Announcing a policy update",
        "Coordinating a project deadline",
        "Addressing a customer concern",
        "Sharing team updates",
        "Proposing a partnership",
        "Scheduling a review meeting",
        "Requesting budget approval",
        "Introducing a new process"
    ]

    actions = ["shorten_selection", "lengthen_selection", "tone_selection"]
    tone_options = ["friendly", "formal", "concise", "detailed"]
    
    lengths = [100, 120, 150, 180, 200]

    # Initialize generator
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
    generator = SelectedTextEmailGenerator(model_name)

    print(f"🚀 Generating {args.count} samples for Scenario 1...")
    print(f"📝 Using model: {model_name}")
    print(f"💾 Output: {args.output}\n")

    with open(args.output, "w", encoding="utf-8") as file:
        for i in tqdm(range(args.count), desc="Generating", unit="sample"):
            try:
                # Generate full email
                topic = random.choice(topics)
                persona = random.choice(personas)
                tone = random.choice(tones)
                length = random.choice(lengths)
                
                full_email = generator.generate_full_email(topic, persona, tone, length)
                
                # Extract selection
                before, selection, after = generator.extract_selection(full_email)
                
                # Choose action
                action = random.choice(actions)
                tone_type = random.choice(tone_options) if action == "tone_selection" else None
                
                # Create record
                record = {
                    "id": i + 1,
                    "topic": topic,
                    "persona": persona,
                    "tone": tone,
                    "action": action,
                    "tone_type": tone_type,
                    "full_email": full_email,
                    "before_selection": before,
                    "selected_text": selection,
                    "after_selection": after
                }
                
                file.write(json.dumps(record, ensure_ascii=False) + "\n")
                
            except Exception as e:
                print(f"\n⚠️  Error generating sample {i+1}: {e}")
                continue

    print(f"\n✅ Dataset generation complete!")
    print(f"📊 Generated {args.count} samples")
    print(f"💾 Saved to: {args.output}")


if __name__ == "__main__":
    main()
