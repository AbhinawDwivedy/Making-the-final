const BUTTON_ID = "ai-rewrite-btn";
const DROPDOWN_ID = "ai-rewrite-dropdown";
const CHAT_SIDEBAR_ID = "ai-chat-sidebar";
const AGENTIC_MODAL_ID = "ai-agentic-modal";

// --- AGENTIC MODE STATE ---
let isAgenticMode = localStorage.getItem('agenticMode') === 'true';

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
    min-width: 200px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 10000;
    border-radius: 8px;
    padding: 8px 0;
    margin-bottom: 5px;
  }
  .ai-dropdown-item {
    color: #3c4043;
    padding: 10px 16px;
    text-decoration: none;
    display: block;
    cursor: pointer;
    font-family: Roboto,sans-serif;
    font-size: 13px;
    transition: background 0.15s;
  }
  .ai-dropdown-item:hover {
    background-color: #f1f3f4;
  }
  .show {display:block;}

  /* ========================================
     AGENTIC MODE TOGGLE - Premium Design
     ======================================== */
  .ai-mode-toggle-container {
    padding: 12px 16px;
    border-bottom: 1px solid #e8e8e8;
    margin-bottom: 8px;
  }
  .ai-mode-toggle {
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    padding: 8px 12px;
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
    border: 1px solid rgba(102, 126, 234, 0.2);
    transition: all 0.3s ease;
  }
  .ai-mode-toggle:hover {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
    border-color: rgba(102, 126, 234, 0.4);
  }
  .ai-mode-toggle.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: transparent;
  }
  .ai-mode-toggle.active .ai-mode-label {
    color: white;
  }
  .ai-mode-toggle.active .ai-mode-desc {
    color: rgba(255,255,255,0.8);
  }
  .ai-mode-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .ai-mode-label {
    font-size: 13px;
    font-weight: 600;
    color: #3c4043;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .ai-mode-desc {
    font-size: 11px;
    color: #5f6368;
  }
  .ai-toggle-switch {
    width: 36px;
    height: 20px;
    background: #dadce0;
    border-radius: 10px;
    position: relative;
    transition: background 0.3s;
  }
  .ai-toggle-switch::after {
    content: '';
    position: absolute;
    width: 16px;
    height: 16px;
    background: white;
    border-radius: 50%;
    top: 2px;
    left: 2px;
    transition: transform 0.3s;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  }
  .ai-mode-toggle.active .ai-toggle-switch {
    background: rgba(255,255,255,0.3);
  }
  .ai-mode-toggle.active .ai-toggle-switch::after {
    transform: translateX(16px);
    background: white;
  }
  
  /* Pulse animation for active agentic mode */
  @keyframes agenticPulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }
    50% { box-shadow: 0 0 0 4px rgba(102, 126, 234, 0); }
  }
  .ai-mode-toggle.active {
    animation: agenticPulse 2s infinite;
  }

  /* ========================================
     AGENTIC PROGRESS MODAL
     ======================================== */
  .ai-agentic-modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 16px;
    padding: 24px;
    z-index: 100001;
    min-width: 320px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    font-family: 'Google Sans', Roboto, sans-serif;
    animation: modalFadeIn 0.3s ease;
  }
  @keyframes modalFadeIn {
    from { opacity: 0; transform: translate(-50%, -50%) scale(0.95); }
    to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  }
  .ai-agentic-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    z-index: 100000;
    backdrop-filter: blur(4px);
  }
  .ai-modal-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    color: white;
  }
  .ai-modal-header h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 500;
  }
  .ai-modal-brain {
    font-size: 24px;
    animation: brainPulse 1.5s infinite;
  }
  @keyframes brainPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
  }
  .ai-modal-progress {
    margin-bottom: 16px;
  }
  .ai-progress-bar {
    height: 6px;
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 8px;
  }
  .ai-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
    background-size: 200% 100%;
    animation: progressShimmer 1.5s infinite linear;
    border-radius: 3px;
    transition: width 0.3s ease;
  }
  @keyframes progressShimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
  .ai-progress-text {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: rgba(255,255,255,0.7);
  }
  .ai-modal-status {
    font-size: 14px;
    color: #e0e0e0;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .ai-status-icon {
    animation: spin 1s infinite linear;
  }
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  .ai-modal-log {
    background: rgba(0,0,0,0.3);
    border-radius: 8px;
    padding: 12px;
    max-height: 120px;
    overflow-y: auto;
    font-size: 11px;
    font-family: monospace;
    color: rgba(255,255,255,0.6);
  }
  .ai-log-entry {
    margin-bottom: 6px;
    display: flex;
    gap: 8px;
  }

  /* ========================================
     SUCCESS SCORE BADGE
     ======================================== */
  .ai-score-badge {
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    font-family: 'Google Sans', Roboto, sans-serif;
    z-index: 100002;
    box-shadow: 0 8px 24px rgba(17, 153, 142, 0.4);
    animation: badgeSlideIn 0.4s ease, badgeFadeOut 0.4s ease 3s forwards;
    cursor: pointer;
  }
  @keyframes badgeSlideIn {
    from { opacity: 0; transform: translateX(50px); }
    to { opacity: 1; transform: translateX(0); }
  }
  @keyframes badgeFadeOut {
    to { opacity: 0; transform: translateX(50px); }
  }
  .ai-score-main {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 4px;
  }
  .ai-score-details {
    font-size: 11px;
    opacity: 0.9;
  }

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

// --- AGENTIC MODE FUNCTIONS ---
function showAgenticModal() {
  // Remove existing modal
  const existing = document.getElementById(AGENTIC_MODAL_ID);
  if (existing) existing.remove();

  const overlay = document.createElement("div");
  overlay.className = "ai-agentic-modal-overlay";
  overlay.id = AGENTIC_MODAL_ID + "-overlay";

  const modal = document.createElement("div");
  modal.className = "ai-agentic-modal";
  modal.id = AGENTIC_MODAL_ID;

  modal.innerHTML = `
    <div class="ai-modal-header">
      <span class="ai-modal-brain">🧠</span>
      <h3>Agentic Refinement</h3>
    </div>
    <div class="ai-modal-progress">
      <div class="ai-progress-bar">
        <div class="ai-progress-fill" id="ai-progress-fill" style="width: 33%"></div>
      </div>
      <div class="ai-progress-text">
        <span id="ai-attempt-text">Attempt 1/3</span>
        <span id="ai-score-text">--</span>
      </div>
    </div>
    <div class="ai-modal-status">
      <span class="ai-status-icon">⚙️</span>
      <span id="ai-status-message">Generating initial draft...</span>
    </div>
    <div class="ai-modal-log" id="ai-modal-log">
      <div class="ai-log-entry">🚀 Starting agentic refinement...</div>
    </div>
  `;

  document.body.appendChild(overlay);
  document.body.appendChild(modal);
}

function updateAgenticModal(attempt, maxAttempts, status, score = null) {
  const progressFill = document.getElementById("ai-progress-fill");
  const attemptText = document.getElementById("ai-attempt-text");
  const scoreText = document.getElementById("ai-score-text");
  const statusMessage = document.getElementById("ai-status-message");
  const log = document.getElementById("ai-modal-log");

  if (progressFill) {
    progressFill.style.width = `${(attempt / maxAttempts) * 100}%`;
  }
  if (attemptText) {
    attemptText.textContent = `Attempt ${attempt}/${maxAttempts}`;
  }
  if (scoreText && score !== null) {
    scoreText.textContent = `Score: ${score}/5.0`;
  }
  if (statusMessage) {
    statusMessage.textContent = status;
  }
  if (log) {
    const entry = document.createElement("div");
    entry.className = "ai-log-entry";
    entry.textContent = `${new Date().toLocaleTimeString()} - ${status}`;
    log.appendChild(entry);
    log.scrollTop = log.scrollHeight;
  }
}

function hideAgenticModal() {
  const modal = document.getElementById(AGENTIC_MODAL_ID);
  const overlay = document.getElementById(AGENTIC_MODAL_ID + "-overlay");
  if (modal) modal.remove();
  if (overlay) overlay.remove();
}

function showScoreBadge(scores, goalAchieved) {
  const existing = document.querySelector(".ai-score-badge");
  if (existing) existing.remove();

  const badge = document.createElement("div");
  badge.className = "ai-score-badge";

  const overall = scores.overall?.score || 0;
  const emoji = goalAchieved ? "✨" : "📊";

  badge.innerHTML = `
    <div class="ai-score-main">${emoji} Quality: ${overall}/5.0</div>
    <div class="ai-score-details">
      Faith: ${scores.faithfulness?.score || 0} | 
      Complete: ${scores.completeness?.score || 0} | 
      Robust: ${scores.robustness?.score || 0}
    </div>
  `;

  badge.onclick = () => badge.remove();
  document.body.appendChild(badge);

  // Auto-remove after 4 seconds
  setTimeout(() => badge.remove(), 4000);
}

// --- REWRITE EMAIL ---
async function rewriteEmail(mode, button = null) {
  const text = getEmailText(button);
  if (!text) {
    alert("No email body text found. Please check if you have text in the visible compose window.");
    return;
  }

  // Check if agentic mode is enabled
  const useAgentic = localStorage.getItem('agenticMode') === 'true';

  if (useAgentic) {
    await rewriteEmailAgentic(mode, text, button);
  } else {
    await rewriteEmailNormal(mode, text, button);
  }
}

async function rewriteEmailNormal(mode, text, button) {
  console.log("Normal mode: Rewriting email...");

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

async function rewriteEmailAgentic(mode, text, button) {
  console.log("🧠 Agentic mode: Starting iterative refinement...");

  // Show progress modal
  showAgenticModal();
  updateAgenticModal(1, 3, "Generating initial draft...");

  try {
    const response = await fetch("http://localhost:8000/rewrite-agentic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mode: mode,
        text: text,
        target_score: 4.5,
        max_attempts: 3
      })
    });

    const data = await response.json();

    if (data.status === "ok") {
      // Process agent log for UI updates
      const agenticInfo = data.agentic_info;

      if (agenticInfo && agenticInfo.agent_log) {
        for (const entry of agenticInfo.agent_log) {
          if (entry.type === "attempt_start") {
            updateAgenticModal(entry.attempt, 3, entry.message);
          } else if (entry.type === "evaluation") {
            const score = entry.scores?.overall?.score || 0;
            updateAgenticModal(entry.attempt, 3, `Evaluating... Score: ${score}/5`, score);
          }
        }
      }

      // Small delay to show final state
      await new Promise(r => setTimeout(r, 500));

      // Hide modal and show result
      hideAgenticModal();
      setEmailText(data.result, button);

      // Show score badge
      if (agenticInfo && agenticInfo.final_scores) {
        showScoreBadge(agenticInfo.final_scores, agenticInfo.goal_achieved);
      }

      // Log details to console
      console.log("🧠 Agentic Result:", {
        goalAchieved: agenticInfo?.goal_achieved,
        attemptsUsed: agenticInfo?.attempts_used,
        finalScores: agenticInfo?.final_scores
      });

    } else {
      hideAgenticModal();
      const msg = data.detail || data.reason || "Unknown error";
      alert("Agentic rewrite failed: " + msg);
    }
  } catch (err) {
    hideAgenticModal();
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

      // Check if user asked to modify/edit content (shorten, lengthen, rewrite, etc.)
      const userAskedToModify = message.toLowerCase().match(
        /\b(shorten|shorter|make|change|edit|rewrite|reword|rephrase|modify|update|fix|improve|lengthen|longer|elaborate|formal|informal|professional|friendly|paragraph|para|sentence|line)\b/
      );

      // Show Apply button if it's a full email OR user asked to modify something and got substantial response
      const shouldShowApply = looksLikeEmail || (userAskedToModify && aiResponse.length > 20);

      if (shouldShowApply) {
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

  // Update button text based on mode
  const updateButtonText = () => {
    const isAgentic = localStorage.getItem('agenticMode') === 'true';
    btn.innerHTML = isAgentic ? `🧠 AI Tools ▾` : `✨ AI Tools ▾`;
  };
  updateButtonText();

  const menu = document.createElement("div");
  menu.className = "ai-dropdown-menu";
  menu.id = DROPDOWN_ID;

  // --- AGENTIC MODE TOGGLE ---
  const toggleContainer = document.createElement("div");
  toggleContainer.className = "ai-mode-toggle-container";

  const toggle = document.createElement("div");
  toggle.className = "ai-mode-toggle" + (localStorage.getItem('agenticMode') === 'true' ? " active" : "");
  toggle.innerHTML = `
    <div class="ai-mode-info">
      <div class="ai-mode-label">
        <span>🧠</span>
        <span>Agentic Mode</span>
      </div>
      <div class="ai-mode-desc">Iterative refinement with self-evaluation</div>
    </div>
    <div class="ai-toggle-switch"></div>
  `;

  toggle.onclick = (e) => {
    e.stopPropagation();
    const isActive = toggle.classList.contains("active");

    if (isActive) {
      toggle.classList.remove("active");
      localStorage.setItem('agenticMode', 'false');
    } else {
      toggle.classList.add("active");
      localStorage.setItem('agenticMode', 'true');
    }

    updateButtonText();
    console.log("Agentic Mode:", !isActive ? "ON" : "OFF");
  };

  toggleContainer.appendChild(toggle);
  menu.appendChild(toggleContainer);

  // --- DROPDOWN ITEMS ---
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
