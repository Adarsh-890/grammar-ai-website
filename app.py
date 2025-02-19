from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# API URLs
LANGUAGE_TOOL_API = "https://api.languagetool.org/v2/check"
OPENAI_API_URL = "https://api.openai.com/v1/completions"

# Securely Fetch API Key from Render
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def correct_grammar(text):
    payload = {"text": text, "language": "en-US"}
    response = requests.post(LANGUAGE_TOOL_API, data=payload)
    if response.status_code == 200:
        matches = response.json().get("matches", [])
        corrected_text = text
        for match in matches:
            if "replacements" in match and match["replacements"]:
                corrected_text = corrected_text.replace(match["context"]["text"], match["replacements"][0]["value"])
        return corrected_text
    return None

def make_chat_human_friendly(text):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "text-davinci-003", "prompt": f"Make this text human-friendly: {text}", "max_tokens": 100}
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    grammar_result = None
    human_friendly_text = None

    if request.method == "POST":
        user_input = request.form["text"]
        grammar_result = correct_grammar(user_input)
        if not grammar_result:  # If grammar correction fails, fallback to human-friendly conversion
            grammar_result = make_chat_human_friendly(user_input)

    return render_template("index.html", grammar_result=grammar_result)

if __name__ == "__main__":
    app.run(debug=True)
