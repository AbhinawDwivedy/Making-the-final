function run(mode) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (!tabs[0].id) return;

        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            func: (m) => {
                if (window.gmailAI) {
                    window.gmailAI.rewriteEmail(m);
                } else {
                    alert("Please refresh the Gmail tab to activate the helper.");
                }
            },
            args: [mode]
        });
    });
}

document.getElementById("shorten").onclick = () => run("shorten");
document.getElementById("elaborate").onclick = () => run("elaborate");
document.getElementById("professional").onclick = () => run("professional");
