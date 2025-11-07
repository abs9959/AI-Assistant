# AI-Assistant

This is a practice repository for a simple AI assistant (Flask + OpenAI).

Quick start:
1. Clone the repo (you already did):
   git clone https://github.com/abs9959/AI-Assistant.git
   cd AI-Assistant

2. Create the files (if not already) and commit them:
   git add .
   git commit -m "chore: initial project files"

3. Push the initial commit to GitHub:
   git push -u origin main

4. Create a Python venv and install:
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt

5. Add .env (DO NOT COMMIT):
   OPENAI_API_KEY=sk-...
   FLASK_SECRET=a_random_secret

6. Run:
   python app.py
   Open http://localhost:5000

Notes:
- Keep .env out of the repo. The provided .gitignore already ignores it.
- If you’re on Windows and want to set environment variables temporarily in Git Bash:
   export OPENAI_API_KEY="sk-..."
   export FLASK_SECRET="a_random_secret"