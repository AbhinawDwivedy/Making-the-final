from openai import OpenAI
from dotenv import load_dotenv
import os, yaml

load_dotenv()

# Load specific prompts for chat
script_dir = os.path.dirname(os.path.abspath(__file__))
# Check for ext_prompts.yaml in gmail-ai-editor folder relative to this script
prompts_path = os.path.join(script_dir, "gmail-ai-editor", "ext_prompts.yaml")

if not os.path.exists(prompts_path):
    # Fallback to current directory if not found in subdirectory
    prompts_path = "ext_prompts.yaml"

with open(prompts_path, "r", encoding="utf-8") as f:
    prompts = yaml.safe_load(f)

class ChatGenerator:
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

    def chat(self, user_message, email_context="", conversation_history=None):
        """
        Handle chat conversation with context using extended prompts.
        
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
