import ollama
import re

def translate_with_ollama(name, segment, from_language, to_language, relevant_context):
    try:
        # Send the request to the Ollama API using the llama3.1 model
        prompt = f"""
        You are a code translator. Translate the following {from_language} code into {to_language}.
        Consider the following context: {relevant_context}
        Ensure the {to_language} code is correctly formatted and enclosed in triple backticks.

        ```{from_language}
        {segment}
        ```

        Please provide the {to_language} output:
        """
        response = ollama.chat(
            model='llama3.1',
            messages=[
                    {"role": "system", "content": f"You are a code translator. Translate this segment of {from_language} code into {to_language}. Segment: {name}. Do not provide any explanations just provide the code."},
                    {"role": "user", "content": prompt}
                ],
        )

        # Print the entire response for debugging purposes
        print(f"Full response from Ollama: {response}")

        # Extract the content from the response
        if response and 'message' in response:
            content = response['message']['content']
            java_code = extract_code_block(content, to_language)
            return java_code or "// Translation failed."
        else:
            return "// No response from Ollama."

    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {str(e)}")
        return f"// Error: {str(e)}"

def extract_code_block(text, language):
    # Regular expression to extract the code block in the specified language
    pattern = rf"```{language}\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
