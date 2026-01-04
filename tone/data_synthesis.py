# import os
# import json
# import random
# from dotenv import load_dotenv
# from openai import OpenAI
# from tqdm import tqdm

# load_dotenv()


# # ==================================================
# # COMPACT GOLD SYNTHESIS CONFIG (10 EACH)
# # ==================================================
# SYNTHESIS_CONFIG = {

#     "target_tones": [
#         "professional",
#         "friendly",
#         "sympathetic"
#     ],

#     "tone_map": {
#         "professional": [
#             "angry",
#             "rude",
#             "passive_aggressive",
#             "impatient"
#         ],
#         "friendly": [
#             "overly_casual",
#             "slang_heavy",
#             "careless"
#         ],
#         "sympathetic": [
#             "emotional",
#             "anxious",
#             "burnt_out"
#         ]
#     },

#     "personas": [
#         "angry_manager",
#         "careless_colleague",
#         "frustrated_intern",
#         "burnt_out_employee",
#         "anxious_employee",
#         "rude_client",
#         "demanding_customer",
#         "panicked_student",
#         "emotional_research_assistant",
#         "startup_founder_under_pressure"
#     ],

#     "topics": [
#         "missed_deadline",
#         "payment_delay",
#         "poor_quality_work",
#         "meeting_missed",
#         "approval_delay",
#         "service_dissatisfaction",
#         "assignment_extension",
#         "exam_absence",
#         "health_emergency",
#         "apology_after_rude_email"
#     ],

#     "edge_cases": [
#         "all_caps_shouting",
#         "excessive_exclamation",
#         "no_punctuation",
#         "one_line_email",
#         "broken_grammar",
#         "emoji_overuse",
#         "slang_abbreviations",
#         "blame_language",
#         "multiple_apologies",
#         "overly_emotional_language"
#     ]
# }


# # ==================================================
# # HELPERS
# # ==================================================
# def random_sender(persona: str) -> str:
#     base = persona.replace("_", "")
#     domains = ["company.com", "clientmail.com", "university.edu", "startup.io"]
#     return f"{base}@{random.choice(domains)}"


# def subject_from_topic(topic: str) -> str:
#     return topic.replace("_", " ").title()


# # ==================================================
# # EMAIL GENERATOR
# # ==================================================
# class GenerateEmail:
#     def __init__(self, model_name):
#         self.client = OpenAI(
#             api_key=os.getenv("OPENAI_API_KEY"),
#             base_url=os.getenv("OPENAI_API_BASE")
#         )
#         self.model = model_name

#     def send_prompt(self, prompt):
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.85
#         )
#         return response.choices[0].message.content.strip()

#     def generate(self, persona, topic, input_tone, edge_cases):
#         prompt = f"""
# Write an UNPROFESSIONAL email.

# Persona: {persona}
# Topic: {topic}
# Tone: {input_tone}

# Intentionally include the following issues:
# {", ".join(edge_cases)}

# Rules:
# - Do NOT correct the tone
# - Sound like a real stressed human
# - Do NOT add greetings or signatures unless natural
# - Return ONLY the email body text
# """
#         return self.send_prompt(prompt)


# # ==================================================
# # MAIN
# # ==================================================
# def main():
#     import argparse
#     parser = argparse.ArgumentParser(description="Generate compact gold synthetic email dataset")
#     parser.add_argument("--count", type=int, default=75)
#     args = parser.parse_args()

#     model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
#     generator = GenerateEmail(model_name)

#     with open("tone_synthetic.jsonl", "w", encoding="utf-8") as file:
#         for i in tqdm(range(args.count), desc="Generating emails"):

#             target_tone = random.choice(SYNTHESIS_CONFIG["target_tones"])
#             input_tone = random.choice(SYNTHESIS_CONFIG["tone_map"][target_tone])

#             persona = random.choice(SYNTHESIS_CONFIG["personas"])
#             topic = random.choice(SYNTHESIS_CONFIG["topics"])
#             edge_cases = random.sample(
#                 SYNTHESIS_CONFIG["edge_cases"],
#                 k=random.choice([1, 2])
#             )

#             try:
#                 content = generator.generate(
#                     persona=persona,
#                     topic=topic,
#                     input_tone=input_tone,
#                     edge_cases=edge_cases
#                 )

#                 record = {
#                     "id": i + 1,
#                     "sender": random_sender(persona),
#                     "subject": subject_from_topic(topic),
#                     "content": content
#                 }

#                 file.write(json.dumps(record, ensure_ascii=False) + "\n")

#             except Exception as e:
#                 print(f"Error at {i+1}: {e}")

#     print("✅ Dataset generation complete → tone_synthetic.jsonl")


# if __name__ == "__main__":
#     main()
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
        "professional", "friendly", "sympathetic"
    ],
    "tone_map": {
        "professional": ["angry", "rude", "passive_aggressive", "impatient"],
        "friendly": ["overly_casual", "slang_heavy", "careless"],
        "sympathetic": ["emotional", "anxious", "burnt_out"]
    },
    "personas": [
        "angry_manager", "careless_colleague", "frustrated_intern",
        "burnt_out_employee", "anxious_employee", "rude_client",
        "demanding_customer", "panicked_student", "emotional_research_assistant",
        "startup_founder_under_pressure"
    ],
    "topics": [
        "missed_deadline", "payment_delay", "poor_quality_work",
        "meeting_missed", "approval_delay", "service_dissatisfaction",
        "assignment_extension", "exam_absence", "health_emergency",
        "apology_after_rude_email"
    ],
    "edge_cases": [
        "all_caps_shouting", "excessive_exclamation", "no_punctuation",
        "one_line_email", "broken_grammar", "emoji_overuse",
        "slang_abbreviations", "blame_language", "multiple_apologies",
        "overly_emotional_language"
    ]
}

# ==================================================
# REALISTIC NAME DATA
# ==================================================
FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Melissa", "George", "Deborah"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
]

# ==================================================
# HELPERS
# ==================================================
def random_sender(persona: str) -> str:
    """Generates a realistic email address based on persona type."""
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    
    # Randomize username format
    format_style = random.choice(["dot", "initial", "full", "num"])
    if format_style == "dot":
        username = f"{fname}.{lname}"
    elif format_style == "initial":
        username = f"{fname[0]}{lname}"
    elif format_style == "full":
        username = f"{fname}{lname}"
    else:
        username = f"{fname}.{lname}{random.randint(1, 99)}"

    # Context-aware domain selection
    if "student" in persona or "research" in persona:
        domain = random.choice(["university.edu", "campus.edu", "student.college.edu"])
    elif "manager" in persona or "employee" in persona or "intern" in persona or "founder" in persona:
        domain = random.choice(["company.com", "startup.io", "corp.net", "bizflow.com", "techs.io"])
    else: # Clients, customers, regular people
        domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"])

    return f"{username.lower()}@{domain}"

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
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.85
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI Error: {e}")
            return ""

    def generate(self, persona, topic, input_tone, edge_cases):
        prompt = f"""
Write an UNPROFESSIONAL email.

Persona Context: {persona.replace('_', ' ')}
Topic: {topic}
Tone: {input_tone}

Intentionally include the following issues:
{", ".join(edge_cases)}

Rules:
- Do NOT correct the tone
- Sound like a real stressed human
- Do NOT add greetings or signatures unless natural for the tone
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

    # Use a set to track IDs to ensure distinctness if needed, though i index is sufficient
    print(f"Starting generation of {args.count} emails...")

    with open("tone_synthetic.jsonl", "w", encoding="utf-8") as file:
        for i in tqdm(range(args.count), desc="Generating emails"):

            target_tone = random.choice(SYNTHESIS_CONFIG["target_tones"])
            input_tone = random.choice(SYNTHESIS_CONFIG["tone_map"][target_tone])

            persona = random.choice(SYNTHESIS_CONFIG["personas"])
            topic = random.choice(SYNTHESIS_CONFIG["topics"])
            
            # Select 1 or 2 edge cases
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

                if not content:
                    print(f"Skipping item {i+1} due to empty generation.")
                    continue

                record = {
                    "id": i + 1,
                    # This now calls the realistic sender function
                    "sender": random_sender(persona), 
                    "subject": subject_from_topic(topic),
                    "content": content,
                    # Optional: Save metadata for your own reference (don't train on this)
                    "metadata": {
                        "persona_type": persona,
                        "target_tone": target_tone,
                        "input_tone": input_tone
                    }
                }

                file.write(json.dumps(record, ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"Error at {i+1}: {e}")

    print("✅ Dataset generation complete → tone_synthetic.jsonl")

if __name__ == "__main__":
    main()