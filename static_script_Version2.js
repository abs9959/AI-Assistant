async function appendMessage(role, text) {
  const container = document.getElementById("messages");
  const el = document.createElement("div");
  el.className = "msg " + (role === "user" ? "user" : "assistant");
  el.textContent = (role === "user" ? "You: " : "Assistant: ") + text;
  container.appendChild(el);
  container.scrollTop = container.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("input");
  const message = input.value.trim();
  if (!message) return;
  appendMessage("user", message);
  input.value = "";
  document.getElementById("send").disabled = true;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    if (data.error) {
      appendMessage("assistant", "Error: " + data.error);
    } else {
      appendMessage("assistant", data.reply);
    }
  } catch (err) {
    appendMessage("assistant", "Network error: " + err.message);
  } finally {
    document.getElementById("send").disabled = false;
  }
}

async function resetConversation() {
  await fetch("/reset", { method: "POST" });
  document.getElementById("messages").innerHTML = "";
  appendMessage("assistant", "Conversation reset. Say hi!");
}

document.getElementById("send").addEventListener("click", sendMessage);
document.getElementById("input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});
document.getElementById("reset").addEventListener("click", resetConversation);

// starter message
appendMessage("assistant", "Hi — I'm your practice assistant. Ask me anything!");