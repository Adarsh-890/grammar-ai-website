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
        result = response.json()
        corrected_text = text
        for match in result.get("matches", []):
            if "replacements" in match and match["replacements"]:
                corrected_text = corrected_text.replace(match["context"]["text"], match["replacements"][0]["value"])
        return corrected_text
    return text  # Agar correction nahi mile toh same text return kare

def make_chat_human_friendly(text):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "text-davinci-003",
        "prompt": f"Make this text human-friendly and correct grammar: {text}",
        "max_tokens": 100
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", text).strip()
    
    return text  # Agar AI fail ho jaye toh original text return kare

@app.route("/", methods=["GET", "POST"])
def index():
    corrected_text = ""
    human_friendly_text = ""

    if request.method == "POST":
        user_input = request.form["text"]
        corrected_text = correct_grammar(user_input)
        human_friendly_text = make_chat_human_friendly(corrected_text)

    return render_template("index.html", input_text=user_input, corrected_text=corrected_text, human_friendly_text=human_friendly_text)

if __name__ == "__main__":
    app.run(debug=True)
