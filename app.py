
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Yahan apna OpenAI API key daalo
OPENAI_API_KEY = "tumhara-openai-api-key"

def correct_grammar(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # ya "gpt-3.5-turbo"
            messages=[{"role": "user", "content": f"Correct this sentence: {text}"}],
            api_key=OPENAI_API_KEY
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/correct", methods=["POST"])
def correct():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided!"}), 400

    corrected_text = correct_grammar(text)
    return jsonify({"corrected_text": corrected_text})

if __name__ == "__main__":
    app.run(debug=True)
