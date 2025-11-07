import os
from flask import Flask, render_template, request, session, jsonify
import openai

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("FLASK_SECRET", "change-me-for-prod")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set the OPENAI_API_KEY environment variable.")
openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = (
    "You are a helpful assistant for practice projects. Keep replies concise and friendly."
)

@app.route("/")
def index():
    # Initialize simple memory
    if "history" not in session:
        session["history"] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # load history from session (list of dicts: {"role": "user"/"assistant", "content": "..."})
    history = session.get("history", [])
    # Append the new user message
    history.append({"role": "user", "content": user_message})

    # Build messages including system prompt and recent history (limit to last N turns)
    max_turns = 6  # keep short for cheaper calls
    recent = history[-(max_turns * 2):]  # each turn has user+assistant
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + recent

    # Call OpenAI Chat Completions
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=256,
            temperature=0.7,
        )
        assistant_text = resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

    # Save assistant reply to history
    history.append({"role": "assistant", "content": assistant_text})
    session["history"] = history

    return jsonify({"reply": assistant_text, "history": history})

@app.route("/reset", methods=["POST"])
def reset():
    session.pop("history", None)
    return jsonify({"ok": True})

if __name__ == "__main__":
    # For local development only. Use a proper WSGI server in prod.
    app.run(host="0.0.0.0", port=5000, debug=True)
