"""
Synthetic Data Generator for Email Tone Change Task
Generates lazy, rude, emotional, unprofessional emails for tone transformation.
Each JSONL line contains strictly:
{"id": int, "sender": str, "subject": str, "content": str}
"""

import os
import json
import random
import time
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# ---------------- CONFIG ----------------

NUM_SAMPLES = 50
OUTPUT_FILE = "synthetic_tone.jsonl"
MAX_RETRIES = 3
SEED = 42

random.seed(SEED)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

MODEL = os.getenv("OPENAI_DATAGEN_MODEL", "gpt-4.1")

# ---------------- HARD-LOCK SYSTEM PROMPT ----------------

SYSTEM_PROMPT = """You are a high-quality synthetic data generator.

Your task is to generate REALISTIC, HUMAN-WRITTEN email drafts that have
CLEARLY INAPPROPRIATE or UNPROFESSIONAL TONES.

CRITICAL RULES:
- Outputs must feel human, messy, emotional, or rude.
- Do NOT sound polite, professional, or AI-written.
- Use frustration, sarcasm, entitlement, or aggression when appropriate.
- Emails should feel like something a real annoyed person typed quickly.
- NEVER explain what you are doing.
- NEVER add commentary.
- Output VALID JSON ONLY with keys: sender, subject, content
"""

# ---------------- FEW-SHOT EXAMPLES ----------------

FEW_SHOT_EXAMPLES = [
    {
        "role": "assistant",
        "content": json.dumps({
            "sender": "angry.customer@email.com",
            "subject": "this is ridiculous",
            "content": "ive emailed twice already and no one bothered replying. this whole thing is a mess and honestly super annoying. not sure why this is so hard to fix."
        })
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "sender": "mike.ops@companymail.com",
            "subject": "re: meeting",
            "content": "you missed the meeting again. not sure if you just dont care or what but this keeps happening. getting pretty tired of chasing this."
        })
    }
]

# ---------------- DIVERSITY AXES ----------------

SOURCE_TONES = [
    "rude and aggressive",
    "overly casual and unprofessional",
    "extremely emotional and panicked",
    "passive-aggressive",
    "dismissive and condescending",
    "angry and demanding",
    "whiny and complaining",
    "sarcastic and bitter",
    "frustrated and impatient",
    "cold and hostile"
]

SCENARIOS = [
    "Complaint about service quality",
    "Request for deadline extension",
    "Response to missed meeting",
    "Feedback on poor work quality",
    "Request for payment",
    "Notification of absence or delay",
    "Disagreement with decision",
    "Request for approval",
    "Follow-up on unanswered email",
    "Report of technical issue"
]

PERSONAS = [
    "frustrated customer",
    "burnt-out employee",
    "aggressive manager",
    "entitled client",
    "stressed student",
    "impatient vendor",
    "annoyed team member",
    "defensive colleague",
    "demanding stakeholder",
    "irritated user"
]

INPUT_STYLES = [
    "rushed",
    "lowercase lazy",
    "emotionally charged",
    "blunt and short-tempered",
    "sarcastic",
    "complaining rant"
]

# ---------------- GENERATION FUNCTION ----------------

def generate_sample(index):
    source_tone = random.choice(SOURCE_TONES)
    scenario = random.choice(SCENARIOS)
    persona = random.choice(PERSONAS)
    style = random.choice(INPUT_STYLES)

    user_prompt = f"""
Persona: {persona}
Scenario: {scenario}
Source Tone: {source_tone}
Style: {style}

Write an email that clearly needs its tone fixed.
The email should be 4–8 sentences.
Return JSON ONLY with keys: sender, subject, content.
"""

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *FEW_SHOT_EXAMPLES,
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.9,
                response_format={"type": "json_object"}
            )

            data = json.loads(response.choices[0].message.content)

            # Ensure only required keys exist
            if all(k in data for k in ("sender", "subject", "content")):
                return {
                    "id": index,
                    "sender": data["sender"],
                    "subject": data["subject"],
                    "content": data["content"]
                }

        except Exception as e:
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"Sample {index} failed: {e}")
            time.sleep(0.5)

# ---------------- MAIN ----------------

def main():
    print(f"🚀 Generating {NUM_SAMPLES} tone-change samples")
    print(f"📌 Model: {MODEL}")
    print(f"🎲 Seed: {SEED}")

    dataset = []
    i = 1

    with tqdm(total=NUM_SAMPLES) as pbar:
        while len(dataset) < NUM_SAMPLES:
            sample = generate_sample(i)
            dataset.append(sample)
            i += 1
            pbar.update(1)

    # Write strictly in the required JSONL format
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for row in dataset:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"\n✅ Saved {len(dataset)} samples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
