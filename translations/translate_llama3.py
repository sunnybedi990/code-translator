import transformers
import torch
import re

# Set up the Llama3 model pipeline
model_id = "meta-llama/Meta-Llama-3-8B"

pipeline = transformers.pipeline(
    "text-generation", 
    model=model_id, 
    model_kwargs={"torch_dtype": torch.bfloat16}, 
    device_map="auto"
)

def translate_with_llama3(name, segment, from_language, to_language, relevant_context):
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
        response = pipeline(prompt)
        
        if response:
            content = response[0]['generated_text']
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