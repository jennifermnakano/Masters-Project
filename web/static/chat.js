async function sendMessage() {
    const studentId = document.getElementById("studentId").value.trim();
    const message = document.getElementById("userMessage").value.trim();
    if (!message || !studentId) return;

    const chatBox = document.getElementById("chatBox");
    const loadingIndicator = document.getElementById("loading");

    // Show user message immediately
    chatBox.innerHTML += `<p class="user-msg">${message}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Clear input
    document.getElementById("userMessage").value = '';

    // Show loading
    loadingIndicator.style.display = "block";

    try {
        // Send request
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: `student_id=${studentId}&message=${encodeURIComponent(message)}`
        });

        if (!response.ok) throw new Error("Network response not ok");

        const data = await response.json();

        // Format bot message using simple Markdown replacement
        let botMsg = data.response
            .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")   // bold
            .replace(/^- /gm, "• ")                     // bullets
            .replace(/\n/g, "<br>");                    // newlines

        chatBox.innerHTML += `<p class="bot-msg">${botMsg}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (err) {
        chatBox.innerHTML += `<p class="bot-msg">Error: ${err.message}</p>`;
    } finally {
        loadingIndicator.style.display = "none";
    }
}
