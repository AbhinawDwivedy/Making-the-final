from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from generate import GenerateEmail
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

# Initialize generator
model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
if not model:
    print("Warning: OPENAI_MODEL not set, defaulting to gpt-4o-mini")
    model = "gpt-4o-mini"
    
gen = GenerateEmail(model)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
