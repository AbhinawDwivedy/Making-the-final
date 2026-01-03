# # from openai import OpenAI
# # import os, json, yaml

# # with open("prompts.yaml","r",encoding="utf-8") as f:
# #     prompts=yaml.safe_load(f)

# # class EmailJudge:
# #     def __init__(self):
# #         self.client=OpenAI(
# #             api_key=os.getenv("OPENAI_API_KEY"),
# #             base_url=os.getenv("OPENAI_API_BASE")
# #         )
# #         self.model=os.getenv("OPENAI_EVAL_MODEL")

# #     def evaluate(self, original, edited, system_prompt, user_prompt):
# #         r=self.client.chat.completions.create(
# #             model=self.model,
# #             messages=[
# #                 {"role":"system","content":system_prompt},
# #                 {"role":"user","content":user_prompt.format(
# #                     original=original,
# #                     edited=edited
# #                 )}
# #             ],
# #             temperature=0
# #         )

# #         return json.loads(r.choices[0].message.content)
# from openai import OpenAI
# import os, json, yaml

# with open("prompts.yaml", "r", encoding="utf-8") as f:
#     prompts = yaml.safe_load(f)

# class EmailJudge:
#     def __init__(self):
#         self.client = OpenAI(
#             api_key=os.getenv("OPENAI_API_KEY"),
#             base_url=os.getenv("OPENAI_API_BASE")
#         )
#         self.model = os.getenv("OPENAI_EVAL_MODEL")

#     def evaluate(self, original, edited):
#         system = prompts["evaluate"]["system"]
#         user = prompts["evaluate"]["user"].format(
#             original=original,
#             edited=edited
#         )

#         r = self.client.chat.completions.create(
#             model=self.model,
#             messages=[
#                 {"role": "system", "content": system},
#                 {"role": "user", "content": user}
#             ],
#             temperature=0
#         )

#         return json.loads(r.choices[0].message.content)

from openai import OpenAI
import os, json, yaml

with open("prompts.yaml", "r", encoding="utf-8") as f:
    prompts = yaml.safe_load(f)

class EmailJudge:
    def __init__(self, model):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.model = model  # <--- UPDATED: Uses the model passed from app.py

    def evaluate(self, original, edited):
        system = prompts["evaluate"]["system"]
        user = prompts["evaluate"]["user"].format(
            original=original,
            edited=edited
        )

        r = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            temperature=0
        )

        return json.loads(r.choices[0].message.content)