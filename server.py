from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from generate import GenerateEmail
from chat_generate import ChatGenerator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow CORS for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify chrome-extension://<id>
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize generator for rewrite
model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
if not model:
    print("Warning: OPENAI_MODEL not set, defaulting to gpt-4o-mini")
    model = "gpt-4o-mini"
    
gen = GenerateEmail(model)

# Initialize generator for chat (using OPENAI_MODEL2)
chat_model = os.getenv("OPENAI_MODEL2", "gpt-4.1")
print(f"Chat using model: {chat_model}")
# Use the new ChatGenerator that uses ext_prompts.yaml
chat_gen = ChatGenerator(chat_model)

class RewriteRequest(BaseModel):
    mode: str
    text: str

@app.post("/rewrite")
async def rewrite_email(request: RewriteRequest):
    try:
        mode = request.mode.lower()
        
        # Default values
        action = mode
        tone = None
        
        # Parse "tone:friendly" or "shorten" etc.
        if mode.startswith("tone:"):
            action = "tone"
            tone_parts = mode.split(":")
            if len(tone_parts) > 1:
                tone = tone_parts[1].capitalize() # e.g. "friendly" -> "Friendly"
        elif mode == "professional": # Legacy support
            action = "tone"
            tone = "Professional"
        elif mode == "elaborate":
            action = "lengthen"
            
        # Log to see what's happening
        print(f"Processing: action={action}, tone={tone}")
            
        result = gen.generate(action, request.text, tone)
        return {"status": "ok", "result": result}
        
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# AGENTIC MODE ENDPOINT
# ============================================
from agent import EmailRefinementAgent

class AgenticRequest(BaseModel):
    mode: str
    text: str
    target_score: float = 4.5
    max_attempts: int = 3

@app.post("/rewrite-agentic")
async def rewrite_agentic(request: AgenticRequest):
    """
    Agentic email rewriting with iterative refinement.
    The agent will refine the email until quality target is met.
    """
    try:
        mode = request.mode.lower()
        
        # Parse mode
        action = mode
        tone = None
        
        if mode.startswith("tone:"):
            action = "tone"
            tone_parts = mode.split(":")
            if len(tone_parts) > 1:
                tone = tone_parts[1].capitalize()
        elif mode == "professional":
            action = "tone"
            tone = "Professional"
        elif mode == "elaborate":
            action = "lengthen"
        
        print(f"[AGENTIC] Processing: action={action}, tone={tone}")
        
        # Create agent with user-specified parameters
        agent = EmailRefinementAgent(
            target_score=request.target_score,
            max_attempts=request.max_attempts,
            model=model  # Use same model as regular endpoint
        )
        
        # Run the agentic refinement
        result = agent.achieve_goal(request.text, task=action, tone=tone)
        
        return {
            "status": "ok",
            "result": result["final_output"],
            "agentic_info": {
                "goal_achieved": result["goal_achieved"],
                "attempts_used": result["attempts_used"],
                "final_scores": result["final_scores"],
                "agent_log": result["agent_log"]
            }
        }
        
    except Exception as e:
        print(f"[AGENTIC] Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

class ChatRequest(BaseModel):
    message: str
    email_context: str = ""
    conversation_history: list = []

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        result = chat_gen.chat(
            user_message=request.message,
            email_context=request.email_context,
            conversation_history=request.conversation_history
        )
        return {"status": "ok", "result": result}
    except Exception as e:
        print(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

