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

def translate_with_llama3(name, segment, from_language, to_language, context=None,selected_model=''):
    try:
        model_id = f"meta-llama/{selected_model}"
        pipeline = transformers.pipeline(
        "text-generation", 
        model=model_id, 
        model_kwargs={"torch_dtype": torch.bfloat16}, 
        device_map="auto"
        )
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