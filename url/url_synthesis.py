# # # # # # import os
# # # # # # import json
# # # # # # import random
# # # # # # from dotenv import load_dotenv
# # # # # # from openai import OpenAI
# # # # # # from tqdm import tqdm

# # # # # # load_dotenv()


# # # # # # class URLEmailGenerator:
# # # # # #     def __init__(self, model_name):
# # # # # #         self.client = OpenAI(
# # # # # #             api_key=os.getenv("OPENAI_API_KEY"),
# # # # # #             base_url=os.getenv("OPENAI_API_BASE")
# # # # # #         )
# # # # # #         self.model = model_name

# # # # # #     def send_prompt(self, prompt):
# # # # # #         response = self.client.chat.completions.create(
# # # # # #             model=self.model,
# # # # # #             messages=[
# # # # # #                 {"role": "user", "content": prompt}
# # # # # #             ],
# # # # # #             temperature=0.8
# # # # # #         )
# # # # # #         return response.choices[0].message.content.strip()

# # # # # #     def generate_email_with_urls(self, topic, persona, tone, length, url_count):
# # # # # #         prompt = (
# # # # # #             "You are an email writing assistant.\n\n"
# # # # # #             f"Topic: {topic}\n"
# # # # # #             f"Author persona: {persona}\n"
# # # # # #             f"Tone: {tone}\n"
# # # # # #             f"Target length: approximately {length} words\n\n"
# # # # # #             f"CRITICAL REQUIREMENT: Include exactly {url_count} realistic, working URLs in the email.\n"
# # # # # #             f"URLs should be:\n"
# # # # # #             f"- Realistic (e.g., https://docs.company.com/guide, https://calendar.app/meeting/abc123)\n"
# # # # # #             f"- Naturally embedded in context (not just listed)\n"
# # # # # #             f"- Varied types (documentation links, meeting links, dashboard URLs, etc.)\n"
# # # # # #             f"- Complete with protocols (https://)\n\n"
# # # # # #             "Generate a clear, well-structured email.\n"
# # # # # #             "Return only the email content."
# # # # # #         )
# # # # # #         return self.send_prompt(prompt)


# # # # # # def main():
# # # # # #     import argparse
# # # # # #     parser = argparse.ArgumentParser(description="Generate URL-rich synthetic email data.")
# # # # # #     parser.add_argument("--count", type=int, default=50, help="Total number of samples to generate")
# # # # # #     args = parser.parse_args()

# # # # # #     personas = [
# # # # # #         "a marketing manager",
# # # # # #         "a startup founder",
# # # # # #         "a product manager",
# # # # # #         "a customer support lead",
# # # # # #         "a sales executive",
# # # # # #         "a software engineer",
# # # # # #         "a project coordinator",
# # # # # #         "an operations manager",
# # # # # #         "a team leader",
# # # # # #         "a business development representative"
# # # # # #     ]

# # # # # #     tones = [
# # # # # #         "professional",
# # # # # #         "friendly",
# # # # # #         "formal",
# # # # # #         "persuasive",
# # # # # #         "informative",
# # # # # #         "enthusiastic",
# # # # # #         "urgent",
# # # # # #         "diplomatic"
# # # # # #     ]

# # # # # #     # Topics specifically designed to naturally include URLs
# # # # # #     topics = [
# # # # # #         "Sharing documentation links for a new feature",
# # # # # #         "Inviting team to a calendar meeting with link",
# # # # # #         "Forwarding important dashboard URLs",
# # # # # #         "Requesting review of online proposal document",
# # # # # #         "Sharing registration link for upcoming webinar",
# # # # # #         "Providing access to project tracking board",
# # # # # #         "Sending conference call details with join link",
# # # # # #         "Sharing company policy update with reference links",
# # # # # #         "Distributing training material URLs",
# # # # # #         "Coordinating via shared document links",
# # # # # #         "Sending customer feedback form link",
# # # # # #         "Sharing quarterly report with supporting links",
# # # # # #         "Providing onboarding resources with URLs",
# # # # # #         "Distributing survey link to team",
# # # # # #         "Sharing competitive analysis with source links"
# # # # # #     ]

# # # # # #     lengths = [100, 120, 150, 180, 200]
    
# # # # # #     # Distribution: shorten (20), lengthen (15), tone (15)
# # # # # #     actions = ["shorten"] * 20 + ["lengthen"] * 15 + ["tone"] * 15
# # # # # #     random.shuffle(actions)

# # # # # #     dataset_size = args.count

# # # # # #     model_name = os.getenv("URL_SYNTHESIS_MODEL")
# # # # # #     if not model_name:
# # # # # #         model_name = "gpt-4.1"
# # # # # #         print(f"URL_SYNTHESIS_MODEL not found in .env, using default: {model_name}")

# # # # # #     generator = URLEmailGenerator(model_name)

# # # # # #     print(f"Generating {dataset_size} URL-rich emails...")
# # # # # #     with open("url_dataset.jsonl", "w", encoding="utf-8") as file:
# # # # # #         for i in tqdm(range(dataset_size), desc="Generating emails", unit="email"):
# # # # # #             # Randomly choose URL count (1-3 URLs per email)
# # # # # #             url_count = random.choice([1, 2, 3])
            
# # # # # #             # Choose action for this sample
# # # # # #             action = actions[i] if i < len(actions) else random.choice(["shorten", "lengthen", "tone"])
            
# # # # # #             # For tone action, pick a specific tone type
# # # # # #             tone_type = random.choice(tones) if action == "tone" else None

# # # # # #             record = {
# # # # # #                 "id": i + 1,
# # # # # #                 "action": action,
# # # # # #                 "tone_type": tone_type,
# # # # # #                 "topic": random.choice(topics),
# # # # # #                 "persona": random.choice(personas),
# # # # # #                 "tone": random.choice(tones),
# # # # # #                 "target_length": random.choice(lengths),
# # # # # #                 "url_count": url_count
# # # # # #             }

# # # # # #             try:
# # # # # #                 email_content = generator.generate_email_with_urls(
# # # # # #                     record["topic"],
# # # # # #                     record["persona"],
# # # # # #                     record["tone"],
# # # # # #                     record["target_length"],
# # # # # #                     record["url_count"]
# # # # # #                 )
# # # # # #                 record["original_email"] = email_content
                
# # # # # #                 file.write(json.dumps(record, ensure_ascii=False) + "\n")
                
# # # # # #             except Exception as e:
# # # # # #                 print(f"\nError generating sample {i+1}: {e}")

# # # # # #     print("\n✅ Dataset generation complete → url_dataset.jsonl")
    
# # # # # #     # Print distribution summary
# # # # # #     print("\n📊 Dataset Distribution:")
# # # # # #     print(f"   Shorten: 20 samples")
# # # # # #     print(f"   Lengthen: 15 samples")
# # # # # #     print(f"   Tone: 15 samples")
# # # # # #     print(f"   Total: {dataset_size} samples")


# # # # # # if __name__ == "__main__":
# # # # # #     main()
# # # # # import os
# # # # # import json
# # # # # import random
# # # # # from dotenv import load_dotenv
# # # # # from openai import OpenAI
# # # # # from tqdm import tqdm

# # # # # load_dotenv()


# # # # # REFERENCE_EMAIL = {
# # # # #     "sender": "elena@blueridgebiotech.com",
# # # # #     "subject": "Lab Test Results and Next Phase Preparation",
# # # # #     "content": (
# # # # #         "Hi team,\n\n"
# # # # #         "The latest batch of lab test results is finally in, and overall the data looks promising. "
# # # # #         "I've compiled a detailed report summarizing the findings, including success rates, anomalies, "
# # # # #         "and environmental conditions recorded during testing.\n\n"
# # # # #         "Please pay special attention to the notes on sample Group C—there were a few unexpected "
# # # # #         "fluctuations that may need closer investigation.\n\n"
# # # # #         "In preparation for the next phase of trials, I’ve outlined a proposed schedule along with "
# # # # #         "material and equipment requirements. Take a moment to review everything and let me know if "
# # # # #         "we need to coordinate additional resources before moving forward.\n\n"
# # # # #         "Looking forward to discussing this in Monday’s sync."
# # # # #     )
# # # # # }


# # # # # GOOD_URL_POOL = [
# # # # #     # A) Plain / Legacy
# # # # #     "01453.com/",
# # # # #     "032255.com/",
# # # # #     "05minute.com/",
# # # # #     "0creditcard.biz/",
# # # # #     "1-kansas.com/",
# # # # #     "1-newjersey.com/",
# # # # #     "10paisa.com/",
# # # # #     "112fm.com/",
# # # # #     "12oclocknews.com/",
# # # # #     "150ninjas.org/",
# # # # #     "1918film.com/",
# # # # #     "1928.info/",
# # # # #     "1crittenden.com/",
# # # # #     "1crowncenter.com/",
# # # # #     "1upmedia.com/",
# # # # #     "1uptest.info/",

# # # # #     # B) Deep paths / old CMS
# # # # #     "07090.blogspot.com/2011/07/westfield-police-officers-vote-no.html",
# # # # #     "1001afilmodyssey.blogspot.com/2010/04/wizard-of-oz-1939.html",
# # # # #     "11d.typepad.com/blog/2006/03/rich_parent_poo.html",
# # # # #     "14for77.blogspot.com/2011/03/2011-kansas-city-royals-prediction.html",
# # # # #     "18thccuisine.blogspot.com/",
# # # # #     "1964topps.wordpress.com/2010/08/07/452-giants-rookie-stars-gil-garridojim-ray-hart/",
# # # # #     "1980toppsbaseball.blogspot.com/2010/06/312-mike-barlow.html",
# # # # #     "1morefilmblog.com/wordpress/johnny-guitar-ray-1954/",

# # # # #     # C) Query params / tracking
# # # # #     "02ec0a3.netsolhost.com/getperson.php?personID=I4920&tree=ncshawfamily",
# # # # #     "0lo5ckgm.gozisanatuza.ru/?n=89425&amp;tid=47936",
# # # # #     "10012.kaluxo.remax-quebec.com/?A9FF0BCB-9683-41D6-955A-F1D9106257E4&lang=EN",
# # # # #     "10704.kaluxo.remax-quebec.com/?00569118-5AAE-48AA-BF94-ADF2D084F50B&lang=EN",
# # # # #     "17441.kaluxo.remax-quebec.com/?42D72F47-640A-4714-A28B-B085C098FAE3&lang=EN",
# # # # #     "17796.kaluxo.remax-quebec.com/?B6693D7A-5046-47B8-A4E5-43DE6037B72D&lang=EN",
# # # # #     "1greengeneration.elementsintime.com/?p=284",
# # # # #     "17hmr.net/index.php?topic=6680.0",

# # # # #     # D) IP-based
# # # # #     "124.105.24.19/",
# # # # #     "141.2.66.26/en/",
# # # # #     "173.193.93.251/our_people/margaret-a-swimmer",
# # # # #     "192.156.19.109/",
# # # # #     "198.164.154.3/~Heritage/RCN/SJ_Built_Frigates.htm",
# # # # #     "199.115.25.156/aqueduct/Stakes/HollieHughes.shtml",

# # # # #     # E) Encoded / special chars
# # # # #     "123movies.info/movie/%c3%83%c5%93%c3%83%c2%a7_yaman_bakire_(1975)_1581424",
# # # # #     "100hot.com/hot100/ws/results/Web/92!FE5%20Montreal/1/302363/RightNav/Relevance/iq=true/zoom=off/qlnk...",
# # # # #     "1957-chevrolet-alternator-conversion.com/wiring.html",
# # # # #     "1337x.org/torrent/239713/Viola-bacia-tutti-Asia-Argento-1998-Ita-sub-Eng-Rus-Thai/",

# # # # #     # F) HTML
# # # # #     '<a href="https://example.com">Click here</a>',
# # # # #     '<a href="https://docs.example.com/api">API Docs</a>',
# # # # #     '<a href="https://example.com/path#anchor">Read More</a>',
# # # # #     '<a href="https://example.com/login?next=/dashboard">Login</a>',
# # # # #     '<a href="http://1-private-detective.tripod.com/oldlook.up.html">Profile</a>',

# # # # #     # G) Markdown
# # # # #     "[Docs](https://docs.example.com)",
# # # # #     "[Pricing](https://example.com/pricing?plan=pro)",
# # # # #     "[Support](https://support.example.com/tickets/new)",
# # # # #     "[Dashboard](https://app.example.com/#/home)",
# # # # #     "[Reset](https://example.com/reset?token=abc123)",

# # # # #     # H) Images
# # # # #     '<img src="https://cdn.example.com/img.png" />',
# # # # #     '<img src="https://images.example.com/banners/sale.jpg">',
# # # # #     '<img src="https://cdn.example.com/assets/icons/icon@2x.png" />',
# # # # #     '<img src="https://example.com/images/logo.svg" />',
# # # # #     '<img src="https://media.example.com/2025/01/header.webp">',
# # # # #     '<img src="https://cdn.example.com/img.png?version=3">',

# # # # #     # I) Short / redirect
# # # # #     "https://bit.ly/3XkP9Qa",
# # # # #     "http://t.co/AbC123",
# # # # #     "https://tinyurl.com/yc4z9abc",
# # # # #     "https://mail.google.com/url?q=https://example.com",
# # # # #     "https://mail.google.com/url?q=https://example.com/pricing&sa=D",

# # # # #     # J) High-risk
# # # # #     "https://example.com/path(1)/details",
# # # # #     "https://example.com/path%20with%20spaces",
# # # # #     "https://example.com/?redirect=https://evil.com",
# # # # #     "https://example.com/?q=<script>alert(1)</script>",
# # # # #     "https://example.com/?a=1&b=2&c=3&d=4&e=5&f=6",
# # # # #     "https://example.com/very/very/very/very/very/long/path/name/index.html",
# # # # # ]


# # # # # class URLEmailGenerator:
# # # # #     def __init__(self, model_name):
# # # # #         self.client = OpenAI(
# # # # #             api_key=os.getenv("OPENAI_API_KEY"),
# # # # #             base_url=os.getenv("OPENAI_API_BASE")
# # # # #         )
# # # # #         self.model = model_name

# # # # #     def send_prompt(self, prompt):
# # # # #         response = self.client.chat.completions.create(
# # # # #             model=self.model,
# # # # #             messages=[{"role": "user", "content": prompt}],
# # # # #             temperature=0.7
# # # # #         )
# # # # #         return response.choices[0].message.content.strip()

# # # # #     def generate_email(self, seed_email=None):
# # # # #         urls = random.sample(GOOD_URL_POOL, random.choice([1, 2, 3]))

# # # # #         prompt = (
# # # # #             "Generate a realistic professional email.\n\n"
# # # # #             "STRICT RULES:\n"
# # # # #             "- URLs must be preserved EXACTLY as given\n"
# # # # #             "- Do NOT normalize, fix, or rewrite URLs\n"
# # # # #             "- Embed URLs naturally inside sentences\n"
# # # # #             "- URLs must NOT be grouped or listed\n\n"
# # # # #             f"URLs to include:\n{urls}\n\n"
# # # # #         )

# # # # #         if seed_email:
# # # # #             prompt += (
# # # # #                 "You MUST reuse the following email content verbatim and "
# # # # #                 "only add URLs naturally:\n\n"
# # # # #                 f"{seed_email}\n\n"
# # # # #                 "Return only the final email body."
# # # # #             )
# # # # #         else:
# # # # #             prompt += (
# # # # #                 "Write a new professional email (120–180 words).\n"
# # # # #                 "Return only the email body."
# # # # #             )

# # # # #         return self.send_prompt(prompt)


# # # # # def main():
# # # # #     import argparse
# # # # #     parser = argparse.ArgumentParser()
# # # # #     parser.add_argument("--count", type=int, default=50)
# # # # #     args = parser.parse_args()

# # # # #     model_name = os.getenv("URL_SYNTHESIS_MODEL", "gpt-4.1")
# # # # #     generator = URLEmailGenerator(model_name)

# # # # #     with open("url_dataset.jsonl", "w", encoding="utf-8") as f:
# # # # #         for i in tqdm(range(args.count), desc="Generating emails"):
# # # # #             use_reference = (i == 0)

# # # # #             record = {
# # # # #                 "id": i + 1,
# # # # #                 "sender": REFERENCE_EMAIL["sender"] if use_reference else f"user{i}@example.com",
# # # # #                 "subject": REFERENCE_EMAIL["subject"] if use_reference else "Project Update",
# # # # #                 "content": generator.generate_email(
# # # # #                     seed_email=REFERENCE_EMAIL["content"] if use_reference else None
# # # # #                 )
# # # # #             }

# # # # #             f.write(json.dumps(record, ensure_ascii=False) + "\n")

# # # # #     print("✅ url_dataset.jsonl generated")


# # # # # if __name__ == "__main__":
# # # # #     main()
# # # # import os
# # # # import json
# # # # import random
# # # # from faker import Faker

# # # # faker = Faker()

# # # # # ======================================================
# # # # # CONFIG
# # # # # ======================================================
# # # # NUM_EMAILS = 200

# # # # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # # # OUTPUT_FILE = os.path.join(BASE_DIR, "url_dataset.jsonl")

# # # # # ======================================================
# # # # # URL POOLS (≥5 EACH)
# # # # # ======================================================
# # # # URL_POOLS = {
# # # #     "plain": [
# # # #         "01453.com/",
# # # #         "032255.com/",
# # # #         "05minute.com/",
# # # #         "10paisa.com/",
# # # #         "1uptest.info/",
# # # #         "1928.info/",
# # # #     ],
# # # #     "blog": [
# # # #         "07090.blogspot.com/2011/07/westfield-police-officers-vote-no.html",
# # # #         "1001afilmodyssey.blogspot.com/2010/04/wizard-of-oz-1939.html",
# # # #         "11d.typepad.com/blog/2006/03/rich_parent_poo.html",
# # # #         "1980toppsbaseball.blogspot.com/2010/06/312-mike-barlow.html",
# # # #         "1morefilmblog.com/wordpress/johnny-guitar-ray-1954/",
# # # #     ],
# # # #     "query": [
# # # #         "02ec0a3.netsolhost.com/getperson.php?personID=I4920&tree=ncshawfamily",
# # # #         "0lo5ckgm.gozisanatuza.ru/?n=89425&tid=47936",
# # # #         "10012.kaluxo.remax-quebec.com/?A9FF0BCB-9683-41D6-955A-F1D9106257E4&lang=EN",
# # # #         "17hmr.net/index.php?topic=6680.0",
# # # #         "1greengeneration.elementsintime.com/?p=284",
# # # #     ],
# # # #     "ip": [
# # # #         "124.105.24.19/",
# # # #         "141.2.66.26/en/",
# # # #         "173.193.93.251/our_people/margaret-a-swimmer",
# # # #         "192.156.19.109/",
# # # #         "199.115.25.156/aqueduct/Stakes/HollieHughes.shtml",
# # # #     ],
# # # #     "encoded": [
# # # #         "123movies.info/movie/%c3%83%c5%93%c3%83%c2%a7_yaman_bakire_(1975)_1581424",
# # # #         "100hot.com/hot100/ws/results/Web/92!FE5%20Montreal/1/302363/RightNav",
# # # #         "1957-chevrolet-alternator-conversion.com/wiring.html",
# # # #         "1337x.org/torrent/239713/Viola-bacia-tutti-Asia-Argento-1998-Ita-sub-Eng-Rus-Thai/",
# # # #         "example.com/path%20with%20spaces",
# # # #     ],
# # # #     "html": [
# # # #         '<a href="https://example.com">Click here</a>',
# # # #         '<a href="https://docs.example.com/api">API Docs</a>',
# # # #         '<a href="https://example.com/path#anchor">Read more</a>',
# # # #         '<a href="https://example.com/login?next=/dashboard">Login</a>',
# # # #         '<a href="http://1-private-detective.tripod.com/oldlook.up.html">Profile</a>',
# # # #     ],
# # # #     "markdown": [
# # # #         "[Docs](https://docs.example.com)",
# # # #         "[Pricing](https://example.com/pricing?plan=pro)",
# # # #         "[Support](https://support.example.com/tickets/new)",
# # # #         "[Dashboard](https://app.example.com/#/home)",
# # # #         "[Reset](https://example.com/reset?token=abc123)",
# # # #     ],
# # # #     "image": [
# # # #         '<img src="https://cdn.example.com/img.png" />',
# # # #         '<img src="https://images.example.com/banners/sale.jpg">',
# # # #         '<img src="https://cdn.example.com/assets/icons/icon@2x.png" />',
# # # #         '<img src="https://example.com/images/logo.svg" />',
# # # #         '<img src="https://media.example.com/2025/01/header.webp">',
# # # #     ],
# # # #     "short": [
# # # #         "https://bit.ly/3XkP9Qa",
# # # #         "http://t.co/AbC123",
# # # #         "https://tinyurl.com/yc4z9abc",
# # # #         "https://mail.google.com/url?q=https://example.com",
# # # #         "https://mail.google.com/url?q=https://example.com/pricing&sa=D",
# # # #     ],
# # # #     "edge": [
# # # #         "https://example.com/path(1)/details",
# # # #         "https://example.com/?redirect=https://evil.com",
# # # #         "https://example.com/?q=<script>alert(1)</script>",
# # # #         "https://example.com/?a=1&b=2&c=3&d=4&e=5&f=6",
# # # #         "https://example.com/very/very/very/very/very/long/path/name/index.html",
# # # #     ],
# # # # }

# # # # URL_CATEGORIES = list(URL_POOLS.keys())

# # # # # ======================================================
# # # # # SENDERS
# # # # # ======================================================
# # # # DOMAINS = [
# # # #     "blueridgebiotech.com",
# # # #     "finflow.io",
# # # #     "cloudops.net",
# # # #     "startuphub.ai",
# # # #     "vendor-services.com",
# # # #     "mail-secure.org",
# # # # ]

# # # # ROLES = ["support", "billing", "security", "alerts", "noreply", "admin"]

# # # # def generate_sender():
# # # #     domain = random.choice(DOMAINS)
# # # #     if random.random() < 0.35:
# # # #         return f"{random.choice(ROLES)}@{domain}"

# # # #     first = faker.first_name().lower()
# # # #     last = faker.last_name().lower()
# # # #     return random.choice([
# # # #         f"{first}@{domain}",
# # # #         f"{first}.{last}@{domain}",
# # # #         f"{first[0]}{last}@{domain}",
# # # #         f"{last}.{first}@{domain}",
# # # #         f"{first}{random.randint(1,99)}@{domain}",
# # # #     ])

# # # # # ======================================================
# # # # # SUBJECTS
# # # # # ======================================================
# # # # SUBJECTS = [
# # # #     "Lab test results and next steps",
# # # #     "Security alert detected",
# # # #     "Invoice available for review",
# # # #     "System maintenance notice",
# # # #     "Marketing campaign performance",
# # # #     "Legal compliance update",
# # # #     "Deployment status report",
# # # #     "Your subscription renewal",
# # # #     "Meeting follow-up notes",
# # # #     "Account access update",
# # # # ]

# # # # # ======================================================
# # # # # EMAIL BODY (GOLDEN)
# # # # # ======================================================
# # # # def generate_email_body():
# # # #     blocks = []

# # # #     # 30% reply chain
# # # #     if random.random() < 0.3:
# # # #         blocks.append(
# # # #             f"On Mon, {faker.name()} wrote:\n> {random.choice(random.choice(list(URL_POOLS.values())))}\n"
# # # #         )

# # # #     paragraphs = [
# # # #         faker.paragraph(nb_sentences=random.randint(2,5))
# # # #         for _ in range(random.randint(2,4))
# # # #     ]

# # # #     # URL injection (1–3 URLs)
# # # #     url_count = random.randint(1,3)
# # # #     chosen_categories = random.choices(URL_CATEGORIES, k=url_count)

# # # #     urls = [random.choice(URL_POOLS[c]) for c in chosen_categories]

# # # #     for url in urls:
# # # #         placement = random.choice(["start", "middle", "end", "paren", "line"])
# # # #         if placement == "start":
# # # #             paragraphs[0] = f"{url}\n\n{paragraphs[0]}"
# # # #         elif placement == "middle":
# # # #             idx = random.randint(0, len(paragraphs)-1)
# # # #             paragraphs[idx] += f" ({url})."
# # # #         elif placement == "end":
# # # #             paragraphs.append(url)
# # # #         elif placement == "paren":
# # # #             paragraphs.append(f"({url})")
# # # #         else:
# # # #             paragraphs.append(f"\n{url}\n")

# # # #     blocks.extend(paragraphs)

# # # #     # Signature sometimes contains URL
# # # #     if random.random() < 0.4:
# # # #         sig_url = random.choice(random.choice(list(URL_POOLS.values())))
# # # #     else:
# # # #         sig_url = ""

# # # #     signature = f"""
# # # # --
# # # # {faker.name()}
# # # # {faker.job()}
# # # # {faker.company()}
# # # # {sig_url}
# # # # """
# # # #     blocks.append(signature)

# # # #     return "\n\n".join(blocks)

# # # # # ======================================================
# # # # # MAIN
# # # # # ======================================================
# # # # def main():
# # # #     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
# # # #         for i in range(1, NUM_EMAILS + 1):
# # # #             record = {
# # # #                 "id": i,
# # # #                 "sender": generate_sender(),
# # # #                 "subject": random.choice(SUBJECTS),
# # # #                 "content": generate_email_body(),
# # # #             }
# # # #             f.write(json.dumps(record, ensure_ascii=False) + "\n")

# # # #     print(f"✅ Generated {NUM_EMAILS} GOLDEN emails → {OUTPUT_FILE}")

# # # # if __name__ == "__main__":
# # # #     main()
# # # import os
# # # import json
# # # import random
# # # from faker import Faker
# # # from dotenv import load_dotenv
# # # from openai import OpenAI
# # # from tqdm import tqdm

# # # # ======================================================
# # # # SETUP
# # # # ======================================================
# # # load_dotenv()
# # # faker = Faker()

# # # client = OpenAI(
# # #     api_key=os.getenv("OPENAI_API_KEY"),
# # #     base_url=os.getenv("OPENAI_API_BASE")
# # # )

# # # MODEL_NAME = os.getenv("URL_SYNTHESIS_MODEL", "gpt-4o")
# # # NUM_EMAILS = 50
# # # OUTPUT_FILE = "url_dataset_ai_randomized.jsonl"

# # # # ======================================================
# # # # URL POOLS
# # # # ======================================================
# # # URL_POOLS = {
# # #     "plain": ["01453.com/", "032255.com/", "10paisa.com/", "1uptest.info/", "1928.info/"],
# # #     "blog": [
# # #         "07090.blogspot.com/2011/07/westfield-police-officers-vote-no.html",
# # #         "11d.typepad.com/blog/2006/03/rich_parent_poo.html",
# # #         "1980toppsbaseball.blogspot.com/2010/06/312-mike-barlow.html",
# # #     ],
# # #     "query": [
# # #         "02ec0a3.netsolhost.com/getperson.php?personID=I4920&tree=ncshawfamily",
# # #         "10012.kaluxo.remax-quebec.com/?A9FF0BCB-9683-41D6-955A-F1D9106257E4&lang=EN",
# # #         "17hmr.net/index.php?topic=6680.0",
# # #     ],
# # #     "ip": ["124.105.24.19/", "141.2.66.26/en/", "192.156.19.109/"],
# # #     "encoded": [
# # #         "123movies.info/movie/%c3%83%c5%93%c3%83%c2%a7_yaman_bakire_(1975)_1581424",
# # #         "100hot.com/hot100/ws/results/Web/92!FE5%20Montreal/1/302363/RightNav",
# # #         "example.com/path%20with%20spaces",
# # #     ],
# # #     "html": [
# # #         '<a href="https://example.com">Click here</a>',
# # #         '<a href="https://docs.example.com/api">API Docs</a>',
# # #         '<a href="https://example.com/login?next=/dashboard">Login</a>',
# # #     ],
# # #     "markdown": [
# # #         "[Docs](https://docs.example.com)",
# # #         "[Support](https://support.example.com/tickets/new)",
# # #         "[Dashboard](https://app.example.com/#/home)",
# # #     ],
# # #     "image": [
# # #         '<img src="https://cdn.example.com/img.png" />',
# # #         '<img src="https://images.example.com/banners/sale.jpg">',
# # #         '<img src="https://example.com/images/logo.svg" />',
# # #     ],
# # #     "short": [
# # #         "https://bit.ly/3XkP9Qa",
# # #         "http://t.co/AbC123",
# # #         "https://tinyurl.com/yc4z9abc",
# # #     ],
# # #     "edge": [
# # #         "https://example.com/path(1)/details",
# # #         "https://example.com/?q=<script>alert(1)</script>",
# # #         "https://example.com/very/very/very/very/very/long/path/name/index.html",
# # #     ],
# # # }
# # # URL_CATEGORIES = list(URL_POOLS.keys())

# # # # ======================================================
# # # # SUBJECT TOPICS
# # # # ======================================================
# # # TOPICS_POOL = [
# # #     "Suspicious Login Attempt",
# # #     "Order Confirmation",
# # #     "Scheduled System Maintenance",
# # #     "Document Signature Required",
# # #     "Account Verification",
# # #     "Policy Update Notification",
# # #     "Invoice Generated",
# # #     "Appointment Confirmation",
# # #     "Password Reset Request",
# # #     "Secure File Shared"
# # # ]

# # # # ======================================================
# # # # TONES & PERSONAS
# # # # ======================================================
# # # TONES = [
# # #     "formal",
# # #     "neutral",
# # #     "slightly urgent",
# # #     "friendly but professional",
# # #     "strict compliance tone"
# # # ]

# # # PERSONAS = [
# # #     "a security operations team member",
# # #     "a billing and payments executive",
# # #     "an IT administrator handling system tickets",
# # #     "a compliance and risk officer",
# # #     "a customer success representative",
# # #     "an automated notification system",
# # #     "a platform support engineer",
# # #     "a corporate HR operations associate"
# # # ]

# # # # ======================================================
# # # # RANDOM SENDERS
# # # # ======================================================
# # # GENERIC_DOMAINS = [
# # #     "blueridgebiotech.com", "finflow.io", "cloudops.net",
# # #     "startuphub.ai", "vendor-services.com", "mail-secure.org",
# # #     "global-logistics.net", "fast-track.io", "admin-notify.com"
# # # ]

# # # def generate_random_sender():
# # #     domain = random.choice(GENERIC_DOMAINS)
# # #     if random.random() < 0.35:
# # #         role = random.choice(["support", "billing", "security", "alerts", "noreply", "admin"])
# # #         return f"{role}@{domain}"

# # #     first = faker.first_name().lower()
# # #     last = faker.last_name().lower()
# # #     return random.choice([
# # #         f"{first}@{domain}",
# # #         f"{first}.{last}@{domain}",
# # #         f"{first[0]}{last}@{domain}",
# # #     ])

# # # # ======================================================
# # # # AI EMAIL GENERATION
# # # # ======================================================
# # # def generate_email_with_ai(subject, tone, persona, selected_urls):
# # #     prompt = (
# # #         f"You are {persona}.\n"
# # #         f"Write a {tone} professional email regarding the subject: '{subject}'.\n\n"
# # #         "STRICT RULES:\n"
# # #         "- You must include the specific URLs provided below.\n"
# # #         "- URLs must be preserved EXACTLY as given.\n"
# # #         "- Embed URLs naturally inside sentences.\n"
# # #         "- Do NOT list URLs separately.\n"
# # #         "- Keep under 150 words.\n"
# # #         "- Return ONLY the email body.\n\n"
# # #         f"URLs:\n{selected_urls}\n"
# # #     )

# # #     response = client.chat.completions.create(
# # #         model=MODEL_NAME,
# # #         messages=[{"role": "user", "content": prompt}],
# # #         temperature=0.75
# # #     )

# # #     return response.choices[0].message.content.strip()

# # # # ======================================================
# # # # MAIN
# # # # ======================================================
# # # def main():
# # #     print(f"🚀 Generating {NUM_EMAILS} AI emails with tone + persona diversity...")

# # #     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
# # #         for i in tqdm(range(1, NUM_EMAILS + 1), desc="Processing"):

# # #             subject = random.choice(TOPICS_POOL)
# # #             sender = generate_random_sender()

# # #             tone = random.choice(TONES)
# # #             persona = random.choice(PERSONAS)

# # #             url_count = random.randint(1, 3)
# # #             chosen_categories = random.choices(URL_CATEGORIES, k=url_count)
# # #             selected_urls = [random.choice(URL_POOLS[c]) for c in chosen_categories]

# # #             content = generate_email_with_ai(
# # #                 subject=subject,
# # #                 tone=tone,
# # #                 persona=persona,
# # #                 selected_urls=selected_urls
# # #             )

# # #             record = {
# # #                 "id": i,
# # #                 "sender": sender,
# # #                 "subject": subject,
# # #                 "content": content,
# # #                 "tone": tone,
# # #                 "persona": persona,
# # #                 "url_categories": chosen_categories,
# # #                 "urls": selected_urls
# # #             }

# # #             f.write(json.dumps(record, ensure_ascii=False) + "\n")

# # #     print(f"✅ Dataset generated → {OUTPUT_FILE}")

# # # if __name__ == "__main__":
# # #     main()
# # import os
# # import json
# # import random
# # from faker import Faker
# # from dotenv import load_dotenv
# # from openai import OpenAI
# # from tqdm import tqdm

# # # ======================================================
# # # SETUP
# # # ======================================================
# # load_dotenv()
# # faker = Faker()

# # client = OpenAI(
# #     api_key=os.getenv("OPENAI_API_KEY"),
# #     base_url=os.getenv("OPENAI_API_BASE")
# # )

# # MODEL_NAME = os.getenv("URL_SYNTHESIS_MODEL", "gpt-4o")
# # NUM_EMAILS = 50
# # OUTPUT_FILE = "url_dataset_ai_randomized.jsonl"

# # # ======================================================
# # # URL POOLS
# # # ======================================================
# # URL_POOLS = {
# #     "plain": ["01453.com/", "032255.com/", "10paisa.com/", "1uptest.info/", "1928.info/"],
# #     "blog": [
# #         "07090.blogspot.com/2011/07/westfield-police-officers-vote-no.html",
# #         "11d.typepad.com/blog/2006/03/rich_parent_poo.html",
# #         "1980toppsbaseball.blogspot.com/2010/06/312-mike-barlow.html",
# #     ],
# #     "query": [
# #         "02ec0a3.netsolhost.com/getperson.php?personID=I4920&tree=ncshawfamily",
# #         "10012.kaluxo.remax-quebec.com/?A9FF0BCB-9683-41D6-955A-F1D9106257E4&lang=EN",
# #         "17hmr.net/index.php?topic=6680.0",
# #     ],
# #     "ip": ["124.105.24.19/", "141.2.66.26/en/", "192.156.19.109/"],
# #     "encoded": [
# #         "123movies.info/movie/%c3%83%c5%93%c3%83%c2%a7_yaman_bakire_(1975)_1581424",
# #         "100hot.com/hot100/ws/results/Web/92!FE5%20Montreal/1/302363/RightNav",
# #         "example.com/path%20with%20spaces",
# #     ],
# #     "html": [
# #         '<a href="https://example.com">Click here</a>',
# #         '<a href="https://docs.example.com/api">API Docs</a>',
# #         '<a href="https://example.com/login?next=/dashboard">Login</a>',
# #     ],
# #     "markdown": [
# #         "[Docs](https://docs.example.com)",
# #         "[Support](https://support.example.com/tickets/new)",
# #         "[Dashboard](https://app.example.com/#/home)",
# #     ],
# #     "image": [
# #         '<img src="https://cdn.example.com/img.png" />',
# #         '<img src="https://images.example.com/banners/sale.jpg">',
# #         '<img src="https://example.com/images/logo.svg" />',
# #     ],
# #     "short": [
# #         "https://bit.ly/3XkP9Qa",
# #         "http://t.co/AbC123",
# #         "https://tinyurl.com/yc4z9abc",
# #     ],
# #     "edge": [
# #         "https://example.com/path(1)/details",
# #         "https://example.com/?q=<script>alert(1)</script>",
# #         "https://example.com/very/very/very/very/very/long/path/name/index.html",
# #     ],
# # }
# # URL_CATEGORIES = list(URL_POOLS.keys())

# # # ======================================================
# # # SUBJECT TOPICS
# # # ======================================================
# # TOPICS_POOL = [
# #     "Suspicious Login Attempt",
# #     "Order Confirmation",
# #     "Scheduled System Maintenance",
# #     "Document Signature Required",
# #     "Account Verification",
# #     "Policy Update Notification",
# #     "Invoice Generated",
# #     "Appointment Confirmation",
# #     "Password Reset Request",
# #     "Secure File Shared"
# # ]

# # # ======================================================
# # # TONES & PERSONAS
# # # ======================================================
# # TONES = [
# #     "formal",
# #     "neutral",
# #     "slightly urgent",
# #     "friendly but professional",
# #     "strict compliance tone"
# # ]

# # PERSONAS = [
# #     "a security operations team member",
# #     "a billing and payments executive",
# #     "an IT administrator handling system tickets",
# #     "a compliance and risk officer",
# #     "a customer success representative",
# #     "an automated notification system",
# #     "a platform support engineer",
# #     "a corporate HR operations associate"
# # ]

# # # ======================================================
# # # RANDOM SENDERS
# # # ======================================================
# # GENERIC_DOMAINS = [
# #     "blueridgebiotech.com", "finflow.io", "cloudops.net",
# #     "startuphub.ai", "vendor-services.com", "mail-secure.org",
# #     "global-logistics.net", "fast-track.io", "admin-notify.com"
# # ]

# # def generate_random_sender():
# #     domain = random.choice(GENERIC_DOMAINS)
# #     if random.random() < 0.35:
# #         role = random.choice(["support", "billing", "security", "alerts", "noreply", "admin"])
# #         return f"{role}@{domain}"

# #     first = faker.first_name().lower()
# #     last = faker.last_name().lower()
# #     return random.choice([
# #         f"{first}@{domain}",
# #         f"{first}.{last}@{domain}",
# #         f"{first[0]}{last}@{domain}",
# #     ])

# # # ======================================================
# # # AI EMAIL GENERATION (FIXED PROMPT)
# # # ======================================================
# # def generate_email_with_ai(subject, tone, persona, selected_urls):
# #     prompt = f"""
# # You are {persona} writing a real, believable business email.

# # Subject: "{subject}"
# # Tone: {tone}

# # CRITICAL REQUIREMENTS:
# # - The email MUST make logical and real-world sense.
# # - The URLs provided MUST be contextually relevant to the subject.
# # - If a URL looks unusual (IP, encoded, blog, short link, etc.), explain it naturally
# #   (e.g., legacy system, third-party provider, archived record, tracking link).
# # - URLs must be preserved EXACTLY as given (no rewriting).
# # - Embed URLs naturally inside sentences (no bullet lists).
# # - Do NOT include random or unrelated explanations.
# # - Keep the email under 150 words.
# # - Return ONLY the email body (no subject line, no signature).

# # URLs to embed:
# # {selected_urls}
# # """

# #     response = client.chat.completions.create(
# #         model=MODEL_NAME,
# #         messages=[{"role": "user", "content": prompt}],
# #         temperature=0.7
# #     )

# #     return response.choices[0].message.content.strip()

# # # ======================================================
# # # MAIN
# # # ======================================================
# # def main():
# #     print(f"🚀 Generating {NUM_EMAILS} high-quality, sense-making AI emails...")

# #     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
# #         for i in tqdm(range(1, NUM_EMAILS + 1), desc="Processing"):
# #             subject = random.choice(TOPICS_POOL)
# #             sender = generate_random_sender()
# #             tone = random.choice(TONES)
# #             persona = random.choice(PERSONAS)

# #             url_count = random.randint(1, 3)
# #             chosen_categories = random.choices(URL_CATEGORIES, k=url_count)
# #             selected_urls = [random.choice(URL_POOLS[c]) for c in chosen_categories]

# #             content = generate_email_with_ai(
# #                 subject=subject,
# #                 tone=tone,
# #                 persona=persona,
# #                 selected_urls=selected_urls
# #             )

# #             record = {
# #                 "id": i,
# #                 "sender": sender,
# #                 "subject": subject,
# #                 "content": content
# #             }

# #             f.write(json.dumps(record, ensure_ascii=False) + "\n")

# #     print(f"✅ Dataset generated successfully → {OUTPUT_FILE}")

# # if __name__ == "__main__":
# #     main()
# import os
# import json
# import random
# from faker import Faker
# from dotenv import load_dotenv
# from openai import OpenAI
# from tqdm import tqdm

# # ======================================================
# # SETUP
# # ======================================================
# load_dotenv()
# faker = Faker()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url=os.getenv("OPENAI_API_BASE")
# )

# MODEL_NAME = os.getenv("URL_SYNTHESIS_MODEL", "gpt-4o")
# NUM_EMAILS = 50
# OUTPUT_FILE = "url_dataset_ai_randomized.jsonl"

# # ======================================================
# # URL POOLS
# # ======================================================
# URL_POOLS = {
#     "plain": ["01453.com/", "032255.com/", "10paisa.com/", "1uptest.info/", "1928.info/"],
#     "blog": [
#         "07090.blogspot.com/2011/07/westfield-police-officers-vote-no.html",
#         "11d.typepad.com/blog/2006/03/rich_parent_poo.html",
#         "1980toppsbaseball.blogspot.com/2010/06/312-mike-barlow.html",
#     ],
#     "query": [
#         "02ec0a3.netsolhost.com/getperson.php?personID=I4920&tree=ncshawfamily",
#         "10012.kaluxo.remax-quebec.com/?A9FF0BCB-9683-41D6-955A-F1D9106257E4&lang=EN",
#         "17hmr.net/index.php?topic=6680.0",
#     ],
#     "ip": ["124.105.24.19/", "141.2.66.26/en/", "192.156.19.109/"],
#     "encoded": [
#         "123movies.info/movie/%c3%83%c5%93%c3%83%c2%a7_yaman_bakire_(1975)_1581424",
#         "100hot.com/hot100/ws/results/Web/92!FE5%20Montreal/1/302363/RightNav",
#         "example.com/path%20with%20spaces",
#     ],
#     "html": [
#         '<a href="https://example.com">Click here</a>',
#         '<a href="https://docs.example.com/api">API Docs</a>',
#         '<a href="https://example.com/login?next=/dashboard">Login</a>',
#     ],
#     "markdown": [
#         "[Docs](https://docs.example.com)",
#         "[Support](https://support.example.com/tickets/new)",
#         "[Dashboard](https://app.example.com/#/home)",
#     ],
#     "image": [
#         '<img src="https://cdn.example.com/img.png" />',
#         '<img src="https://images.example.com/banners/sale.jpg">',
#         '<img src="https://example.com/images/logo.svg" />',
#     ],
#     "short": [
#         "https://bit.ly/3XkP9Qa",
#         "http://t.co/AbC123",
#         "https://tinyurl.com/yc4z9abc",
#     ],
#     "edge": [
#         "https://example.com/path(1)/details",
#         "https://example.com/?q=<script>alert(1)</script>",
#         "https://example.com/very/very/very/very/very/long/path/name/index.html",
#     ],
# }
# URL_CATEGORIES = list(URL_POOLS.keys())

# # ======================================================
# # SUBJECT TOPICS
# # ======================================================
# TOPICS_POOL = [
#     "Suspicious Login Attempt",
#     "Order Confirmation",
#     "Scheduled System Maintenance",
#     "Document Signature Required",
#     "Account Verification",
#     "Policy Update Notification",
#     "Invoice Generated",
#     "Appointment Confirmation",
#     "Password Reset Request",
#     "Secure File Shared"
# ]

# # ======================================================
# # TONES & PERSONAS
# # ======================================================
# TONES = [
#     "formal",
#     "neutral",
#     "slightly urgent",
#     "friendly but professional",
#     "strict compliance tone"
# ]

# PERSONAS = [
#     "a security operations team member",
#     "a billing and payments executive",
#     "an IT administrator handling system tickets",
#     "a compliance and risk officer",
#     "a customer success representative",
#     "an automated notification system",
#     "a platform support engineer",
#     "a corporate HR operations associate"
# ]

# # ======================================================
# # RANDOM SENDERS
# # ======================================================
# GENERIC_DOMAINS = [
#     "blueridgebiotech.com", "finflow.io", "cloudops.net",
#     "startuphub.ai", "vendor-services.com", "mail-secure.org",
#     "global-logistics.net", "fast-track.io", "admin-notify.com"
# ]

# def generate_random_sender():
#     domain = random.choice(GENERIC_DOMAINS)
#     if random.random() < 0.35:
#         role = random.choice(["support", "billing", "security", "alerts", "noreply", "admin"])
#         return f"{role}@{domain}"

#     first = faker.first_name().lower()
#     last = faker.last_name().lower()
#     return random.choice([
#         f"{first}@{domain}",
#         f"{first}.{last}@{domain}",
#         f"{first[0]}{last}@{domain}",
#     ])

# # ======================================================
# # AI EMAIL GENERATION (SAFE + RETRY)
# # ======================================================
# def generate_email_with_ai(subject, tone, persona, selected_urls):
#     prompt = f"""
# You are {persona} writing a real, believable business email.

# Subject: "{subject}"
# Tone: {tone}

# CRITICAL REQUIREMENTS:
# - The email MUST make logical and real-world sense.
# - The URLs provided MUST be contextually relevant to the subject.
# - If a URL looks unusual (IP, encoded, blog, short link, etc.), explain it naturally.
# - URLs must be preserved EXACTLY as given.
# - Embed URLs naturally inside sentences.
# - Keep the email under 150 words.
# - Return ONLY the email body.

# URLs to embed:
# {selected_urls}
# """

#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.7
#     )

#     msg = response.choices[0].message.content
#     return msg.strip() if msg else ""

# # ======================================================
# # MAIN (GUARANTEED 50 EMAILS)
# # ======================================================
# def main():
#     print(f"🚀 Generating {NUM_EMAILS} high-quality, sense-making AI emails...")

#     generated = 0

#     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#         with tqdm(total=NUM_EMAILS, desc="Processing") as pbar:
#             while generated < NUM_EMAILS:

#                 subject = random.choice(TOPICS_POOL)
#                 sender = generate_random_sender()
#                 tone = random.choice(TONES)
#                 persona = random.choice(PERSONAS)

#                 url_count = random.randint(1, 3)
#                 chosen_categories = random.choices(URL_CATEGORIES, k=url_count)
#                 selected_urls = [random.choice(URL_POOLS[c]) for c in chosen_categories]

#                 content = generate_email_with_ai(
#                     subject=subject,
#                     tone=tone,
#                     persona=persona,
#                     selected_urls=selected_urls
#                 )

#                 if not content:
#                     continue  # retry without counting

#                 record = {
#                     "id": generated + 1,
#                     "sender": sender,
#                     "subject": subject,
#                     "content": content
#                 }

#                 f.write(json.dumps(record, ensure_ascii=False) + "\n")

#                 generated += 1
#                 pbar.update(1)

#     print(f"✅ Dataset generated successfully → {OUTPUT_FILE}")

# if __name__ == "__main__":
#     main()
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
    
    # 1. WRITTEN EMAILS (The Output of Writers)
    "written_mini": os.path.join(BASE_DIR, "emails_written_by_mini.jsonl"),
    "written_41":   os.path.join(BASE_DIR, "emails_written_by_41.jsonl"),
    
    # 2. INDIVIDUAL EVALUATION RESULTS (The Scores for each pair)
    # These are the 4 files you asked for
    "eval_w_mini_j_mini": os.path.join(BASE_DIR, "results_writer_mini_judge_mini.jsonl"),
    "eval_w_mini_j_41":   os.path.join(BASE_DIR, "results_writer_mini_judge_41.jsonl"),
    "eval_w_41_j_mini":   os.path.join(BASE_DIR, "results_writer_41_judge_mini.jsonl"),
    "eval_w_41_j_41":     os.path.join(BASE_DIR, "results_writer_41_judge_41.jsonl"),

    # 3. MASTER CSV (For Analysis)
    "final_csv": os.path.join(BASE_DIR, "full_matrix_metrics.csv"),
}

# Ensure prompts exist
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
def generate_dataset(writer_model, output_file):
    print(f"\n✍️  [GENERATION] Checking output file for Writer: {writer_model}...")
    
    if os.path.exists(output_file):
        print(f"   ✅ File '{os.path.basename(output_file)}' already exists. Skipping.")
        return

    print(f"   🚀 Starting generation for {writer_model}...")
    
    if not os.path.exists(FILES["raw_dataset"]):
        print("❌ Error: Raw dataset missing.")
        exit()

    client = get_client()
    SYSTEM_PROMPT = "You are an AI assistant. Rewrite the email to be professional. IMPORTANT: Preserve all URLs exactly."

    with open(FILES["raw_dataset"], "r", encoding="utf-8") as f_in, \
         open(output_file, "w", encoding="utf-8") as f_out:
        
        lines = f_in.readlines()
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
            
            except Exception as e:
                print(f"   ⚠️ Write error for {writer_model}: {e}")
    
    print(f"   ✅ Finished writing. Saved to {os.path.basename(output_file)}")

# ======================================================
# STAGE 2: EVALUATION (The Judges)
# ======================================================
class URLLLMEvaluator:
    def __init__(self, model):
        self.client = get_client()
        self.model = model

    def evaluate(self, original, edited):
        if "evaluate" not in PROMPTS: return None
        system = PROMPTS["evaluate"]["system"]
        user = PROMPTS["evaluate"]["user"].format(original=original, edited=edited)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0
            )
            content = response.choices[0].message.content
            # Clean potential markdown
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "")
            return json.loads(content)
        except Exception:
            return None

def run_evaluation_task(input_file, output_file, writer_name, judge_name):
    """
    Runs a single evaluation pair and saves to a specific JSONL file.
    Returns a list of records to add to the master CSV.
    """
    print(f"\n⚖️  [JUDGING] Writer: {writer_name} | Judge: {judge_name}")
    print(f"    Input: {os.path.basename(input_file)}")
    print(f"    Output: {os.path.basename(output_file)}")

    # If result file already exists, we load it instead of re-running (save money/time)
    if os.path.exists(output_file):
        print("    ✅ Result file already exists. Loading data...")
        csv_rows = []
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                # Flatten for CSV
                csv_rows.append({
                    "id": data["id"],
                    "writer_model": writer_name,
                    "judge_model": judge_name,
                    "pair_label": f"Writer:{writer_name}\nJudge:{judge_name}",
                    "url_score": data["scores"]["url_score"],
                    "faithfulness": data["scores"]["faithfulness"],
                    "original_email": data["original_email"],
                    "edited_email": data["edited_email"]
                })
        return csv_rows

    evaluator = URLLLMEvaluator(judge_name)
    csv_rows = []
    
    with open(input_file, "r", encoding="utf-8") as f_in, \
         open(output_file, "w", encoding="utf-8") as f_out:
        
        samples = [json.loads(line) for line in f_in]
        
        for sample in tqdm(samples, desc="    Evaluating"):
            eval_result = evaluator.evaluate(sample["original_email"], sample["edited_email"])
            
            if eval_result:
                # 1. Structure for JSONL file (Detailed)
                detailed_record = {
                    "id": sample.get("id"),
                    "writer_model": writer_name,
                    "judge_model": judge_name,
                    "original_email": sample["original_email"],
                    "edited_email": sample["edited_email"],
                    "scores": {
                        "url_score": eval_result.get("url_preservation", {}).get("score", 0),
                        "faithfulness": eval_result.get("faithfulness", {}).get("score", 0),
                        "explanation": eval_result.get("url_preservation", {}).get("explanation", "")
                    }
                }
                f_out.write(json.dumps(detailed_record) + "\n")
                
                # 2. Structure for CSV (Flat)
                csv_rows.append({
                    "id": sample.get("id"),
                    "writer_model": writer_name,
                    "judge_model": judge_name,
                    "pair_label": f"Writer:{writer_name}\nJudge:{judge_name}",
                    "url_score": detailed_record["scores"]["url_score"],
                    "faithfulness": detailed_record["scores"]["faithfulness"],
                    "original_email": sample["original_email"],
                    "edited_email": sample["edited_email"]
                })
    
    return csv_rows

# ======================================================
# MAIN
# ======================================================
def main():
    print("🚀 INITIALIZING 2x2 EVALUATION MATRIX")
    
    # 1. GENERATE (Writers)
    generate_dataset("gpt-4o-mini", FILES["written_mini"])
    generate_dataset("gpt-4.1",     FILES["written_41"]) 

    # 2. EVALUATE (Judges) - Running all 4 combinations
    all_csv_data = []

    # Pair 1: Mini writes, Mini judges
    data_1 = run_evaluation_task(FILES["written_mini"], FILES["eval_w_mini_j_mini"], "gpt-4o-mini", "gpt-4o-mini")
    all_csv_data.extend(data_1)

    # Pair 2: Mini writes, 4.1 judges
    data_2 = run_evaluation_task(FILES["written_mini"], FILES["eval_w_mini_j_41"], "gpt-4o-mini", "gpt-4.1")
    all_csv_data.extend(data_2)

    # Pair 3: 4.1 writes, Mini judges
    data_3 = run_evaluation_task(FILES["written_41"], FILES["eval_w_41_j_mini"], "gpt-4.1", "gpt-4o-mini")
    all_csv_data.extend(data_3)

    # Pair 4: 4.1 writes, 4.1 judges
    data_4 = run_evaluation_task(FILES["written_41"], FILES["eval_w_41_j_41"], "gpt-4.1", "gpt-4.1")
    all_csv_data.extend(data_4)

    # 3. SAVE MASTER CSV
    if all_csv_data:
        print(f"\n💾 Saving Consolidated Master Data to: {FILES['final_csv']}")
        df = pd.DataFrame(all_csv_data)
        df.to_csv(FILES["final_csv"], index=False)
        print("✅ SUCCESS: All 4 evaluation files + Master CSV created.")
        print("👉 NOW RUN: python url_compare.py")
    else:
        print("❌ No data collected.")

if __name__ == "__main__":
    main()