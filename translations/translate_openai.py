import os
import re
import openai
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
# Initialize the OpenAI client with your API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
def translate_with_openai(name, segment, from_language, to_language,context=None):
    try:
        # Prepare the translation prompt with relevant context
        if context:
            # If context is provided, include it in the prompt
            prompt = f"""
            You are a code translator. Translate the following {from_language} code into {to_language}.
            Use the provided context to ensure accurate translation. Ensure the {to_language} code is correctly formatted and enclosed in triple backticks.

            Context:
            ```{from_language}
            {context}
            ```

            Now translate the following {from_language} code:

            ```{from_language}
            {segment}
            ```

            Please provide the {to_language} output:
            """
        else:
            # If no context is provided, use a simpler prompt
            prompt = f"""
            You are a code translator. Translate the following {from_language} code into {to_language}.
            Ensure the {to_language} code is correctly formatted and enclosed in triple backticks.

            ```{from_language}
            {segment}
            ```

            Please provide the {to_language} output:
            """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a code translator. Translate this {from_language} code to {to_language}."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000,
            top_p=1
        )
        
        if response.choices:
            content = response.choices[0].message.content.strip()
            translated_code = extract_code_block(content, to_language)
            return translated_code or "// Translation failed."
        else: return "// No response from OpenAI."
    except Exception as e:
        return f"// Error: {str(e)}"



def extract_code_block(text, language):
    pattern = rf"```{language}\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
