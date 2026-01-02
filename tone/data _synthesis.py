import os
import json
import random
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

load_dotenv()


# ==================================================
# COMPACT GOLD SYNTHESIS CONFIG (10 EACH)
# ==================================================
SYNTHESIS_CONFIG = {

    "target_tones": [
        "professional",
        "friendly",
        "sympathetic"
    ],

    "tone_map": {
        "professional": [
            "angry",
            "rude",
            "passive_aggressive",
            "impatient"
        ],
        "friendly": [
            "overly_casual",
            "slang_heavy",
            "careless"
        ],
        "sympathetic": [
            "emotional",
            "anxious",
            "burnt_out"
        ]
    },

    "personas": [
        "angry_manager",
        "careless_colleague",
        "frustrated_intern",
        "burnt_out_employee",
        "anxious_employee",
        "rude_client",
        "demanding_customer",
        "panicked_student",
        "emotional_research_assistant",
        "startup_founder_under_pressure"
    ],

    "topics": [
        "missed_deadline",
        "payment_delay",
        "poor_quality_work",
        "meeting_missed",
        "approval_delay",
        "service_dissatisfaction",
        "assignment_extension",
        "exam_absence",
        "health_emergency",
        "apology_after_rude_email"
    ],

    "edge_cases": [
        "all_caps_shouting",
        "excessive_exclamation",
        "no_punctuation",
        "one_line_email",
        "broken_grammar",
        "emoji_overuse",
        "slang_abbreviations",
        "blame_language",
        "multiple_apologies",
        "overly_emotional_language"
    ]
}


# ==================================================
# HELPERS
# ==================================================
def random_sender(persona: str) -> str:
    base = persona.replace("_", "")
    domains = ["company.com", "clientmail.com", "university.edu", "startup.io"]
    return f"{base}@{random.choice(domains)}"


def subject_from_topic(topic: str) -> str:
    return topic.replace("_", " ").title()


# ==================================================
# EMAIL GENERATOR
# ==================================================
class GenerateEmail:
    def __init__(self, model_name):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.model = model_name

    def send_prompt(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85
        )
        return response.choices[0].message.content.strip()

    def generate(self, persona, topic, input_tone, edge_cases):
        prompt = f"""
Write an UNPROFESSIONAL email.

Persona: {persona}
Topic: {topic}
Tone: {input_tone}

Intentionally include the following issues:
{", ".join(edge_cases)}

Rules:
- Do NOT correct the tone
- Sound like a real stressed human
- Do NOT add greetings or signatures unless natural
- Return ONLY the email body text
"""
        return self.send_prompt(prompt)


# ==================================================
# MAIN
# ==================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate compact gold synthetic email dataset")
    parser.add_argument("--count", type=int, default=75)
    args = parser.parse_args()

    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
    generator = GenerateEmail(model_name)

    with open("tone_synthetic.jsonl", "w", encoding="utf-8") as file:
        for i in tqdm(range(args.count), desc="Generating emails"):

            target_tone = random.choice(SYNTHESIS_CONFIG["target_tones"])
            input_tone = random.choice(SYNTHESIS_CONFIG["tone_map"][target_tone])

            persona = random.choice(SYNTHESIS_CONFIG["personas"])
            topic = random.choice(SYNTHESIS_CONFIG["topics"])
            edge_cases = random.sample(
                SYNTHESIS_CONFIG["edge_cases"],
                k=random.choice([1, 2])
            )

            try:
                content = generator.generate(
                    persona=persona,
                    topic=topic,
                    input_tone=input_tone,
                    edge_cases=edge_cases
                )

                record = {
                    "id": i + 1,
                    "sender": random_sender(persona),
                    "subject": subject_from_topic(topic),
                    "content": content
                }

                file.write(json.dumps(record, ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"Error at {i+1}: {e}")

    print("✅ Dataset generation complete → tone_synthetic.jsonl")


if __name__ == "__main__":
    main()
