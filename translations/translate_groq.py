from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
import re

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def translate_with_groq(name, segment, from_language, to_language, relevant_context):
    # Placeholder for Groq API integration
    # Replace with actual Groq API calls
    try:
        prompt = f"""
        You are a code translator. Translate the following {from_language} code into {to_language}.
        Consider the following context: {relevant_context}
        Ensure the {to_language} code is correctly formatted and enclosed in triple backticks.

        ```{from_language}
        {segment}
        ```

        Please provide the {to_language} output:
        """
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                    {"role": "system", "content": f"You are a code translator. Translate this segment of {from_language} code into {to_language}. Segment: {name}. Do not provide any explanations just provide the code."},
                    {"role": "user", "content": prompt}
                ],
            temperature=0.1,
            max_tokens=2000,
            top_p=1
        )
        if response.choices:
            content = response.choices[0].message.content.strip()
            java_code = extract_code_block(content, to_language)
            return java_code or "// Translation failed."
        
        else:
            return "// No response from OpenAI."
        
    except Exception as e:
        return f"// Error: {str(e)}"

def extract_code_block(text, language):
    pattern = rf"```{language}\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None