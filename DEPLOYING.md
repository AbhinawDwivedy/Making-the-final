# Deploying to Streamlit Cloud

This guide will walk you through deploying the AI Email Editor to Streamlit Cloud.

## Prerequisites

1.  **GitHub Account**: You need to host this code on GitHub.
2.  **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io/).
3.  **OpenAI API Key**: You will need your API key for the "Secrets" configuration.

## Step 1: Push Code to GitHub

Ensure your project is a public (or private) repository on GitHub.
If you haven't pushed it yet:

1.  Create a new repository on GitHub.
2.  Run the following commands in your terminal:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    git push -u origin main
    ```

## Step 2: Deploy on Streamlit Cloud

1.  Log in to [Streamlit Cloud](https://share.streamlit.io/).
2.  Click **New app** (top right).
3.  **Repository**: Select your GitHub repository (`YOUR_USERNAME/YOUR_REPO_NAME`).
4.  **Branch**: Select `main`.
5.  **Main file path**: Enter `app.py`.
6.  Click **Deploy!**

## Step 3: Configure Secrets

The app needs your OpenAI API Key to function. Do NOT commit your `.env` file to GitHub. Instead:

1.  Once the app is processing (or if it fails immediately), click the **Settings** menu (three dots in lower right or "Manage app" in dashboard).
2.  Go to **Secrets**.
3.  Paste the following configuration:

    ```toml
    OPENAI_API_KEY = "sk-..."
    OPENAI_MODEL = "gpt-4o-mini"
    ```
    *(Replace `sk-...` with your actual OpenAI API Key)*

4.  Click **Save**.

## Step 4: Reboot

If the app failed initially due to missing keys, go to the app menu and select **Reboot**.

Your app should now be live! 🚀
