from flask import Flask, render_template, request
import requests

app = Flask(__name__)

LANGUAGE_TOOL_API = "https://api.languagetool.org/v2/check"

def correct_grammar(text):
    payload = {"text": text, "language": "en-US"}
    
    try:
        response = requests.post(LANGUAGE_TOOL_API, data=payload, timeout=10)
    except requests.exceptions.RequestException:
        return text  # Network error par original text return kare
    
    if response.status_code == 200:
        result = response.json()
        
        if not result.get("matches"):
            return text
        
        corrected_text = list(text)
        cumulative_delta = 0
        
        # Process matches from earliest to latest after sorting
        for match in sorted(result["matches"], key=lambda x: x["offset"]):
            if not match.get("replacements"):
                continue
            
            start = match["offset"]
            length = match["length"]
            replacement = match["replacements"][0]["value"]
            
            adjusted_start = start + cumulative_delta
            adjusted_end = adjusted_start + length
            
            if adjusted_start > len(corrected_text):
                continue
            if adjusted_end > len(corrected_text):
                adjusted_end = len(corrected_text)
            
            corrected_text[adjusted_start:adjusted_end] = list(replacement)
            cumulative_delta += len(replacement) - length
            
        return "".join(corrected_text)
    
    return text  # Fallback for non-200 status codes

@app.route("/", methods=["GET", "POST"])
def home():
    corrected_text = ""
    
    if request.method == "POST":
        user_input = request.form["text"]
        corrected_text = correct_grammar(user_input)
    
    return render_template("index.html", corrected_text=corrected_text)

if __name__ == '__main__':
    app.run(debug=True)
