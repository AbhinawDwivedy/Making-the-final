
import json
import pandas as pd
from collections import Counter

def analyze_tone_results(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    
    if not data:
        print("No data found.")
        return

    df = pd.DataFrame(data)
    
    total_samples = len(df)
    pass_rate = df['pass'].mean() * 100
    avg_score = df['score'].mean()
    
    print(f"Total Samples: {total_samples}")
    print(f"Overall Pass Rate: {pass_rate:.2f}%")
    print(f"Average Score: {avg_score:.2f}")
    
    print("\n--- Breakdown by Target Tone ---")
    tone_stats = df.groupby('target_tone').agg(
        Count=('id', 'count'),
        Pass_Rate=('pass', 'mean'),
        Avg_Score=('score', 'mean')
    )
    tone_stats['Pass_Rate'] = tone_stats['Pass_Rate'] * 100
    print(tone_stats)
    
    print("\n--- Breakdown by Persona ---")
    persona_stats = df.groupby('persona').agg(
        Count=('id', 'count'),
        Pass_Rate=('pass', 'mean'),
        Avg_Score=('score', 'mean')
    )
    persona_stats['Pass_Rate'] = persona_stats['Pass_Rate'] * 100
    print(persona_stats)

    print("\n--- Failure Analysis ---")
    failures = df[~df['pass']]
    print(f"Total Failures: {len(failures)}")
    if len(failures) > 0:
        print("Sample Failures:")
        print(failures[['id', 'target_tone', 'persona', 'score']].head(5))

if __name__ == "__main__":
    analyze_tone_results('c:/Users/dwive/OneDrive/画像/ai_till week1/tone/cross_eval_results.jsonl')
