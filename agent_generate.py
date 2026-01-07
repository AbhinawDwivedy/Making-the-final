"""
ReAct-Style Email Editing Agent

A proper agent implementation following the Think → Plan → Act → Observe loop.
Uses LLM-based evaluation for goal checking (no hard-coded metrics).

Model: Uses OPENAI_MODEL2 (gpt-4.1) for all reasoning.
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


class AgentEmailEditor:
    """
    ReAct-style email editing agent.
    
    The agent follows this loop:
    1. THINK: Analyze the email, understand constraints
    2. PLAN: Create a step-by-step strategy
    3. ACT: Execute the plan using tools
    4. OBSERVE: Check if goal is achieved (LLM-based)
    5. LOOP: If not achieved, go back to PLAN with critique
    
    Uses gpt-4.1 (OPENAI_MODEL2) for all reasoning steps.
    """
    
    def __init__(self, max_loops: int = 3):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        # Use the more capable model for agent reasoning
        self.model = os.getenv("OPENAI_MODEL2", "gpt-4.1")
        self.max_loops = max_loops
        self.agent_log = []
    
    def _log(self, phase: str, message: str, details: dict = None):
        """Add entry to agent log."""
        entry = {
            "phase": phase,
            "message": message,
            "details": details or {}
        }
        self.agent_log.append(entry)
        print(f"[{phase}] {message}")
    
    def _call_api(self, messages: list, temperature: float = 0.7) -> str:
        """Make API call to LLM."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    
    def _parse_json(self, text: str) -> dict:
        """Parse JSON from LLM response, handling markdown code blocks."""
        clean = text.strip()
        if clean.startswith("```"):
            clean = re.sub(r'^```\w*\n?', '', clean)
            clean = re.sub(r'\n?```$', '', clean)
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw": text}
    
    # =========================================================================
    # PHASE 1: THINK - Analyze the email
    # =========================================================================
    def _think(self, email_text: str, task: str, tone: str = None) -> dict:
        """
        Analyze the email to understand its structure and constraints.
        
        Returns:
            dict with key_facts, urls, names, current_tone, constraints
        """
        self._log("THINK", "🧠 Analyzing email structure and constraints...")
        
        system_prompt = """You are an email analysis expert.

Analyze the given email and extract structured information.

Your analysis must include:
1. key_facts: List of important facts, dates, numbers, commitments mentioned
2. urls: List of any URLs/links in the email (extract exact URLs)
3. names: List of people mentioned
4. current_tone: The current tone of the email (formal, informal, friendly, etc.)
5. main_purpose: What is the email trying to achieve?
6. constraints: What MUST be preserved when editing this email?

Respond ONLY in valid JSON with this schema:
{
  "key_facts": ["fact1", "fact2"],
  "urls": ["url1", "url2"],
  "names": ["name1", "name2"],
  "current_tone": "informal",
  "main_purpose": "requesting a meeting",
  "constraints": ["must keep the deadline", "must keep the link"]
}"""
        
        user_prompt = f"""TASK: {task.upper()}
{f'TARGET TONE: {tone}' if tone else ''}

EMAIL TO ANALYZE:
{email_text}

Analyze this email and extract the structured information."""
        
        response = self._call_api([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], temperature=0)
        
        analysis = self._parse_json(response)
        self._log("THINK", "✅ Analysis complete", analysis)
        return analysis
    
    # =========================================================================
    # PHASE 2: PLAN - Create editing strategy
    # =========================================================================
    def _plan(self, email_text: str, task: str, analysis: dict, 
              tone: str = None, previous_critique: str = None) -> dict:
        """
        Create a step-by-step plan for editing the email.
        
        Args:
            previous_critique: If this is a retry, what went wrong before
        
        Returns:
            dict with steps (list of action steps)
        """
        self._log("PLAN", "📋 Creating editing strategy...")
        
        system_prompt = """You are an expert email editor creating a plan.

Based on the email analysis, create a specific step-by-step plan for the editing task.

Your plan should:
1. Be specific to this email (not generic advice)
2. Reference the constraints that MUST be preserved
3. List 3-5 concrete steps to achieve the goal
4. If there was a previous attempt that failed, address those issues

Respond ONLY in valid JSON with this schema:
{
  "strategy_summary": "Brief description of the approach",
  "steps": [
    "Step 1: specific action",
    "Step 2: specific action",
    "Step 3: specific action"
  ],
  "must_preserve": ["list of things to not change"]
}"""
        
        critique_section = ""
        if previous_critique:
            critique_section = f"""

PREVIOUS ATTEMPT FAILED. CRITIQUE:
{previous_critique}

You MUST address these issues in your new plan."""
        
        user_prompt = f"""TASK: {task.upper()}
{f'TARGET TONE: {tone}' if tone else ''}

EMAIL:
{email_text}

ANALYSIS:
{json.dumps(analysis, indent=2)}
{critique_section}

Create a specific plan for this editing task."""
        
        response = self._call_api([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], temperature=0.3)
        
        plan = self._parse_json(response)
        self._log("PLAN", "✅ Plan created", plan)
        return plan
    
    # =========================================================================
    # PHASE 3: ACT - Execute the plan
    # =========================================================================
    def _act(self, email_text: str, task: str, analysis: dict, 
             plan: dict, tone: str = None) -> str:
        """
        Execute the editing plan and produce the result.
        
        Returns:
            The edited email text
        """
        self._log("ACT", "⚡ Executing plan...")
        
        # Get base prompts from prompts.yaml
        task_key = task if task != "elaborate" else "lengthen"
        base_system = prompts.get("email_core", {}).get("system", "")
        task_system = prompts.get(task_key, {}).get("system", "")
        
        # Enhanced system prompt with plan context
        system_prompt = f"""{base_system}

{task_system}

EXECUTION INSTRUCTIONS:
You are executing a specific plan. Follow it precisely.

PLAN TO EXECUTE:
{json.dumps(plan, indent=2)}

CONSTRAINTS FROM ANALYSIS:
- Key facts to preserve: {json.dumps(analysis.get('key_facts', []))}
- URLs to preserve EXACTLY: {json.dumps(analysis.get('urls', []))}
- Names to keep: {json.dumps(analysis.get('names', []))}

CRITICAL RULES:
1. Follow each step in the plan
2. Preserve ALL URLs exactly as they appear (character for character)
3. Keep all key facts and commitments
4. Output ONLY the edited email, no explanations"""
        
        user_prompt = f"""ORIGINAL EMAIL:
{email_text}

{f'TARGET TONE: {tone}' if tone else ''}

Execute the plan and output the edited email."""
        
        result = self._call_api([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], temperature=0.5)
        
        self._log("ACT", "✅ Edit complete", {"preview": result[:100] + "..."})
        return result.strip()
    
    # =========================================================================
    # PHASE 4: OBSERVE - Check if goal achieved using evaluate prompt
    # =========================================================================
    def _observe(self, original: str, edited: str, task: str, 
                 analysis: dict, tone: str = None) -> dict:
        """
        Evaluate if the edit achieved the goal using the evaluate prompt from prompts.yaml.
        
        Uses the existing Faithfulness, Completeness, Robustness criteria.
        
        Returns:
            dict with:
            - goal_achieved: bool (True if overall score >= 4)
            - scores: {faithfulness, completeness, robustness, overall}
            - critique: what to fix if not achieved
        """
        self._log("OBSERVE", "👁️ Evaluating result using Faithfulness/Completeness/Robustness...")
        
        # Use the evaluate prompt from prompts.yaml
        system_prompt = prompts.get("evaluate", {}).get("system", "")
        user_prompt = prompts.get("evaluate", {}).get("user", "").format(
            original=original,
            edited=edited
        )
        
        response = self._call_api([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], temperature=0)
        
        scores = self._parse_json(response)
        
        # Extract scores
        faithfulness = scores.get("faithfulness", {}).get("score", 0)
        completeness = scores.get("completeness", {}).get("score", 0)
        robustness = scores.get("robustness", {}).get("score", 0)
        overall = scores.get("overall", {}).get("score", 0)
        
        # Goal is achieved if overall score >= 4.5
        goal_achieved = overall >= 4.5
        
        # Build critique from low-scoring dimensions (this tells PLAN what to fix)
        critique_parts = []
        if faithfulness < 4.5:
            critique_parts.append(f"Faithfulness ({faithfulness}/5): {scores.get('faithfulness', {}).get('reason', 'Unknown')}")
        if completeness < 4.5:
            critique_parts.append(f"Completeness ({completeness}/5): {scores.get('completeness', {}).get('reason', 'Unknown')}")
        if robustness < 4.5:
            critique_parts.append(f"Robustness ({robustness}/5): {scores.get('robustness', {}).get('reason', 'Unknown')}")
        
        # Add overall reason if goal not achieved
        if not goal_achieved:
            critique_parts.append(f"Overall ({overall}/5): {scores.get('overall', {}).get('reason', 'Need ≥4.5')}")
        
        critique = " | ".join(critique_parts) if critique_parts else ""
        
        # Build observation result
        observation = {
            "goal_achieved": goal_achieved,
            "scores": {
                "faithfulness": faithfulness,
                "completeness": completeness,
                "robustness": robustness,
                "overall": overall
            },
            "score_reasons": {
                "faithfulness": scores.get("faithfulness", {}).get("reason", ""),
                "completeness": scores.get("completeness", {}).get("reason", ""),
                "robustness": scores.get("robustness", {}).get("reason", ""),
                "overall": scores.get("overall", {}).get("reason", "")
            },
            "critique": critique,
            "quality_score": overall
        }
        
        # Log the evaluation
        if goal_achieved:
            self._log("OBSERVE", f"✅ Goal achieved! Overall: {overall}/5", observation)
        else:
            self._log("OBSERVE", f"❌ Goal not achieved. Overall: {overall}/5 (need ≥4.5)", observation)
        
        return observation
    
    # =========================================================================
    # MAIN AGENT LOOP
    # =========================================================================
    def generate(self, action: str, email_text: str, tone: str = None, 
                 selected_text: str = None) -> dict:
        """
        Main entry point - runs the full agent loop.
        
        Args:
            action: 'shorten', 'lengthen', or 'tone'
            email_text: The email content (or full email if selected_text provided)
            tone: Target tone (only for 'tone' action)
            selected_text: If provided, only this portion is edited
        
        Returns:
            dict with:
            - result: The edited email text
            - goal_achieved: Whether the agent succeeded
            - loops_used: Number of loops taken
            - agent_log: Full log of agent reasoning
            - final_quality_score: 1-5 quality rating
        """
        # Reset log for new generation
        self.agent_log = []
        
        self._log("START", f"🚀 Starting agent for task: {action}", {
            "action": action,
            "tone": tone,
            "has_selection": bool(selected_text)
        })
        
        # Determine what text to actually edit
        text_to_edit = selected_text if selected_text else email_text
        task = action if action != "elaborate" else "lengthen"
        
        # PHASE 1: THINK (only once at the start)
        analysis = self._think(text_to_edit, task, tone)
        
        # Loop variables
        current_result = None
        previous_critique = None
        goal_achieved = False
        final_observation = None
        
        for loop in range(1, self.max_loops + 1):
            self._log("LOOP", f"🔄 Loop {loop}/{self.max_loops}")
            
            # PHASE 2: PLAN
            plan = self._plan(
                text_to_edit, task, analysis, tone, 
                previous_critique=previous_critique
            )
            
            # PHASE 3: ACT
            current_result = self._act(
                text_to_edit, task, analysis, plan, tone
            )
            
            # PHASE 4: OBSERVE
            observation = self._observe(
                text_to_edit, current_result, task, analysis, tone
            )
            final_observation = observation
            
            # Check if goal achieved
            if observation.get("goal_achieved", False):
                goal_achieved = True
                self._log("SUCCESS", f"✨ Goal achieved in {loop} loop(s)!", {
                    "quality_score": observation.get("quality_score", "N/A")
                })
                break
            else:
                # Prepare critique for next loop
                previous_critique = observation.get("critique", "Unknown issue")
                self._log("RETRY", f"⚠️ Retrying with critique: {previous_critique[:100]}...")
        
        # If we exhausted all loops
        if not goal_achieved:
            self._log("MAX_LOOPS", f"⚠️ Max loops ({self.max_loops}) reached. Returning best effort.")
        
        return {
            "result": current_result,
            "goal_achieved": goal_achieved,
            "loops_used": loop,
            "agent_log": self.agent_log,
            "final_quality_score": final_observation.get("quality_score", 0) if final_observation else 0,
            "final_checks": final_observation.get("checks", []) if final_observation else []
        }


# =============================================================================
# Quick test
# =============================================================================
if __name__ == "__main__":
    agent = AgentEmailEditor(max_loops=3)
    
    test_email = """Hey John,

Hope you're doing well! Just wanted to touch base about the project meeting. 
We're planning to have it on Friday at 3pm. Here's the Zoom link: 
https://zoom.us/j/1234567890?pwd=abc123

The budget is $5000 and we need to finalize everything by end of month.
Let me know if that works for you!

Thanks,
Sarah"""
    
    print("\n" + "="*60)
    print("Testing SHORTEN task")
    print("="*60)
    
    result = agent.generate("shorten", test_email)
    
    print("\n" + "="*60)
    print("FINAL RESULT")
    print("="*60)
    print(f"Goal Achieved: {result['goal_achieved']}")
    print(f"Loops Used: {result['loops_used']}")
    print(f"Quality Score: {result['final_quality_score']}")
    print(f"\nEdited Email:\n{result['result']}")
