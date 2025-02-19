import requests

LANGUAGE_TOOL_API = "https://api.languagetool.org/v2/check"

def correct_grammar(text):
    payload = {"text": text, "language": "en-US"}
    
    try:
        # Adding timeout to prevent hanging requests
        response = requests.post(LANGUAGE_TOOL_API, data=payload, timeout=10)
    except requests.exceptions.RequestException:
        return text  # Return original text on network errors
    
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
            
            # Adjust positions based on previous changes
            adjusted_start = start + cumulative_delta
            adjusted_end = adjusted_start + length
            
            # Check if adjusted positions are within bounds
            if adjusted_start > len(corrected_text):
                continue
            if adjusted_end > len(corrected_text):
                adjusted_end = len(corrected_text)
            
            # Apply replacement
            corrected_text[adjusted_start:adjusted_end] = list(replacement)
            
            # Update cumulative delta for length changes
            cumulative_delta += len(replacement) - length
            
        return "".join(corrected_text)
    
    return text  # Fallback for non-200 status codes
