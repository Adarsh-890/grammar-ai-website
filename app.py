import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API URLs
LANGUAGE_TOOL_API = "https://api.languagetool.org/v2/check"
OPENAI_API_URL = "https://api.openai.com/v1/completions"

# Securely fetching API Key from Render environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def correct_grammar(text):
    payload = {"text": text, "language": "en-US"}
    response = requests.post(LANGUAGE_TOOL_API, data=payload)
    return response.json() if response.status_code == 200 else None

def make_chat_human_friendly(text):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "text-davinci-003", "prompt": f"Make this text human-friendly: {text}", "max_tokens": 100}
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    return response.json()["choices"][0]["text"].strip() if response.status_code == 200 else None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["text"]
        grammar_result = correct_grammar(user_input)
        human_friendly_text = make_chat_human_friendly(user_input)
        return render_template("index.html", grammar_result=grammar_result, human_friendly_text=human_friendly_text)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
