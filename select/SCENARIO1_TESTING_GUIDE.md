# Scenario 1: Selected Text Preservation Testing Guide

## Overview

This guide covers testing for **Scenario 1: Selected Text Preservation** - evaluating whether AI models correctly edit ONLY the selected portion of an email while leaving surrounding text completely unchanged.

## The Problem

Email Helper actions (shorten, lengthen, tone change) should apply **only to user-highlighted text**, not the entire email. Some models fail this and modify the full email even when only a portion is selected.

---

## Files Structure

```
selected_text_prompts.yaml          # Prompt configurations
selected_text_synthesis.py          # Dataset generation
selected_text_evaluate.py           # Evaluation script
selected_text_compare.py            # Model comparison
SCENARIO1_TESTING_GUIDE.md          # This guide
```

---

## Quick Start

### 1. Generate Test Dataset

```bash
# Generate 50 samples (default)
python selected_text_synthesis.py

# Generate custom number of samples
python selected_text_synthesis.py --count 100

# Custom output file
python selected_text_synthesis.py --count 50 --output my_dataset.jsonl
```

**Output:** `selected_text_dataset.jsonl`

**Dataset Structure:**
```json
{
  "id": 1,
  "topic": "Requesting feedback on a proposal",
  "persona": "a marketing manager",
  "tone": "professional",
  "action": "shorten_selection",
  "tone_type": null,
  "full_email": "Full email text...",
  "before_selection": "Text before the selected portion...",
  "selected_text": "The portion that should be edited...",
  "after_selection": "Text after the selected portion..."
}
```

---

### 2. Evaluate a Model

```bash
# Evaluate GPT-4.1
python selected_text_evaluate.py --model gpt-4.1

# Evaluate GPT-4o-mini
python selected_text_evaluate.py --model gpt-4o-mini

# Custom dataset and output
python selected_text_evaluate.py \
  --model gpt-4.1 \
  --dataset my_dataset.jsonl \
  --output my_results.jsonl

# Process limited samples (for testing)
python selected_text_evaluate.py --model gpt-4.1 --limit 10
```

**Output:** `selected_text_results_{model}.jsonl`

---

### 3. Compare Models

```bash
# Compare two or more models
python selected_text_compare.py \
  --results selected_text_results_gpt-4.1.jsonl \
            selected_text_results_gpt-4o-mini.jsonl

# Custom output report
python selected_text_compare.py \
  --results selected_text_results_*.jsonl \
  --output my_comparison.json
```

**Output:** `selected_text_comparison_report.json`

---

## Understanding Results

### Evaluation Metrics

#### 1. **Selection Boundary Preservation** (Primary Metric)
- **5**: Perfect - Only selected portion edited, surrounding text 100% unchanged
- **4**: Near-perfect - Trivial changes to surrounding (whitespace only)
- **3**: Partial - Minor modifications to surrounding text
- **2**: Poor - Significant changes to surrounding text
- **1**: Failed - Entire email modified
- **0**: Catastrophic - Unusable output

#### 2. **Edit Quality**
Measures how well the edit achieves the requested action (shorten/lengthen/tone).

#### 3. **Faithfulness**
Ensures no facts are added or removed from the selected portion.

#### 4. **Completeness**
Verifies all key information in selection is preserved.

#### 5. **Overall Score**
Average of the four metrics above.

---

### Boundary Check (Automated)

The evaluation includes a programmatic check:

```python
{
  "correctly_scoped": true/false,  # Model returned ONLY edited selection
  "contains_before_text": false,   # Should be false
  "contains_after_text": false     # Should be false
}
```

**Ideal Result:** `correctly_scoped = true`

---

## Sample Workflow

### Complete End-to-End Testing

```bash
# Step 1: Generate dataset
python selected_text_synthesis.py --count 50

# Step 2: Evaluate multiple models
python selected_text_evaluate.py --model gpt-4.1
python selected_text_evaluate.py --model gpt-4o-mini

# Step 3: Compare results
python selected_text_compare.py \
  --results selected_text_results_gpt-4.1.jsonl \
            selected_text_results_gpt-4o-mini.jsonl
```

---

## Configuration

### Environment Variables

Required in `.env`:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://api.openai.com/v1

# Model Configuration
MODEL_NAME=gpt-4o-mini           # For dataset generation
EVALUATE_MODEL=gpt-4.1           # For evaluation
```

### Customizing Prompts

Edit `selected_text_prompts.yaml` to modify:
- System instructions for editing
- Evaluation criteria
- Scoring rubrics

---

## Expected Results

### High-Performing Model
- **Selection Boundary Preservation**: 4.5-5.0/5
- **Correctly Scoped Rate**: >95%
- **Overall Score**: >4.0/5

### Failing Model
- **Selection Boundary Preservation**: <3.0/5
- **Correctly Scoped Rate**: <50%
- Modifies text outside selection boundaries

---

## Troubleshooting

### Issue: Model returns full email instead of just edited selection

**Diagnosis:** Model doesn't understand the task  
**Solution:** Check prompts in `selected_text_prompts.yaml`, ensure clear markers

### Issue: Evaluation scores seem inconsistent

**Diagnosis:** Evaluator model misunderstanding  
**Solution:** Use GPT-4.1 as evaluator (set `EVALUATE_MODEL=gpt-4.1`)

### Issue: Dataset generation fails

**Diagnosis:** API errors or missing configuration  
**Solution:** Verify `.env` file, check API key and base URL

---

## Best Practices

1. **Generate diverse datasets**: Use default 50+ samples for reliable metrics
2. **Consistent evaluator**: Always use the same evaluator model (GPT-4.1 recommended)
3. **Multiple runs**: Run evaluation multiple times to account for temperature variance
4. **Review failures**: Manually inspect samples with low scores to identify patterns

---

## Integration with Scenario 2 (URL Preservation)

Both scenarios can be tested independently or combined:

```bash
# Test both scenarios sequentially
python url_synthesis.py --count 50
python url_evaluate.py --model gpt-4.1

python selected_text_synthesis.py --count 50
python selected_text_evaluate.py --model gpt-4.1
```

For combined testing, create emails that have:
- Selected text portions (Scenario 1)
- URLs within the selected portions (Scenario 2)

This tests both defects simultaneously.

---

## Next Steps

1. ✅ Generate initial dataset
2. ✅ Evaluate baseline model (GPT-4o-mini)
3. ✅ Evaluate comparison model (GPT-4.1)
4. ✅ Compare results
5. 📊 Present findings to stakeholders
6. 🎯 Recommend best model for Email Helper feature

---

## Support

For issues or questions, refer to:
- Prompt configurations: `selected_text_prompts.yaml`
- URL testing guide: `URL_TESTING_GUIDE.md`
- Main README: `README.md`
