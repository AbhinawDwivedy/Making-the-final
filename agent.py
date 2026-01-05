"""
Agentic Email Refinement Agent

This module provides an autonomous agent that iteratively refines emails
until quality targets are met through self-evaluation and adaptive strategies.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import yaml
import re

load_dotenv()

# Load prompts
script_dir = os.path.dirname(os.path.abspath(__file__))
prompts_path = os.path.join(script_dir, "prompts.yaml")
with open(prompts_path, "r", encoding="utf-8") as f:
    prompts = yaml.safe_load(f)


class EmailRefinementAgent:
    """
    An autonomous agent that refines emails through iterative self-evaluation.
    
    The agent:
    1. Generates an initial edit based on the task
    2. Evaluates the output quality (Faithfulness, Completeness, Robustness)
    3. If quality < target, diagnoses issues and adapts strategy
    4. Repeats until quality target is met or max attempts reached
    """
    
    def __init__(self, target_score: float = 4.5, max_attempts: int = 3, model: str = None):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.target_score = target_score
        self.max_attempts = max_attempts
        self.agent_log = []
    
    def _call_api(self, messages: list, temperature: float = 0.7) -> str:
        """Make API call to LLM."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    
    def _generate(self, email_text: str, task: str, tone: str = None, 
                  strategy_hint: str = None) -> str:
        """Generate an edited email based on task."""
        # Map task names
        action_map = {
            "lengthen": "lengthen",
            "elaborate": "lengthen",
            "shorten": "shorten",
            "tone": "tone"
        }
        action = action_map.get(task, task)
        
        # Build system prompt with optional strategy hint
        system_prompt = prompts.get("email_core", {}).get("system", "")
        task_system = prompts.get(action, {}).get("system", "")
        
        if strategy_hint:
            task_system += f"\n\nADDITIONAL STRATEGY:\n{strategy_hint}"
        
        full_system = f"{system_prompt}\n\n{task_system}"
        
        # Build user prompt
        user_prompt = prompts.get(action, {}).get("user", "").format(
            selected_text=email_text,
            tone=tone or "Professional"
        )
        
        return self._call_api([
            {"role": "system", "content": full_system},
            {"role": "user", "content": user_prompt}
        ])
    
    def _evaluate(self, original: str, edited: str) -> dict:
        """Evaluate the quality of an edited email."""
        system_prompt = prompts.get("evaluate", {}).get("system", "")
        user_prompt = prompts.get("evaluate", {}).get("user", "").format(
            original=original,
            edited=edited
        )
        
        response = self._call_api([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], temperature=0)
        
        # Parse JSON response
        try:
            # Clean up response if wrapped in markdown
            clean_response = response.strip()
            if clean_response.startswith("```"):
                clean_response = re.sub(r'^```\w*\n?', '', clean_response)
                clean_response = re.sub(r'\n?```$', '', clean_response)
            
            scores = json.loads(clean_response)
            return scores
        except json.JSONDecodeError:
            # Fallback: assume good quality if parsing fails
            return {
                "faithfulness": {"score": 4, "reason": "Parse error - assuming ok"},
                "completeness": {"score": 4, "reason": "Parse error - assuming ok"},
                "robustness": {"score": 4, "reason": "Parse error - assuming ok"},
                "overall": {"score": 4, "reason": "Parse error - assuming ok"}
            }
    
    def _diagnose(self, scores: dict) -> list:
        """Diagnose issues based on low scores."""
        issues = []
        
        if scores.get("faithfulness", {}).get("score", 5) < 4:
            issues.append({
                "type": "faithfulness",
                "severity": "high",
                "fix": "Be more careful to preserve exact facts without adding assumptions"
            })
        
        if scores.get("completeness", {}).get("score", 5) < 4:
            issues.append({
                "type": "completeness", 
                "severity": "high",
                "fix": "Ensure all key information, requests, and deadlines are preserved"
            })
        
        if scores.get("robustness", {}).get("score", 5) < 4:
            issues.append({
                "type": "robustness",
                "severity": "medium",
                "fix": "Improve grammar, clarity, and professional tone"
            })
        
        return issues
    
    def _adapt_strategy(self, issues: list, attempt: int) -> str:
        """Generate strategy hints based on diagnosed issues."""
        hints = []
        
        for issue in issues:
            hints.append(f"- {issue['fix']}")
        
        # Add progressive hints based on attempt number
        if attempt >= 2:
            hints.append("- Be extremely conservative with changes")
            hints.append("- Verify every fact from original is present in output")
        
        return "\n".join(hints) if hints else None
    
    def achieve_goal(self, email_text: str, task: str, tone: str = None) -> dict:
        """
        Main agentic loop: refine email until quality target is met.
        
        Args:
            email_text: Original email content
            task: 'lengthen', 'shorten', or 'tone'
            tone: Target tone (only for 'tone' task)
        
        Returns:
            Dictionary with:
            - goal_achieved: bool
            - attempts_used: int
            - final_output: str
            - final_scores: dict
            - agent_log: list of activities
        """
        self.agent_log = []
        
        # Log start
        self.agent_log.append({
            "type": "start",
            "message": "🚀 Agent starting refinement task",
            "email_length": len(email_text.split()),
            "task": task,
            "tone": tone,
            "target_score": self.target_score
        })
        
        current_output = None
        current_scores = None
        strategy_hint = None
        
        for attempt in range(1, self.max_attempts + 1):
            # Log attempt start
            self.agent_log.append({
                "type": "attempt_start",
                "attempt": attempt,
                "message": f"📝 Attempt {attempt}/{self.max_attempts}",
                "strategy_description": strategy_hint or "Initial generation"
            })
            
            # Generate
            current_output = self._generate(
                email_text, task, tone, strategy_hint
            )
            
            # Evaluate
            current_scores = self._evaluate(email_text, current_output)
            overall_score = current_scores.get("overall", {}).get("score", 0)
            
            # Log evaluation
            self.agent_log.append({
                "type": "evaluation",
                "attempt": attempt,
                "message": f"📊 Evaluated: {overall_score}/5.0",
                "scores": current_scores
            })
            
            # Check if goal achieved
            if overall_score >= self.target_score:
                self.agent_log.append({
                    "type": "success",
                    "message": f"✅ Goal achieved! Score: {overall_score}/5.0",
                    "attempts_used": attempt
                })
                
                return {
                    "goal_achieved": True,
                    "attempts_used": attempt,
                    "final_output": current_output,
                    "final_scores": current_scores,
                    "agent_log": self.agent_log
                }
            
            # Diagnose and adapt
            issues = self._diagnose(current_scores)
            
            self.agent_log.append({
                "type": "diagnosis",
                "attempt": attempt,
                "message": f"🔍 Diagnosing issues...",
                "diagnosis": issues
            })
            
            strategy_hint = self._adapt_strategy(issues, attempt)
        
        # Max attempts reached
        self.agent_log.append({
            "type": "max_attempts",
            "message": f"⚠️ Max attempts ({self.max_attempts}) reached. Returning best effort.",
            "final_score": current_scores.get("overall", {}).get("score", 0)
        })
        
        return {
            "goal_achieved": False,
            "attempts_used": self.max_attempts,
            "final_output": current_output,
            "final_scores": current_scores,
            "agent_log": self.agent_log
        }


# Quick test if run directly
if __name__ == "__main__":
    agent = EmailRefinementAgent(target_score=4.5, max_attempts=3)
    
    test_email = "hey, meeting tmrw at 5pm ok? thx"
    result = agent.achieve_goal(test_email, task="lengthen")
    
    print("\n=== RESULT ===")
    print(f"Goal achieved: {result['goal_achieved']}")
    print(f"Attempts: {result['attempts_used']}")
    print(f"Score: {result['final_scores']['overall']['score']}/5.0")
    print(f"\nOutput:\n{result['final_output']}")
