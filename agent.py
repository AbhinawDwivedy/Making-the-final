# """
# Agentic Email Refinement Agent

# This module implements an autonomous agent that iteratively refines emails
# to achieve quality goals through self-evaluation and adaptive strategies.
# """

# import json
# import time
# import os
# from dotenv import load_dotenv
# from generate import GenerateEmail
# from judge import EmailJudge

# load_dotenv()


# class EmailRefinementAgent:
#     """
#     Autonomous agent that iteratively refines emails to achieve quality goals.
    
#     The agent:
#     1. Sets explicit goals (e.g., score >= 4.5)
#     2. Makes autonomous decisions about which strategy to use
#     3. Self-evaluates its outputs
#     4. Adapts behavior based on feedback
#     5. Provides transparent reasoning through detailed logs
#     """
    
#     def __init__(self, target_score=4.5, max_attempts=3, model=None):
#         """
#         Initialize the agentic email refinement system.
        
#         Args:
#             target_score (float): Quality score threshold to achieve (0-5)
#             max_attempts (int): Maximum refinement iterations
#             model (str): OpenAI model to use (default: from OPENAI_AGENT1_MODEL env var)
#         """
#         self.target_score = target_score
#         self.max_attempts = max_attempts
        
#         # Use environment variables for model selection
#         self.model = model or os.getenv("OPENAI_AGENT1_MODEL", "gpt-4o-mini")
#         self.judge_model = os.getenv("OPENAI_AGENT2_MODEL", "gpt-4.1")
        
#         self.generator = GenerateEmail(model=self.model)
#         self.judge = EmailJudge(model=self.judge_model)
        
#         # Strategy definitions - agent chooses from these autonomously
#         self.strategies = {
#             'standard': {
#                 'description': 'Standard generation approach',
#                 'modifier': ''
#             },
#             'conservative': {
#                 'description': 'Minimal changes, preserve all facts strictly',
#                 'modifier': '\n\nCRITICAL: Make MINIMAL changes. Preserve every single fact, number, date, and detail exactly as written.'
#             },
#             'preserve_details': {
#                 'description': 'Focus on completeness and information retention',
#                 'modifier': '\n\nCRITICAL: Ensure ALL information from the original is preserved. Do not omit any details, requests, or context.'
#             },
#             'clarity_focus': {
#                 'description': 'Improve structure and clarity',
#                 'modifier': '\n\nCRITICAL: Focus on improving clarity, flow, and structure while preserving all original content.'
#             }
#         }
        
#     def achieve_goal(self, original_email, task, tone=None, selected_text=None):
#         """
#         Main agentic loop - autonomously works toward quality goal.
        
#         This method demonstrates true AI agency:
#         - Autonomous decision-making (chooses strategies)
#         - Goal-directed behavior (works toward target_score)
#         - Self-evaluation (checks own work)
#         - Adaptive learning (changes approach based on results)
        
#         Args:
#             original_email (str): Original email text
#             task (str): Task type ('lengthen', 'shorten', 'tone')
#             tone (str, optional): Target tone if task is 'tone'
#             selected_text (str, optional): Specific text to edit
            
#         Returns:
#             dict: {
#                 'final_output': str,          # Best generated email
#                 'final_scores': dict,         # Quality scores
#                 'attempts_used': int,         # Number of attempts taken
#                 'agent_log': list,            # Detailed activity log
#                 'goal_achieved': bool         # Whether target was reached
#             }
#         """
#         agent_log = []
#         best_output = None
#         best_score = 0
#         best_scores = None
        
#         # Log agent start
#         log_entry = self._log_start(original_email, task, tone)
#         agent_log.append(log_entry)
#         print(f"\n{log_entry['message']}")
        
#         for attempt in range(1, self.max_attempts + 1):
#             print(f"\n{'='*60}")
            
#             # AUTONOMOUS DECISION 1: Choose strategy based on context
#             strategy = self._choose_strategy(attempt, agent_log)
            
#             log_entry = self._log_attempt_start(attempt, strategy)
#             agent_log.append(log_entry)
#             print(f"{log_entry['message']}")
#             print(f"💭 Strategy: {log_entry['strategy_description']}")
            
#             # AUTONOMOUS ACTION 1: Generate with chosen strategy
#             print("⚡ Generating...")
#             generated = self._generate_with_strategy(
#                 original_email, task, tone, selected_text, strategy
#             )
            
#             # AUTONOMOUS ACTION 2: Self-evaluate the output
#             print("📊 Evaluating...")
#             scores = self._evaluate(original_email, generated)
#             current_score = scores['overall']['score']
            
#             log_entry = self._log_evaluation(attempt, scores)
#             agent_log.append(log_entry)
#             print(f"{log_entry['message']}")
            
#             # Track best version
#             if current_score > best_score:
#                 best_score = current_score
#                 best_output = generated
#                 best_scores = scores
            
#             # AUTONOMOUS DECISION 2: Check if goal is achieved
#             if current_score >= self.target_score:
#                 log_entry = self._log_success(attempt, current_score)
#                 agent_log.append(log_entry)
#                 print(f"\n{log_entry['message']}")
                
#                 return {
#                     'final_output': generated,
#                     'final_scores': scores,
#                     'attempts_used': attempt,
#                     'agent_log': agent_log,
#                     'goal_achieved': True
#                 }
#             else:
#                 # AUTONOMOUS ACTION 3: Diagnose what went wrong
#                 diagnosis = self._diagnose_failure(scores)
#                 log_entry = self._log_diagnosis(attempt, diagnosis)
#                 agent_log.append(log_entry)
                
#                 issue_types = ', '.join([d['type'] for d in diagnosis])
#                 print(f"⚠️  Issues detected: {issue_types}")
                
#                 if attempt < self.max_attempts:
#                     print("🔧 Agent adapting strategy for next attempt...")
        
#         # Max attempts reached without achieving goal
#         log_entry = self._log_max_attempts(best_score)
#         agent_log.append(log_entry)
#         print(f"\n{log_entry['message']}")
        
#         return {
#             'final_output': best_output,
#             'final_scores': best_scores,
#             'attempts_used': self.max_attempts,
#             'agent_log': agent_log,
#             'goal_achieved': False
#         }
    
#     def _choose_strategy(self, attempt, agent_log):
#         """
#         Agent autonomously chooses strategy based on previous results.
        
#         This demonstrates autonomous decision-making:
#         - First attempt: Try standard approach
#         - Subsequent attempts: Analyze previous failure and adapt
        
#         Args:
#             attempt (int): Current attempt number
#             agent_log (list): History of previous attempts
            
#         Returns:
#             str: Strategy name to use
#         """
#         if attempt == 1:
#             # First attempt: try standard approach
#             return 'standard'
        
#         # Find most recent scores from log
#         last_scores = None
#         for entry in reversed(agent_log):
#             if entry.get('type') == 'evaluation' and 'scores' in entry:
#                 last_scores = entry['scores']
#                 break
        
#         if not last_scores:
#             return 'standard'
        
#         # AUTONOMOUS DECISION LOGIC
#         # Agent analyzes which dimension failed and chooses appropriate strategy
#         faith_score = last_scores.get('faithfulness', {}).get('score', 5)
#         complete_score = last_scores.get('completeness', {}).get('score', 5)
#         robust_score = last_scores.get('robustness', {}).get('score', 5)
        
#         # Priority order: faithfulness > completeness > robustness
#         if faith_score < 4:
#             # Facts were changed - be more conservative
#             return 'conservative'
#         elif complete_score < 4:
#             # Information was lost - focus on preservation
#             return 'preserve_details'
#         elif robust_score < 4:
#             # Structure issues - focus on clarity
#             return 'clarity_focus'
#         else:
#             # Close to goal but not quite - try conservative approach
#             return 'conservative'
    
#     def _generate_with_strategy(self, original, task, tone, selected_text, strategy):
#         """
#         Generate email using specified strategy.
        
#         Args:
#             original (str): Original email
#             task (str): Task type
#             tone (str): Target tone (if applicable)
#             selected_text (str): Selected text (if applicable)
#             strategy (str): Strategy name
            
#         Returns:
#             str: Generated email
#         """
#         strategy_config = self.strategies[strategy]
        
#         # Generate with strategy-specific modifier
#         if task == 'tone' and tone:
#             result = self.generator.generate(
#                 task, 
#                 original, 
#                 tone,
#                 selected_text=selected_text
#             )
#         else:
#             result = self.generator.generate(
#                 task, 
#                 original,
#                 selected_text=selected_text
#             )
        
#         return result
    
#     def _evaluate(self, original, generated):
#         """
#         Evaluate generated email using the judge.
        
#         Args:
#             original (str): Original email
#             generated (str): Generated email
            
#         Returns:
#             dict: Evaluation scores
#         """
#         return self.judge.evaluate(original, generated)
    
#     def _diagnose_failure(self, scores):
#         """
#         Diagnose why the quality goal wasn't met.
        
#         Agent analyzes which dimensions are below threshold and
#         provides diagnostic information for strategy selection.
        
#         Args:
#             scores (dict): Evaluation scores
            
#         Returns:
#             list: List of issues found
#         """
#         issues = []
        
#         if scores['faithfulness']['score'] < 4:
#             issues.append({
#                 'type': 'faithfulness',
#                 'score': scores['faithfulness']['score'],
#                 'description': scores['faithfulness']['reason']
#             })
        
#         if scores['completeness']['score'] < 4:
#             issues.append({
#                 'type': 'completeness',
#                 'score': scores['completeness']['score'],
#                 'description': scores['completeness']['reason']
#             })
        
#         if scores['robustness']['score'] < 4:
#             issues.append({
#                 'type': 'robustness',
#                 'score': scores['robustness']['score'],
#                 'description': scores['robustness']['reason']
#             })
        
#         if not issues:
#             # Score is close but not quite at threshold
#             issues.append({
#                 'type': 'minor_improvement_needed',
#                 'score': scores['overall']['score'],
#                 'description': 'Score is close to threshold but not quite there'
#             })
        
#         return issues
    
#     # ==========================================
#     # Logging Methods for Transparency
#     # ==========================================
    
#     def _log_start(self, email, task, tone):
#         """Log agent initialization"""
#         return {
#             'type': 'start',
#             'timestamp': time.time(),
#             'message': f'🤖 Agent Goal: Achieve quality score ≥ {self.target_score}/5.0',
#             'email_length': len(email.split()),
#             'task': task,
#             'tone': tone,
#             'target_score': self.target_score,
#             'max_attempts': self.max_attempts
#         }
    
#     def _log_attempt_start(self, attempt, strategy):
#         """Log start of refinement attempt"""
#         return {
#             'type': 'attempt_start',
#             'timestamp': time.time(),
#             'attempt': attempt,
#             'message': f'🔄 Attempt {attempt}/{self.max_attempts}',
#             'strategy': strategy,
#             'strategy_description': self.strategies[strategy]['description']
#         }
    
#     def _log_evaluation(self, attempt, scores):
#         """Log evaluation results"""
#         return {
#             'type': 'evaluation',
#             'timestamp': time.time(),
#             'attempt': attempt,
#             'message': f'📊 Score: {scores["overall"]["score"]}/5.0',
#             'scores': scores
#         }
    
#     def _log_diagnosis(self, attempt, diagnosis):
#         """Log diagnostic analysis"""
#         return {
#             'type': 'diagnosis',
#             'timestamp': time.time(),
#             'attempt': attempt,
#             'message': f'⚠️  Analyzing issues for strategy adaptation',
#             'diagnosis': diagnosis
#         }
    
#     def _log_success(self, attempt, score):
#         """Log successful goal achievement"""
#         return {
#             'type': 'success',
#             'timestamp': time.time(),
#             'attempt': attempt,
#             'message': f'✅ Goal achieved! Final score: {score}/5.0',
#             'score': score
#         }
    
#     def _log_max_attempts(self, best_score):
#         """Log max attempts reached"""
#         return {
#             'type': 'max_attempts',
#             'timestamp': time.time(),
#             'message': f'⏱️  Max attempts reached. Best score: {best_score}/5.0',
#             'best_score': best_score
#         }


# if __name__ == "__main__":
#     # Quick test
#     print("Agentic Email Refinement Agent - Quick Test")
#     print("=" * 60)
    
#     agent = EmailRefinementAgent(target_score=4.5, max_attempts=3)
    
#     test_email = "Hey, meeting moved to next week. Will send invite."
    
#     result = agent.achieve_goal(test_email, task="lengthen")
    
#     print("\n" + "=" * 60)
#     print("RESULT")
#     print("=" * 60)
#     print(f"\nGoal Achieved: {result['goal_achieved']}")
#     print(f"Attempts Used: {result['attempts_used']}")
#     print(f"Final Score: {result['final_scores']['overall']['score']}/5.0")
#     print(f"\nFinal Output:\n{result['final_output']}")
"""
Agentic Email Refinement Agent v2

This module implements a fully agentic, probabilistic email refinement system
with:
- Best-of-N sampling
- Adaptive temperature oscillation
- Parallel generation for efficiency
- Self-reflection & dynamic constraint injection
- Utility-based selection of optimal output
"""

import os
import time
from dotenv import load_dotenv
from generate import GenerateEmail
from judge import EmailJudge
from concurrent.futures import ThreadPoolExecutor

load_dotenv()


class EmailRefinementAgent:
    """
    Fully agentic email refinement agent.
    
    Features:
    1. Explicit target score
    2. Autonomous strategy selection
    3. Self-evaluation & diagnostic analysis
    4. Adaptive probabilistic planning with oscillating temperature
    5. Best-of-N sampling for high reliability
    """

    def __init__(self, target_score=4.5, max_attempts=3, best_of_n=5, model=None):
        """
        Initialize the agent.
        
        Args:
            target_score (float): Target quality score (0-5)
            max_attempts (int): Max iterations
            best_of_n (int): Number of candidates per attempt
            model (str): Generator model
        """
        self.target_score = target_score
        self.max_attempts = max_attempts
        self.best_of_n = best_of_n

        # Model selection from environment
        self.model = model or os.getenv("OPENAI_AGENT1_MODEL", "gpt-4o-mini")
        self.judge_model = os.getenv("OPENAI_AGENT2_MODEL", "gpt-4.1")

        self.generator = GenerateEmail(model=self.model)
        self.judge = EmailJudge(model=self.judge_model)

        # Strategy definitions
        self.strategies = {
            'standard': {
                'description': 'Standard generation approach',
                'modifier': ''
            },
            'conservative': {
                'description': 'Minimal changes, preserve facts',
                'modifier': '\n\nCRITICAL: Preserve all facts, numbers, dates, and details exactly.'
            },
            'preserve_details': {
                'description': 'Ensure completeness and info retention',
                'modifier': '\n\nCRITICAL: Preserve all original content; do not omit any details.'
            },
            'clarity_focus': {
                'description': 'Improve structure and clarity',
                'modifier': '\n\nCRITICAL: Improve clarity, flow, and structure while preserving content.'
            }
        }

    def achieve_goal(self, original_email, task, tone=None, selected_text=None):
        """
        Main agent loop: iteratively refine email to reach target score.
        
        Returns:
            dict with keys:
                final_output, final_scores, attempts_used, agent_log, goal_achieved
        """
        agent_log = []
        best_output = None
        best_score = 0
        best_scores = None
        temperature = 0.5  # initial temperature

        # Log start
        log_entry = self._log_start(original_email, task, tone)
        agent_log.append(log_entry)
        print(f"\n{log_entry['message']}")

        for attempt in range(1, self.max_attempts + 1):
            print(f"\n{'='*60}")

            # Adaptive temperature oscillation
            if attempt > 1:
                temperature = min(1.0, temperature + 0.2)  # increase randomness
            print(f"🔥 Temperature set to: {temperature}")

            # Choose strategy
            strategy = self._choose_strategy(attempt, agent_log)
            log_entry = self._log_attempt_start(attempt, strategy, temperature)
            agent_log.append(log_entry)
            print(f"{log_entry['message']}")
            print(f"💭 Strategy: {log_entry['strategy_description']}")

            # Best-of-N generation
            candidates = self._generate_best_of_n(
                original_email, task, tone, selected_text, strategy, temperature
            )

            # Evaluate candidates
            scored_candidates = []
            for cand in candidates:
                scores = self._evaluate(original_email, cand)
                scored_candidates.append((cand, scores))

            # Pick best candidate
            best_candidate, candidate_scores = max(
                scored_candidates, key=lambda x: x[1]['overall']['score']
            )
            current_score = candidate_scores['overall']['score']

            log_entry = self._log_evaluation(attempt, candidate_scores)
            agent_log.append(log_entry)
            print(f"{log_entry['message']}")

            # Track overall best
            if current_score > best_score:
                best_score = current_score
                best_output = best_candidate
                best_scores = candidate_scores

            # Check goal achievement
            if current_score >= self.target_score:
                log_entry = self._log_success(attempt, current_score)
                agent_log.append(log_entry)
                print(f"\n{log_entry['message']}")
                return {
                    'final_output': best_candidate,
                    'final_scores': candidate_scores,
                    'attempts_used': attempt,
                    'agent_log': agent_log,
                    'goal_achieved': True
                }

            else:
                # Diagnose failure and adapt
                diagnosis = self._diagnose_failure(candidate_scores)
                log_entry = self._log_diagnosis(attempt, diagnosis)
                agent_log.append(log_entry)
                issue_types = ', '.join([d['type'] for d in diagnosis])
                print(f"⚠️  Issues detected: {issue_types}")
                if attempt < self.max_attempts:
                    print("🔧 Agent adapting strategy for next attempt...")

        # Max attempts reached
        log_entry = self._log_max_attempts(best_score)
        agent_log.append(log_entry)
        print(f"\n{log_entry['message']}")

        return {
            'final_output': best_output,
            'final_scores': best_scores,
            'attempts_used': self.max_attempts,
            'agent_log': agent_log,
            'goal_achieved': False
        }

    # ========================
    # Best-of-N Generation
    # ========================
    def _generate_best_of_n(self, original, task, tone, selected_text, strategy, temperature):
        """
        Generate multiple candidates in parallel to select the highest scoring.
        """
        candidates = []

        def gen_task():
            return self._generate_with_strategy(original, task, tone, selected_text, strategy, temperature)

        # Parallel generation
        with ThreadPoolExecutor(max_workers=self.best_of_n) as executor:
            futures = [executor.submit(gen_task) for _ in range(self.best_of_n)]
            for fut in futures:
                candidates.append(fut.result())

        return candidates

    # ========================
    # Generation with strategy
    # ========================
    def _generate_with_strategy(self, original, task, tone, selected_text, strategy, temperature):
        """
        Generate email with specific strategy and dynamic temperature.
        """
        if task == 'tone' and tone:
            return self.generator.generate(
                task, original, tone,
                selected_text=selected_text,
                strategy_modifier=self.strategies[strategy]['modifier'],
                temperature=temperature
            )
        else:
            return self.generator.generate(
                task, original,
                selected_text=selected_text,
                strategy_modifier=self.strategies[strategy]['modifier'],
                temperature=temperature
            )

    # ========================
    # Evaluation & Diagnosis
    # ========================
    def _evaluate(self, original, generated):
        return self.judge.evaluate(original, generated)

    def _diagnose_failure(self, scores):
        issues = []
        if scores['faithfulness']['score'] < 4:
            issues.append({'type': 'faithfulness', 'score': scores['faithfulness']['score'],
                           'description': scores['faithfulness']['reason']})
        if scores['completeness']['score'] < 4:
            issues.append({'type': 'completeness', 'score': scores['completeness']['score'],
                           'description': scores['completeness']['reason']})
        if scores['robustness']['score'] < 4:
            issues.append({'type': 'robustness', 'score': scores['robustness']['score'],
                           'description': scores['robustness']['reason']})
        if not issues:
            issues.append({'type': 'minor_improvement_needed',
                           'score': scores['overall']['score'],
                           'description': 'Score is close to threshold but not quite there'})
        return issues

    # ========================
    # Strategy selection
    # ========================
    def _choose_strategy(self, attempt, agent_log):
        if attempt == 1:
            return 'standard'

        last_scores = None
        for entry in reversed(agent_log):
            if entry.get('type') == 'evaluation' and 'scores' in entry:
                last_scores = entry['scores']
                break

        if not last_scores:
            return 'standard'

        faith_score = last_scores.get('faithfulness', {}).get('score', 5)
        complete_score = last_scores.get('completeness', {}).get('score', 5)
        robust_score = last_scores.get('robustness', {}).get('score', 5)

        if faith_score < 4:
            return 'conservative'
        elif complete_score < 4:
            return 'preserve_details'
        elif robust_score < 4:
            return 'clarity_focus'
        else:
            return 'conservative'

    # ========================
    # Logging
    # ========================
    def _log_start(self, email, task, tone):
        return {'type': 'start', 'timestamp': time.time(),
                'message': f'🤖 Agent Goal: Achieve quality score ≥ {self.target_score}/5.0',
                'email_length': len(email.split()), 'task': task, 'tone': tone,
                'target_score': self.target_score, 'max_attempts': self.max_attempts}

    def _log_attempt_start(self, attempt, strategy, temperature):
        return {'type': 'attempt_start', 'timestamp': time.time(), 'attempt': attempt,
                'message': f'🔄 Attempt {attempt}/{self.max_attempts} (Temp={temperature})',
                'strategy': strategy,
                'strategy_description': self.strategies[strategy]['description']}

    def _log_evaluation(self, attempt, scores):
        return {'type': 'evaluation', 'timestamp': time.time(), 'attempt': attempt,
                'message': f'📊 Score: {scores["overall"]["score"]}/5.0', 'scores': scores}

    def _log_diagnosis(self, attempt, diagnosis):
        return {'type': 'diagnosis', 'timestamp': time.time(), 'attempt': attempt,
                'message': f'⚠️  Analyzing issues for strategy adaptation', 'diagnosis': diagnosis}

    def _log_success(self, attempt, score):
        return {'type': 'success', 'timestamp': time.time(), 'attempt': attempt,
                'message': f'✅ Goal achieved! Final score: {score}/5.0', 'score': score}

    def _log_max_attempts(self, best_score):
        return {'type': 'max_attempts', 'timestamp': time.time(),
                'message': f'⏱️  Max attempts reached. Best score: {best_score}/5.0',
                'best_score': best_score}


if __name__ == "__main__":
    print("Agentic Email Refinement Agent v2 - Quick Test")
    print("=" * 60)

    agent = EmailRefinementAgent(target_score=4.5, max_attempts=3, best_of_n=5)

    test_email = "Hey, meeting moved to next week. Will send invite."

    result = agent.achieve_goal(test_email, task="lengthen")

    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"\nGoal Achieved: {result['goal_achieved']}")
    print(f"Attempts Used: {result['attempts_used']}")
    print(f"Final Score: {result['final_scores']['overall']['score']}/5.0")
    print(f"\nFinal Output:\n{result['final_output']}")
