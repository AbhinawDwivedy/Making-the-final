# Chrome Extension Setup & File Guide

## 1. How to Setup (Developer Mode)

Follow these steps to load your extension into Google Chrome for testing and development:

1.  **Open Chrome Extensions Page**
    *   Open Google Chrome.
    *   Navigate to `chrome://extensions` in the address bar.
    *   Alternatively, click the puzzle piece icon (Extensions) > "Manage Extensions".

2.  **Enable Developer Mode**
    *   In the top-right corner of the Extensions page, toggle the **Developer mode** switch to **ON**.

3.  **Load Unpacked Extension**
    *   Click the **"Load unpacked"** button that appears in the top-left toolbar.
    *   A file picker window will open. Navigate to and select the `gmail-ai-editor` folder (the folder containing `manifest.json`).

4.  **Verify Installation**
    *   You should now see "AI Email Editor" card in your list of extensions.
    *   Ensure the toggle on the card is blue (Enabled).
    *   Go to Gmail (`mail.google.com`) and refresh the page to see the extension in action.

5.  **Reloading Changes**
    *   If you make changes to the code, go back to `chrome://extensions` and click the **refresh icon** (circular arrow) on your extension's card.
    *   Then, reload your Gmail tab to apply the changes.

---

## 2. File Explanations

Here is a breakdown of the key files in your `gmail-ai-editor` folder and how they work together:

### **1. `manifest.json`**
*   **What it is:** The configuration file (blueprint) for the extension.
*   **What it does:** tells Chrome essential details like the extension's name, version, permissions (e.g., access to `mail.google.com`), and which scripts to run.
*   **Key part:** It defines `content_scripts` effectively saying "Run `content.js` whenever the user visits Gmail".

### **2. `content.js`**
*   **What it is:** The main logic script that runs *inside* the Gmail web page.
*   **What it does:**
    *   Interacts with the Gmail DOM (page structure).
    *   Finds the unread email body or the compose window.
    *   Injects the custom buttons (like the AI dropdown or "Agentic Refinement" modal) into the Gmail interface.
    *   Reads the email text, sends it to your backend (server), and replaces the text with the AI-generated version.
    *   Handles the "Agentic Mode" UI, including the progress modal and sidebar chat.

### **3. `popup.html`**
*   **What it is:** The layout file for the small window that appears when you click the extension icon in the Chrome browser toolbar.
*   **What it does:** Provides a simple menu with buttons like "Shorten", "Elaborate", and "Make Professional".

### **4. `popup.js`**
*   **What it is:** The logic for `popup.html`.
*   **What it does:** Listen for clicks on the popup buttons. When a button is clicked, it sends a message to the active tab (Gmail) telling `content.js` to execute a specific action (e.g., "rewrite this email to be professional").

### **5. `ext_prompts.yaml`**
*   **What it is:** A data file storing the prompt templates.
*   **What it does:** Centralizes the instructions for the AI. Instead of hardcoding prompts in JavaScript, they are stored here for easy editing. *Note: In this specific architecture, these prompts are likely read by your Python backend server, not directly by the browser extension itself.*
