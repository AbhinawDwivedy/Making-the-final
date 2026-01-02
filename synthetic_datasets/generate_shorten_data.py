# """
# Synthetic Data Generator for Email Shortening Task
# Generates overly long, verbose emails (150–200 words) that need to be shortened.
# Each JSONL line contains strictly:
# {"id": int, "sender": str, "subject": str, "content": str}
# """

# import os
# import json
# import random
# import time
# from openai import OpenAI
# from dotenv import load_dotenv
# from tqdm import tqdm

# load_dotenv()

# # ---------------- CONFIG ----------------

# NUM_SAMPLES = 50
# OUTPUT_FILE = "synthetic_shorten.jsonl"
# MAX_RETRIES = 3
# SEED = 42

# random.seed(SEED)

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url=os.getenv("OPENAI_API_BASE")
# )

# MODEL = os.getenv("OPENAI_DATAGEN_MODEL", "gpt-4.1")

# # ---------------- HARD-LOCK SYSTEM PROMPT ----------------

# SYSTEM_PROMPT = """You are a high-quality synthetic data generator.

# Your task is to generate REALISTIC, HUMAN-WRITTEN emails that are
# CLEARLY TOO LONG and NEED TO BE SHORTENED.

# HARD LENGTH CONSTRAINT (MANDATORY):
# - Email body MUST be between 150 and 200 WORDS.
# - Outputs outside this range are INVALID.

# STYLE REQUIREMENTS:
# - Emails must be verbose, repetitive, and over-explained.
# - Include unnecessary background, justifications, and tangents.
# - Do NOT be concise.
# - Do NOT summarize.
# - Do NOT explain what you are doing.
# - Do NOT add commentary.

# OUTPUT RULES:
# - Output VALID JSON ONLY
# - Allowed keys: sender, subject, content
# """

# # ---------------- FEW-SHOT EXAMPLES ----------------

# FEW_SHOT_EXAMPLES = [
#     {
#         "role": "assistant",
#         "content": json.dumps({
#             "sender": "overexplaining.manager@company.com",
#             "subject": "project update and background",
#             "content": "Hi everyone, I wanted to take some time to provide a thorough update on the project, even though parts of this may already be familiar to you. When we first discussed this initiative a few weeks ago, there were several assumptions made that I think are worth revisiting in detail. Over the past few days I’ve had multiple conversations that reminded me how important it is to restate the full background so no one feels out of the loop. This email might be longer than necessary, but I believe it’s helpful to walk through every step that led us here before getting to the actual point."
#         })
#     }
# ]

# # ---------------- DIVERSITY AXES ----------------

# SCENARIOS = [
#     "Project status update",
#     "Meeting recap",
#     "Request for clarification",
#     "Proposal explanation",
#     "Follow-up email",
#     "Instructional email",
#     "Approval request",
#     "Complaint explanation",
#     "Deadline discussion",
#     "Thank-you note"
# ]

# PERSONAS = [
#     "overexplaining manager",
#     "anxious employee",
#     "detail-obsessed analyst",
#     "long-winded executive",
#     "verbose academic",
#     "chatty colleague",
#     "over-communicating team lead",
#     "apologetic junior staff",
#     "rambling customer",
#     "formal consultant"
# ]

# CONTEXTS = [
#     "simple update turned into an essay",
#     "basic question wrapped in long context",
#     "short request with excessive background",
#     "routine follow-up with repeated points",
#     "straightforward message over-justified",
#     "simple confirmation bloated with detail",
#     "quick note expanded unnecessarily",
#     "minor issue explained at length",
#     "basic approval request over-explained",
#     "short thank-you stretched too far"
# ]

# TONES = [
#     "formal",
#     "friendly",
#     "urgent",
#     "polite",
#     "apologetic",
#     "enthusiastic"
# ]

# # ---------------- GENERATION FUNCTION ----------------

# def generate_sample(index):
#     scenario = random.choice(SCENARIOS)
#     persona = random.choice(PERSONAS)
#     context = random.choice(CONTEXTS)
#     tone = random.choice(TONES)

#     user_prompt = f"""
# Persona: {persona}
# Scenario: {scenario}
# Context: {context}
# Tone: {tone}

# Write a verbose email in the specified tone.
# The email MUST be between 150 and 200 words and clearly need shortening.
# Return JSON ONLY with keys: sender, subject, content.
# """

#     for attempt in range(1, MAX_RETRIES + 1):
#         try:
#             response = client.chat.completions.create(
#                 model=MODEL,
#                 messages=[
#                     {"role": "system", "content": SYSTEM_PROMPT},
#                     *FEW_SHOT_EXAMPLES,
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 temperature=0.9,
#                 response_format={"type": "json_object"}
#             )

#             data = json.loads(response.choices[0].message.content)

#             if not all(k in data for k in ("sender", "subject", "content")):
#                 continue

#             word_count = len(data["content"].split())
#             if not (150 <= word_count <= 200):
#                 continue

#             return {
#                 "id": index,
#                 "sender": data["sender"],
#                 "subject": data["subject"],
#                 "content": data["content"]
#             }

#         except Exception as e:
#             if attempt == MAX_RETRIES:
#                 raise RuntimeError(f"Sample {index} failed: {e}")
#             time.sleep(0.5)

# # ---------------- MAIN ----------------

# def main():
#     print(f"🚀 Generating {NUM_SAMPLES} shortening samples")
#     print(f"📌 Model: {MODEL}")
#     print(f"🎲 Seed: {SEED}")

#     dataset = []
#     i = 1

#     with tqdm(total=NUM_SAMPLES) as pbar:
#         while len(dataset) < NUM_SAMPLES:
#             sample = generate_sample(i)
#             dataset.append(sample)
#             i += 1
#             pbar.update(1)

#     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#         for row in dataset:
#             f.write(json.dumps(row, ensure_ascii=False) + "\n")

#     print(f"\n✅ Saved {len(dataset)} samples to {OUTPUT_FILE}")

# if __name__ == "__main__":
#     main()
"""
Synthetic Data Generator for Email Shortening Task
Generates overly long, verbose emails (150–200 words) that need to be shortened.
Each JSONL line contains strictly:
{"id": int, "sender": str, "subject": str, "content": str}
"""

import os
import json
import random
import time
import re
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# ---------------- CONFIG ----------------

NUM_SAMPLES = 50
OUTPUT_FILE = "synthetic_shorten.jsonl"
MAX_RETRIES = 3
SEED = 42

random.seed(SEED)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

MODEL = os.getenv("OPENAI_DATAGEN_MODEL", "gpt-4.1")

# ---------------- NAME + DOMAIN POOLS ----------------

FIRST_NAMES = [
    "Alex", "Jordan", "Sam", "Chris", "Taylor", "Morgan", "Riley",
    "Ava", "Emma", "Olivia", "Noah", "Liam", "Ethan", "Mia", "Sophia",
    "Daniel", "Lucas", "Arjun", "Rohan", "Ananya", "Neha", "Rahul"
]

LAST_NAMES = [
    "Smith", "Johnson", "Brown", "Williams", "Miller", "Davis",
    "Anderson", "Clark", "Lopez", "Patel", "Sharma", "Gupta", "Verma"
]

DOMAINS = [
    "gmail.com",
    "outlook.com",
    "company.com",
    "corpmail.com",
    "business.org",
    "workmail.com"
]

EMAIL_REGEX = re.compile(r"^[a-z]+(\.[a-z]+)?@[a-z0-9.-]+\.[a-z]{2,}$")

def generate_realistic_sender():
    first = random.choice(FIRST_NAMES).lower()
    last = random.choice(LAST_NAMES).lower()
    domain = random.choice(DOMAINS)
    return f"{first}.{last}@{domain}"

# ---------------- HARD-LOCK SYSTEM PROMPT ----------------

SYSTEM_PROMPT = """You are a high-quality synthetic data generator.

Your task is to generate REALISTIC, HUMAN-WRITTEN emails that are
CLEARLY TOO LONG and NEED TO BE SHORTENED.

HARD LENGTH CONSTRAINT (MANDATORY):
- Email body MUST be between 150 and 200 WORDS.
- Outputs outside this range are INVALID.

STYLE REQUIREMENTS:
- Emails must be verbose, repetitive, and over-explained.
- Include unnecessary background, justifications, and tangents.
- Do NOT be concise.
- Do NOT summarize.
- Do NOT explain what you are doing.
- Do NOT add commentary.

OUTPUT RULES:
- Output VALID JSON ONLY
- Allowed keys: sender, subject, content
"""

# ---------------- FEW-SHOT (FIXED SENDER) ----------------

FEW_SHOT_EXAMPLES = [
    {
        "role": "assistant",
        "content": json.dumps({
            "sender": "alex.johnson@company.com",
            "subject": "project update and background",
            "content": "Hi everyone, I wanted to take some time to provide a thorough update on the project, even though parts of this may already be familiar to you. When we first discussed this initiative a few weeks ago, there were several assumptions made that I think are worth revisiting in detail. Over the past few days I’ve had multiple conversations that reminded me how important it is to restate the full background so no one feels out of the loop. This email might be longer than necessary, but I believe it’s helpful to walk through every step that led us here before getting to the actual point."
        })
    }
]

# ---------------- DIVERSITY AXES ----------------

SCENARIOS = [
    "Project status update",
    "Meeting recap",
    "Request for clarification",
    "Proposal explanation",
    "Follow-up email",
    "Instructional email",
    "Approval request",
    "Complaint explanation",
    "Deadline discussion",
    "Thank-you note"
]

PERSONAS = [
    "overexplaining manager",
    "anxious employee",
    "detail-obsessed analyst",
    "long-winded executive",
    "verbose academic",
    "chatty colleague",
    "over-communicating team lead",
    "apologetic junior staff",
    "rambling customer",
    "formal consultant"
]

CONTEXTS = [
    "simple update turned into an essay",
    "basic question wrapped in long context",
    "short request with excessive background",
    "routine follow-up with repeated points",
    "straightforward message over-justified",
    "simple confirmation bloated with detail",
    "quick note expanded unnecessarily",
    "minor issue explained at length",
    "basic approval request over-explained",
    "short thank-you stretched too far"
]

TONES = [
    "formal",
    "friendly",
    "urgent",
    "polite",
    "apologetic",
    "enthusiastic"
]

# ---------------- GENERATION FUNCTION ----------------

def generate_sample(index):
    scenario = random.choice(SCENARIOS)
    persona = random.choice(PERSONAS)
    context = random.choice(CONTEXTS)
    tone = random.choice(TONES)
    sender = generate_realistic_sender()

    user_prompt = f"""
Persona: {persona}
Scenario: {scenario}
Context: {context}
Tone: {tone}

Write a verbose email in the specified tone.
The email MUST be between 150 and 200 words and clearly need shortening.
Use this sender email exactly: {sender}
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

            if not all(k in data for k in ("sender", "subject", "content")):
                continue

            if not EMAIL_REGEX.match(data["sender"]):
                continue

            word_count = len(data["content"].split())
            if not (150 <= word_count <= 200):
                continue

            return {
                "id": index,
                "sender": data["sender"],
                "subject": data["subject"],
                "content": data["content"]
            }

        except Exception:
            if attempt == MAX_RETRIES:
                raise
            time.sleep(0.5)

# ---------------- MAIN ----------------

def main():
    print(f"🚀 Generating {NUM_SAMPLES} shortening samples")
    print(f"📌 Model: {MODEL}")
    print(f"🎲 Seed: {SEED}")

    dataset = []
    i = 1

    with tqdm(total=NUM_SAMPLES) as pbar:
        while len(dataset) < NUM_SAMPLES:
            dataset.append(generate_sample(i))
            i += 1
            pbar.update(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for row in dataset:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"\n✅ Saved {len(dataset)} samples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
