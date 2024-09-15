import os
import requests
import re

def translate_with_custom(name, segment, from_language, to_language, relevant_context=None,selected_model=''):
    # Fetch custom API details from environment variables or request
    CUSTOM_API_URL = os.getenv("CUSTOM_API_URL")
    CUSTOM_API_KEY = os.getenv("CUSTOM_API_KEY")  # If required

    if not CUSTOM_API_URL:
        return "// Custom API URL not configured."
    prompt = f"""
        You are a code translator. Translate the following {from_language} code into {to_language}.
        Consider the following context: {relevant_context}
        Ensure the {to_language} code is correctly formatted and enclosed in triple backticks.

        ```{from_language}
        {segment}
        ```

        Please provide the {to_language} output:
        """

    try:
        headers = {}
        if CUSTOM_API_KEY:
            headers['Authorization'] = f"Bearer {CUSTOM_API_KEY}"
        
        payload = {
            from_language: segment,
            "target_language": to_language
        }

        response = requests.post(CUSTOM_API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('translated_code', '// No translated code returned.')
        else:
            return f"// Custom API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"// Custom Translation Error: {str(e)}"
 

def extract_code_block(text, language):
    pattern = rf"```{language}\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None