const BUTTON_ID = "ai-rewrite-btn";
const DROPDOWN_ID = "ai-rewrite-dropdown";
const CHAT_SIDEBAR_ID = "ai-chat-sidebar";

// --- STYLES ---
const STYLES = `
  .ai-dropdown-container {
    position: relative;
    display: inline-block;
  }
  .ai-main-btn {
    margin-left: 8px;
    padding: 0 10px;
    height: 36px;
    border: 1px solid #dadce0;
    border-radius: 4px;
    cursor: pointer;
    background: #fff;
    font-weight: 500;
    color: #3c4043;
    display: flex;
    align-items: center;
    font-family: 'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;
    font-size: 14px;
  }
  .ai-main-btn:hover {
    background-color: #f1f3f4;
    border-color: #dadce0;
  }
  .ai-dropdown-menu {
    display: none;
    position: absolute;
    bottom: 100%;
    left: 8px;
    background-color: white;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 10000;
    border-radius: 4px;
    padding: 8px 0;
    margin-bottom: 5px;
  }
  .ai-dropdown-item {
    color: #3c4043;
    padding: 8px 16px;
    text-decoration: none;
    display: block;
    cursor: pointer;
    font-family: Roboto,sans-serif;
    font-size: 13px;
  }
  .ai-dropdown-item:hover {
    background-color: #f1f3f4;
  }
  .show {display:block;}

  /* Chat Sidebar Styles */
  .ai-chat-sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: 380px;
    height: 100vh;
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    box-shadow: -4px 0 20px rgba(0,0,0,0.3);
    z-index: 100000;
    display: flex;
    flex-direction: column;
    font-family: 'Google Sans', Roboto, sans-serif;
    transition: transform 0.3s ease;
  }
  .ai-chat-sidebar.hidden {
    transform: translateX(100%);
  }
  .ai-chat-header {
    padding: 16px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
  }
  .ai-chat-header h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .ai-chat-close {
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
  }
  .ai-chat-close:hover {
    background: rgba(255,255,255,0.3);
  }
  .ai-chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .ai-chat-message {
    max-width: 85%;
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.5;
    animation: fadeIn 0.3s ease;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .ai-chat-message.user {
    align-self: flex-end;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 4px;
  }
  .ai-chat-message.assistant {
    align-self: flex-start;
    background: rgba(255,255,255,0.1);
    color: #e0e0e0;
    border-bottom-left-radius: 4px;
  }
  .ai-chat-message.assistant .apply-btn {
    margin-top: 10px;
    padding: 8px 14px;
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    border: none;
    border-radius: 20px;
    color: white;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .ai-chat-message.assistant .apply-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4);
  }
  .ai-chat-input-area {
    padding: 16px;
    background: rgba(0,0,0,0.2);
    display: flex;
    gap: 10px;
    flex-shrink: 0;
  }
  .ai-chat-input {
    flex: 1;
    padding: 12px 16px;
    border: none;
    border-radius: 24px;
    background: rgba(255,255,255,0.1);
    color: white;
    font-size: 14px;
    outline: none;
    transition: background 0.2s;
  }
  .ai-chat-input::placeholder {
    color: rgba(255,255,255,0.5);
  }
  .ai-chat-input:focus {
    background: rgba(255,255,255,0.15);
  }
  .ai-chat-send {
    width: 44px;
    height: 44px;
    border: none;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .ai-chat-send:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
  }
  .ai-chat-send:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
  .ai-typing-indicator {
    display: flex;
    gap: 4px;
    padding: 12px 16px;
    background: rgba(255,255,255,0.1);
    border-radius: 16px;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
  }
  .ai-typing-indicator span {
    width: 8px;
    height: 8px;
    background: #667eea;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out;
  }
  .ai-typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
  .ai-typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
`;

// Inject styles
const styleSheet = document.createElement("style");
styleSheet.innerText = STYLES;
document.head.appendChild(styleSheet);

// --- CHAT STATE ---
let chatHistory = [];
let currentEmailContext = "";

// --- CORE UTILS ---
function getEmailBodyElement(button = null) {
  if (button) {
    let parent = button.parentElement;
    for (let i = 0; i < 10 && parent; i++) {
      const body = parent.querySelector('[aria-label="Message Body"]');
      if (body) return body;
      parent = parent.parentElement;
    }
  }
  const bodies = document.querySelectorAll('[aria-label="Message Body"]');
  for (const body of bodies) {
    if (body.offsetParent !== null) {
      return body;
    }
  }
  return null;
}

function getEmailText(button = null) {
  const el = getEmailBodyElement(button);
  return el ? el.innerText : null;
}

function setEmailText(text, button = null) {
  const el = getEmailBodyElement(button);
  if (el) {
    el.innerText = text;
  }
}

async function rewriteEmail(mode, button = null) {
  const text = getEmailText(button);
  if (!text) {
    alert("No email body text found. Please check if you have text in the visible compose window.");
    return;
  }

  console.log("Rewriting email... Please wait.");

  try {
    const response = await fetch("http://localhost:8000/rewrite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mode: mode,
        text: text
      })
    });

    const data = await response.json();

    if (data.status === "ok") {
      setEmailText(data.result, button);
    } else {
      const msg = data.detail || data.reason || "Unknown error";
      alert("Rewrite failed: " + msg);
    }
  } catch (err) {
    alert("Error connecting to backend: " + err.message + ". Is server.py running?");
  }
}

// --- CHAT SIDEBAR ---
function createChatSidebar() {
  // Remove existing sidebar if any
  const existing = document.getElementById(CHAT_SIDEBAR_ID);
  if (existing) existing.remove();

  const sidebar = document.createElement("div");
  sidebar.id = CHAT_SIDEBAR_ID;
  sidebar.className = "ai-chat-sidebar hidden";

  sidebar.innerHTML = `
    <div class="ai-chat-header">
      <h3>✨ AI Email Assistant</h3>
      <button class="ai-chat-close">×</button>
    </div>
    <div class="ai-chat-messages" id="ai-chat-messages">
      <div class="ai-chat-message assistant">
        👋 Hi! I can help you with your email. I can see what you're writing.
        <br><br>
        Try: "Make this more formal" or "Write an email asking for a meeting tomorrow"
      </div>
    </div>
    <div class="ai-chat-input-area">
      <input type="text" class="ai-chat-input" placeholder="Type your message..." id="ai-chat-input">
      <button class="ai-chat-send" id="ai-chat-send">➤</button>
    </div>
  `;

  document.body.appendChild(sidebar);

  // Event listeners
  sidebar.querySelector(".ai-chat-close").onclick = () => closeChatSidebar();

  const input = sidebar.querySelector("#ai-chat-input");
  const sendBtn = sidebar.querySelector("#ai-chat-send");

  sendBtn.onclick = () => sendChatMessage();
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendChatMessage();
  });

  return sidebar;
}

function openChatSidebar() {
  let sidebar = document.getElementById(CHAT_SIDEBAR_ID);
  if (!sidebar) {
    sidebar = createChatSidebar();
  }

  // Reset chat history on open
  chatHistory = [];

  // Capture current email context
  currentEmailContext = getEmailText() || "";

  // Show sidebar
  setTimeout(() => sidebar.classList.remove("hidden"), 10);

  // Focus input
  setTimeout(() => {
    const input = document.getElementById("ai-chat-input");
    if (input) input.focus();
  }, 300);
}

function closeChatSidebar() {
  const sidebar = document.getElementById(CHAT_SIDEBAR_ID);
  if (sidebar) {
    sidebar.classList.add("hidden");
  }
}

async function sendChatMessage() {
  const input = document.getElementById("ai-chat-input");
  const messagesContainer = document.getElementById("ai-chat-messages");
  const sendBtn = document.getElementById("ai-chat-send");

  const message = input.value.trim();
  if (!message) return;

  // Clear input
  input.value = "";

  // Add user message to UI
  const userMsgEl = document.createElement("div");
  userMsgEl.className = "ai-chat-message user";
  userMsgEl.textContent = message;
  messagesContainer.appendChild(userMsgEl);

  // Add to history
  chatHistory.push({ role: "user", content: message });

  // Show typing indicator
  const typingEl = document.createElement("div");
  typingEl.className = "ai-typing-indicator";
  typingEl.innerHTML = "<span></span><span></span><span></span>";
  messagesContainer.appendChild(typingEl);

  // Scroll to bottom
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Disable send button
  sendBtn.disabled = true;

  try {
    // Refresh email context before sending
    currentEmailContext = getEmailText() || "";

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message,
        email_context: currentEmailContext,
        conversation_history: chatHistory.slice(0, -1) // Exclude current message (already sent)
      })
    });

    const data = await response.json();

    // Remove typing indicator
    typingEl.remove();

    if (data.status === "ok") {
      const aiResponse = data.result;

      // Add to history
      chatHistory.push({ role: "assistant", content: aiResponse });

      // Create AI message element
      const aiMsgEl = document.createElement("div");
      aiMsgEl.className = "ai-chat-message assistant";

      // Check if response looks like an email (has greeting or is multi-line)
      const looksLikeEmail = aiResponse.includes("\n") &&
        (aiResponse.toLowerCase().includes("dear") ||
          aiResponse.toLowerCase().includes("hi ") ||
          aiResponse.toLowerCase().includes("hello") ||
          aiResponse.toLowerCase().includes("regards") ||
          aiResponse.toLowerCase().includes("best,") ||
          aiResponse.toLowerCase().includes("thanks,") ||
          aiResponse.length > 100);

      if (looksLikeEmail) {
        aiMsgEl.innerHTML = `
          <div style="white-space: pre-wrap; margin-bottom: 8px;">${escapeHtml(aiResponse)}</div>
          <button class="apply-btn">📋 Apply to Email</button>
        `;
        aiMsgEl.querySelector(".apply-btn").onclick = () => {
          setEmailText(aiResponse);
          // Show feedback
          const btn = aiMsgEl.querySelector(".apply-btn");
          btn.textContent = "✓ Applied!";
          btn.style.background = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)";
          setTimeout(() => {
            btn.textContent = "📋 Apply to Email";
          }, 2000);
        };
      } else {
        aiMsgEl.innerHTML = `<div style="white-space: pre-wrap;">${escapeHtml(aiResponse)}</div>`;
      }

      messagesContainer.appendChild(aiMsgEl);
    } else {
      const errorMsgEl = document.createElement("div");
      errorMsgEl.className = "ai-chat-message assistant";
      errorMsgEl.textContent = "Sorry, something went wrong. Please try again.";
      messagesContainer.appendChild(errorMsgEl);
    }
  } catch (err) {
    typingEl.remove();
    const errorMsgEl = document.createElement("div");
    errorMsgEl.className = "ai-chat-message assistant";
    errorMsgEl.textContent = "Error: " + err.message + ". Is the server running?";
    messagesContainer.appendChild(errorMsgEl);
  }

  // Re-enable send button
  sendBtn.disabled = false;

  // Scroll to bottom
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Expose to Popup
window.gmailAI = {
  rewriteEmail,
  openChatSidebar
};

// --- INLINE DROPDOWN LOGIC ---
function createButton() {
  const container = document.createElement("div");
  container.className = "ai-dropdown-container";
  container.id = BUTTON_ID;

  const btn = document.createElement("div");
  btn.className = "ai-main-btn";
  btn.innerHTML = `✨ AI Tools ▾`;

  const menu = document.createElement("div");
  menu.className = "ai-dropdown-menu";
  menu.id = DROPDOWN_ID;

  const addItem = (text, mode, isChat = false) => {
    const item = document.createElement("div");
    item.className = "ai-dropdown-item";
    item.innerText = text;
    item.onclick = (e) => {
      e.stopPropagation();
      menu.classList.remove("show");
      if (isChat) {
        openChatSidebar();
      } else {
        rewriteEmail(mode, btn);
      }
    };
    menu.appendChild(item);
  };

  // Add Options
  addItem("✂️ Shorten", "shorten");
  addItem("📝 Elaborate", "elaborate");
  addItem("👔 Professional", "tone:Professional");
  addItem("🤝 Friendly", "tone:Friendly");
  addItem("💜 Sympathetic", "tone:Sympathetic");

  // Add separator
  const separator = document.createElement("div");
  separator.style.cssText = "height: 1px; background: #e0e0e0; margin: 8px 0;";
  menu.appendChild(separator);

  // Add Chat option
  addItem("💬 Chat with AI", "", true);

  // Toggle Menu
  btn.onclick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    document.querySelectorAll('.ai-dropdown-menu').forEach(el => {
      if (el !== menu) el.classList.remove("show");
    });
    menu.classList.toggle("show");
  };

  // Close on click outside
  window.addEventListener('click', (e) => {
    if (!container.contains(e.target)) {
      menu.classList.remove('show');
    }
  });

  container.appendChild(btn);
  container.appendChild(menu);

  return container;
}

function injectButton(toolbar) {
  if (toolbar.querySelector(`#${BUTTON_ID}`)) return;
  toolbar.appendChild(createButton());
}

function findComposeToolbars() {
  return document.querySelectorAll('[aria-label="Formatting options"]');
}

const observer = new MutationObserver(() => {
  const toolbars = findComposeToolbars();
  toolbars.forEach(injectButton);
});

// Start observing
observer.observe(document.body, {
  childList: true,
  subtree: true
});
