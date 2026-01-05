# # from openai import OpenAI
# # from dotenv import load_dotenv
# # import os
# # import yaml

# # load_dotenv()

# # with open("prompts.yaml", "r", encoding="utf-8") as f:
# #     prompts = yaml.safe_load(f)

# # class GenerateEmail:
# #     def __init__(self, model: str):
# #         # initialize client once
# #         self.client = OpenAI(
# #             base_url=os.getenv("OPENAI_API_BASE"),
# #             api_key=os.getenv("OPENAI_API_KEY"),
# #         )
# #         self.deployment_name = model
# #         self.client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_API_BASE"))
# #         self.model=model

# #     def _call_api(self,messages):
# #         r=self.client.chat.completions.create(model=self.model,messages=messages,temperature=0.7)
# #         return r.choices[0].message.content

# #     def get_prompt(self,name,type="user",**k):
# #         return prompts[name][type].format(**k)

# #     def send_prompt(self,user,system):
# #         return self._call_api([{"role":"system","content":system},{"role":"user","content":user}])

# #     def generate(self,action,email_text,tone=None):
# #         args={"selected_text":email_text,"tone":tone}
# #         return self.send_prompt(self.get_prompt(action,"user",**args),self.get_prompt(action,"system",**args))
# from openai import OpenAI
# from dotenv import load_dotenv
# import os, json, yaml

# load_dotenv()

# with open("prompts.yaml","r",encoding="utf-8") as f:
#     prompts=yaml.safe_load(f)

# class GenerateEmail:
#     def __init__(self,model):
#         self.client=OpenAI(
#             api_key=os.getenv("OPENAI_API_KEY"),
#             base_url=os.getenv("OPENAI_API_BASE")
#         )
#         self.model=model

#     def _call_api(self,messages):
#         r=self.client.chat.completions.create(
#             model=self.model,
#             messages=messages,
#             temperature=0.7
#         )
#         return r.choices[0].message.content

#     def generate(self,action,email_text,tone=None):
#         args={"selected_text":email_text,"tone":tone}
#         system=prompts[action]["system"].format(**args)
#         user=prompts[action]["user"].format(**args)
#         return self._call_api([
#             {"role":"system","content":system},
#             {"role":"user","content":user}
#         ])

# class EmailJudge:
#     def __init__(self):
#         self.client=OpenAI(
#             api_key=os.getenv("OPENAI_API_KEY"),
#             base_url=os.getenv("OPENAI_API_BASE")
#         )
#         self.model=os.getenv("OPENAI_EVAL_MODEL")

#     def evaluate(self,original,edited):
#         system=prompts["evaluate"]["system"]
#         user=prompts["evaluate"]["user"].format(
#             original=original,
#             edited=edited
#         )
#         r=self.client.chat.completions.create(
#             model=self.model,
#             messages=[
#                 {"role":"system","content":system},
#                 {"role":"user","content":user}
#             ],
#             temperature=0
#         )
#         return json.loads(r.choices[0].message.content)
from openai import OpenAI
from dotenv import load_dotenv
import os, yaml

load_dotenv()

with open("prompts.yaml", "r", encoding="utf-8") as f:
    prompts = yaml.safe_load(f)

class GenerateEmail:
    def __init__(self, model):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.model = model

    def _call_api(self, messages):
        r = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        return r.choices[0].message.content

    def generate(self, action, email_text, tone=None, selected_text=None):
        """
        Generate edited email content.
        
        Args:
            action: 'lengthen', 'shorten', or 'tone'
            email_text: The full email content
            tone: Target tone (only for 'tone' action)
            selected_text: If provided, only this portion will be edited
                          with email_text used as context
        
        Returns:
            Edited text (either full email or just the selected portion)
        """
        # Determine if we're in selection mode
        is_selection_mode = selected_text is not None and selected_text.strip()
        
        if is_selection_mode:
            # Use selection-specific prompts
            prompt_key = f"{action}_selection"
            args = {
                "selected_text": selected_text,
                "full_email": email_text,
                "tone": tone
            }
        else:
            # Use standard prompts for full email
            prompt_key = action
            args = {
                "selected_text": email_text,
                "tone": tone
            }

        system = prompts[prompt_key]["system"].format(**args)
        user = prompts[prompt_key]["user"].format(**args)

        return self._call_api([
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ])

    def chat(self, user_message, email_context="", conversation_history=None):
        """
        Handle chat conversation with context.
        
        Args:
            user_message: The user's chat message
            email_context: Current email content for context
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            AI response string
        """
        if conversation_history is None:
            conversation_history = []
        
        # Build system prompt with email context
        system = prompts["chat"]["system"].format(
            email_context=email_context if email_context else "(No email content yet - user may be drafting a new email)"
        )
        
        # Build messages list
        messages = [{"role": "system", "content": system}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return self._call_api(messages)

