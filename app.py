import requests

LANGUAGE_TOOL_API = "https://api.languagetool.org/v2/check"

def correct_grammar(text):
    payload = {"text": text, "language": "en-US"}
    response = requests.post(LANGUAGE_TOOL_API, data=payload)

    if response.status_code == 200:
        result = response.json()
        
        # Agar koi grammar mistake nahi hai toh original text return karein
        if not result.get("matches"):
            return text

        corrected_text = list(text)  # Text ko list banayein taaki indexing se replace kar sakein
        for match in result["matches"]:
            if "replacements" in match and match["replacements"]:
                start = match["offset"]
                end = start + match["length"]
                replacement = match["replacements"][0]["value"]

                # Replace incorrect word
                corrected_text[start:end] = replacement

        return "".join(corrected_text)  # List ko wapas string me convert karein

    return text  # Agar API fail ho jaye toh original text return karein
