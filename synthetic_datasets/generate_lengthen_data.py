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
OUTPUT_FILE = "synthetic_length.jsonl"
MAX_RETRIES = 3
SEED = 42

random.seed(SEED)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

MODEL = os.getenv("OPENAI_DATAGEN_MODEL")

if not MODEL:
    raise RuntimeError("OPENAI_DATAGEN_MODEL not set in .env")

# ---------------- HARD-LOCK SYSTEM PROMPT ----------------

SYSTEM_PROMPT = """You are a high-quality synthetic data generator.

Your task is to generate REALISTIC, HUMAN-WRITTEN email drafts that represent
what a lazy, rushed, or imperfect user might type before asking an AI to
“lengthen” or improve the email.

CRITICAL RULES:
- Outputs must feel human, imperfect, and natural.
- Avoid polished, AI-like, or overly complete writing unless explicitly required.
- Match the requested tone, persona, style, and target length.
- The email body should often feel under-written, informal, emotional, or incomplete.
- Use abbreviations, lowercase, shorthand, bullet points, or rough phrasing when appropriate.
- NEVER explain what you are doing.
- NEVER include extra commentary.
- Output VALID JSON ONLY.

You must strictly follow the requested TARGET LENGTH range.
If unsure, undershoot slightly rather than overshoot.

The JSON must contain exactly:
- sender (realistic email address)
- subject (short and realistic)
- content (email body only)
"""

# ---------------- FEW-SHOT EXAMPLES ----------------

FEW_SHOT_EXAMPLES = [
    {
        "role": "assistant",
        "content": json.dumps(
            {
                "sender": "tom.k@startupmail.com",
                "subject": "deadline",
                "content": "missed the deadline today. not sure next steps. sorry about that."
            }
        )
    },
    {
        "role": "assistant",
        "content": json.dumps(
            {
                "sender": "priya.dev@cloudops.io",
                "subject": "prod issue",
                "content": "svc went down around 2am. tried restart, didnt help. logs weird. might be my deploy. pls advise asap."
            }
        )
    }
]

# ---------------- DIVERSITY AXES ----------------

TONES = [
    "Urgent", "Annoyed", "Casual", "Apologetic", "Confused",
    "Demanding", "Neutral", "Enthusiastic", "Professional",
    "Hesitant", "Passive-Aggressive"
]

PERSONAS = [
    "Busy CEO", "Nervous Intern", "Angry Customer", "Strict HR",
    "Sales Rep", "Tired Parent", "Software Engineer", "Event Planner"
]

CONTEXTS = [
    "Missed deadline", "Refund request", "Scheduling sync", "Server crash",
    "Invoice error", "Rejecting offer", "Feedback", "Sick leave",
    "Thank you", "Ghosted email follow-up"
]

INPUT_STYLES = [
    "Lazy (lowercase)", "Bullet points", "Broken English",
    "Rude/Blunt", "Cryptic Shorthand", "Standard", "Rushed Mobile"
]

# ---------------- LENGTH CONTROL ----------------

LENGTH_TARGETS = [
    "Ultra-Short (5-15 words)",
    "Ultra-Short (5-15 words)",
    "Short (25-40 words)",
    "Short (25-40 words)",
    "Medium (50-80 words)",
    "Long Rough Draft (90-120 words)"
]

LENGTH_RANGES = {
    "Ultra-Short": (5, 15),
    "Short": (25, 40),
    "Medium": (50, 80),
    "Long Rough Draft": (90, 120)
}

def extract_length_key(label):
    for key in LENGTH_RANGES:
        if key in label:
            return key
    raise ValueError(f"Unknown length label: {label}")

def valid_length(text, length_key):
    lo, hi = LENGTH_RANGES[length_key]
    wc = len(text.split())
    return lo <= wc <= hi

# ---------------- SAMPLE GENERATION ----------------

def generate_sample(index):
    persona = random.choice(PERSONAS)
    context = random.choice(CONTEXTS)
    tone = random.choice(TONES)
    style = random.choice(INPUT_STYLES)
    length_label = random.choice(LENGTH_TARGETS)
    length_key = extract_length_key(length_label)

    user_prompt = f"""
Persona: {persona}
Context: {context}
Tone: {tone}
Style: {style}
TARGET LENGTH: {length_label} (STRICT)

Generate a lazy, imperfect draft email.
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
            content = data.get("content", "")

            if not valid_length(content, length_key):
                continue

            return {
                "id": index,
                "sender": data.get("sender"),
                "subject": data.get("subject"),
                "content": content
            }

        except Exception as e:
            if attempt == MAX_RETRIES:
                raise RuntimeError(
                    f"Sample {index} failed after {MAX_RETRIES} retries: {e}"
                )
            time.sleep(0.5)

# ---------------- MAIN ----------------

def main():
    print(f"🚀 Generating {NUM_SAMPLES} samples")
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

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for row in dataset:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"\n✅ Saved {len(dataset)} samples to {OUTPUT_FILE}")

 

if __name__ == "__main__":
    main()
