# 📧 AI Email Editor & Evaluation Framework

## 📋 Overview
This project is a comprehensive AI-powered email editing tool designed to assist users in refining their emails. It allows for **changing tone**, **shortening**, and **lengthening** emails while strictly preserving critical information such as URLs.

Beyond the application itself, this repository contains a robust **End-to-End Evaluation Framework** used to validate the performance of different LLMs (e.g., GPT-4o-mini vs. GPT-4.1) on these tasks.

## ✨ Key Features
-   **Multi-Action Editing**:
    -   **Change Tone**: Convert emails to *Professional*, *Friendly*, or *Sympathetic* tones.
    -   **Shorten**: Condense emails without losing key details.
    -   **Elaborate**: Expand on brief points to create full emails.
-   **Constraint Preservation**: Specialized logic to ensure URLs and specific formatting remain untouched during edits.
-   **Real-time Evaluation**: Built-in "LLM-as-a-Judge" feedback loop to score the AI's output on *Faithfulness*, *Completeness*, and *Robustness*.
-   **Agentic Refinement**: Autonomous agent (`agent.py`) that iteratively improves emails through self-evaluation and adaptive strategies until it meets quality targets.
-   **Interactive UI**: A user-friendly Streamlit application for testing and demoing features.

## 📂 Project Structure

### 1. Core Application
-   **`app.py`**: The main Streamlit web application.
-   **`generate.py`**: Handles interaction with OpenAI's API for generating email edits.
-   **`judge.py`**: Contains the logic for the "LLM Judge" to evaluate outputs.
-   **`agent.py`**: Implementation of the **EmailRefinementAgent**, an autonomous loop that generates, evaluates, diagnoses issues, and adapts its strategy to achieve high-quality results.

### 2. Tone Analysis (`/tone`)
Dedicated module for testing model performance on tone shifting.
-   **`tone_evaluation.py`**: Script to evaluate how well models shift tones (e.g., Rude -> Professional).
-   **`evaluation_results.json`**: Detailed logs of model performance on tone tasks.
-   **`tone_report.md`**: Summary report of tone accuracy stats.

### 3. URL Preservation (`/url`)
Critical module ensuring models do not hallucinate or modify hyperlinks.
-   **`url_synthesis.py`**: Generates synthetic emails containing complex URLs and IP addresses.
-   **`url_evaluate.py`**: Runs evaluation to check if URLs are preserved character-for-character.
-   **`full_matrix_metrics.csv`**: Comprehensive results comparing different models on URL tasks.

### 4. Synthetic Data
-   **`/synthetic_datasets`**: Contains generated JSONL files used for testing.
-   **`/datasets`**: Source files for the app's default examples.

### 5. Chrome Extension (`/gmail-ai-editor`)
A browser extension to bring the AI editor directly into the Gmail interface.
-   **`manifest.json`**: Extension configuration.
-   **`content.js`**: Script that interacts with the Gmail DOM to inject buttons and read email content.
-   **`popup.html/js`**: UI for the extension's popup window.

### 6. Selected Text (`/select`)
Module for "Elaborate" and other text selection based features.
-   **`selected_text_synthesis.py`**: Generates synthetic data for selected text operations.
-   **`selected_text_evaluate.py`**: Evaluates model performance on selected text tasks.

### 7. Datasets Evaluator (`/datasets_evaluator`)
General purpose evaluation scripts for the core datasets.
-   **`cross_eval.py`**: Runs cross-evaluation across different models and tasks.
-   **`analytics.py`**: helper script for analyzing evaluation results.


## 🚀 Getting Started

### Prerequisites
-   Python 3.8+
-   OpenAI API Key

### Installation
1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up Environment**:
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_api_key_here
    OPENAI_MODEL=gpt-4.1  # or gpt-4o-mini
    ```

### Running the App
Launch the Streamlit interface:
```bash
streamlit run app.py
```

### Installing the Chrome Extension
1.  Open Chrome and go to `chrome://extensions/`.
2.  Enable **Developer mode** in the top-right corner.
3.  Click **Load unpacked**.
4.  Select the `gmail-ai-editor` folder from this repository.
5.  Open Gmail, compose a new email, and look for the AI Assistant toolbar.

## 📊 Evaluation Framework
To run the evaluations yourself:

**For Tone:**
```bash
cd tone
python tone_evaluation.py
```

**For URL Preservation:**
```bash
cd url
python url_evaluate.py
```

## 🤖 Models Used
-   **Generative Models**: `gpt-4o-mini`, `gpt-4.1` (Custom fine-tunes or aliases).
-   **Judge Model**: Typically a stronger model (e.g., GPT-4o) used to score the outputs of the smaller generative models.

## ☁️ Deployment
For instructions on deploying to Streamlit Cloud, see [DEPLOYING.md](DEPLOYING.md).

## 📝 License
[Your License Here]
