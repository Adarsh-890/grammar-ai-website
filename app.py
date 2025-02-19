def correct_grammar(text):
    payload = {"text": text, "language": "en-US"}
    response = requests.post(LANGUAGE_TOOL_API, data=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        # Agar koi error nahi mila toh original text return karein
        if not result.get("matches"):
            return text
        
        corrected_text = text
        for match in result["matches"]:
            if "replacements" in match and match["replacements"]:
                # Replace incorrect word with the first suggested correction
                incorrect_word = match["context"]["text"]
                replacement = match["replacements"][0]["value"]
                corrected_text = corrected_text.replace(incorrect_word, replacement, 1)
        
        return corrected_text

    return text  # API fail ho jaye toh original text return kare
