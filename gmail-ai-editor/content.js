const BUTTON_ID = "ai-rewrite-btn";
const DROPDOWN_ID = "ai-rewrite-dropdown";

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
    bottom: 100%; /* Show ABOVE the button */
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
`;

// Inject styles
const styleSheet = document.createElement("style");
styleSheet.innerText = STYLES;
document.head.appendChild(styleSheet);

// --- CORE UTILS ---


function getEmailBodyElement(button = null) {
  // 1. If button is clicked, search somewhat locally (in the same compose window)
  if (button) {
    let parent = button.parentElement;
    // Traverse up max 10 levels to find a common container
    for (let i = 0; i < 10 && parent; i++) {
      const body = parent.querySelector('[aria-label="Message Body"]');
      if (body) return body;
      parent = parent.parentElement;
    }
  }

  // 2. Fallback: Find the first *visible* message body
  const bodies = document.querySelectorAll('[aria-label="Message Body"]');
  for (const body of bodies) {
    // offsetParent is a good check for visibility (it's null if hidden)
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

  // Show loading state (simple alert for MVP, or console log)
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
      setEmailText(data.result, button); // Pass button context
    } else {
      // FastAPI returns 'detail', our custom errors might return 'reason'
      const msg = data.detail || data.reason || "Unknown error";
      alert("Rewrite failed: " + msg);
    }
  } catch (err) {
    alert("Error connecting to backend: " + err.message + ". Is server.py running?");
  }
}

// Expose to Popup
window.gmailAI = {
  rewriteEmail
};


// --- INLINE BUTTON LOGIC ---

// --- INLINE DROPDOWN LOGIC ---

function createButton() {
  const container = document.createElement("div");
  container.className = "ai-dropdown-container";
  container.id = BUTTON_ID; // Use same ID key to prevent dupes

  // 1. Main Toggle Button
  const btn = document.createElement("div");
  btn.className = "ai-main-btn";
  btn.innerHTML = `✨ AI Tools ▾`;

  // 2. Dropdown Menu
  const menu = document.createElement("div");
  menu.className = "ai-dropdown-menu";
  menu.id = DROPDOWN_ID;

  // Helper to create items
  const addItem = (text, mode) => {
    const item = document.createElement("div");
    item.className = "ai-dropdown-item";
    item.innerText = text;
    item.onclick = (e) => {
      e.stopPropagation();
      menu.classList.remove("show"); // Close menu
      rewriteEmail(mode, btn); // Pass btn as context
    };
    menu.appendChild(item);
  };

  // Add Options
  addItem("✂️ Shorten", "shorten");
  addItem("📝 Elaborate", "elaborate");
  addItem("👔 Professional", "tone:Professional");
  addItem("🤝 Friendly", "tone:Friendly");
  addItem("💜 Sympathetic", "tone:Sympathetic");

  // Toggle Menu
  btn.onclick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    // Close others
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
