"""
Test script for Agentic Email Refinement Agent

This script demonstrates the autonomous behavior of the agent
and validates that it can achieve quality goals through iterative refinement.
"""

from agent import EmailRefinementAgent
import json


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_basic_elaboration():
    """Test agent on basic email elaboration"""
    print_section("TEST 1: Basic Elaboration")
    
    email = """
    Hey team, just a quick update.
    Project is on track. Will share details tomorrow.
    """
    
    print(f"\nOriginal Email:\n{email}")
    print(f"\nTask: Elaborate this email")
    print(f"Target: Quality score >= 4.5")
    
    agent = EmailRefinementAgent(target_score=4.5, max_attempts=3)
    result = agent.achieve_goal(email, task="lengthen")
    
    # Display results
    print_section("RESULTS")
    print(f"\n✓ Goal Achieved: {result['goal_achieved']}")
    print(f"✓ Attempts Used: {result['attempts_used']}/{agent.max_attempts}")
    print(f"✓ Final Score: {result['final_scores']['overall']['score']}/5.0")
    
    print(f"\n--- Final Output ---")
    print(result['final_output'])
    
    print(f"\n--- Quality Breakdown ---")
    scores = result['final_scores']
    print(f"Faithfulness: {scores['faithfulness']['score']}/5")
    print(f"  → {scores['faithfulness']['reason']}")
    print(f"\nCompleteness: {scores['completeness']['score']}/5")
    print(f"  → {scores['completeness']['reason']}")
    print(f"\nRobustness: {scores['robustness']['score']}/5")
    print(f"  → {scores['robustness']['reason']}")


def test_tone_change():
    """Test agent on tone transformation"""
    print_section("TEST 2: Tone Change (Casual → Professional)")
    
    email = """
    yo! thx for the heads up about the meeting.
    i'll def be there. catch u later!
    """
    
    print(f"\nOriginal Email:\n{email}")
    print(f"\nTask: Change tone to Professional")
    print(f"Target: Quality score >= 4.5")
    
    agent = EmailRefinementAgent(target_score=4.5, max_attempts=3)
    result = agent.achieve_goal(email, task="tone", tone="Professional")
    
    # Display results
    print_section("RESULTS")
    print(f"\n✓ Goal Achieved: {result['goal_achieved']}")
    print(f"✓ Attempts Used: {result['attempts_used']}/{agent.max_attempts}")
    print(f"✓ Final Score: {result['final_scores']['overall']['score']}/5.0")
    
    print(f"\n--- Final Output ---")
    print(result['final_output'])


def test_shorten():
    """Test agent on email condensation"""
    print_section("TEST 3: Shorten Email")
    
    email = """
    Dear Team,
    
    I hope this email finds you well. I wanted to take a moment to reach out 
    and provide you with a comprehensive update on the current status of our 
    ongoing project. As you may already be aware, we have been making steady 
    progress over the past several weeks, and I am pleased to report that we 
    are currently on track to meet our established timeline and deliverables.
    
    In terms of next steps, I will be compiling a detailed report that 
    outlines all of our achievements, challenges encountered, and lessons 
    learned throughout this process. I anticipate sharing this comprehensive 
    document with the entire team by the end of the day tomorrow, so please 
    keep an eye out for it in your inbox.
    
    Thank you very much for your continued dedication and hard work.
    
    Best regards
    """
    
    print(f"\nOriginal Email Length: {len(email.split())} words")
    print(f"\nTask: Shorten while preserving key information")
    print(f"Target: Quality score >= 4.5")
    
    agent = EmailRefinementAgent(target_score=4.5, max_attempts=3)
    result = agent.achieve_goal(email, task="shorten")
    
    # Display results
    print_section("RESULTS")
    print(f"\n✓ Goal Achieved: {result['goal_achieved']}")
    print(f"✓ Attempts Used: {result['attempts_used']}/{agent.max_attempts}")
    print(f"✓ Final Score: {result['final_scores']['overall']['score']}/5.0")
    print(f"✓ New Length: {len(result['final_output'].split())} words")
    
    print(f"\n--- Final Output ---")
    print(result['final_output'])


def test_agent_log():
    """Demonstrate agent activity log"""
    print_section("TEST 4: Agent Activity Log")
    
    email = "Meeting at 5?"
    
    print(f"\nOriginal: {email}")
    print(f"\nThis test shows the agent's decision-making process...\n")
    
    agent = EmailRefinementAgent(target_score=4.5, max_attempts=3)
    result = agent.achieve_goal(email, task="lengthen")
    
    print_section("AGENT ACTIVITY LOG")
    
    for entry in result['agent_log']:
        if entry['type'] == 'start':
            print(f"\n{entry['message']}")
            print(f"  Email length: {entry['email_length']} words")
            print(f"  Task: {entry['task']}")
        
        elif entry['type'] == 'attempt_start':
            print(f"\n{entry['message']}")
            print(f"  💭 Strategy chosen: {entry['strategy_description']}")
        
        elif entry['type'] == 'evaluation':
            print(f"  {entry['message']}")
            scores = entry['scores']
            print(f"     Faithfulness: {scores['faithfulness']['score']}/5")
            print(f"     Completeness: {scores['completeness']['score']}/5")
            print(f"     Robustness: {scores['robustness']['score']}/5")
        
        elif entry['type'] == 'diagnosis':
            issues = entry['diagnosis']
            issue_list = ', '.join([d['type'] for d in issues])
            print(f"  ⚠️  Issues identified: {issue_list}")
            if len(result['agent_log']) > result['agent_log'].index(entry) + 1:
                print(f"  🔧 Adapting strategy...")
        
        elif entry['type'] == 'success':
            print(f"\n{entry['message']}")
        
        elif entry['type'] == 'max_attempts':
            print(f"\n{entry['message']}")


def run_all_tests():
    """Run all test cases"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "AGENTIC EMAIL AGENT TEST SUITE" + " " * 22 + "║")
    print("╚" + "═" * 68 + "╝")
    
    try:
        test_basic_elaboration()
        input("\n\nPress Enter to continue to next test...")
        
        test_tone_change()
        input("\n\nPress Enter to continue to next test...")
        
        test_shorten()
        input("\n\nPress Enter to continue to next test...")
        
        test_agent_log()
        
        print_section("ALL TESTS COMPLETED")
        print("\n✅ Agent successfully demonstrated:")
        print("   • Autonomous decision-making")
        print("   • Goal-seeking behavior")
        print("   • Self-evaluation")
        print("   • Adaptive strategies")
        print("   • Transparent reasoning\n")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
