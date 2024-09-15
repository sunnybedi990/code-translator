from flask import Flask, request, jsonify, stream_with_context, Response
from flask_cors import CORS
# Set your OpenAI API key
from dotenv import load_dotenv
from openai import OpenAI
import os
import re
from translations import get_translator
from segments import get_segments, extract_code_skeleton  # Import the get_segments function
import tiktoken  # Library to count tokens
import subprocess
import traceback


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
MAX_TOKEN_LIMIT = 120000  # Define your token limit here
OPEN_AI_MAX_TOKEN_LIMIT = 128000
LLAMA3_MAX_TOKEN_LIMIT = 128000


# Function to map frontend model names to CLI model names
def map_model_name(model_name):
    model_mapping = {
        "Llama 3.1 - 8B": "llama3.1:8b",
        "Llama 3.1 - 70B": "llama3.1:70b",
        "Gemma 2 - 2B": "gemma2:2b",
        "Gemma 2 - 9B": "gemma2:9b",
        "Mistral-Nemo - 12B": "mistral-nemo:12b",
        "Mistral Large 2 - 123B": "mistral-large2:123b",
        "Qwen 2 - 0.5B": "qwen2:0.5b",
        "Qwen 2 - 72B": "qwen2:72b",
        "DeepSeek-Coder V2 - 16B": "deepseek-coder-v2:16b",
        "Phi-3 - 3B": "phi3:3b",
        "Phi-3 - 14B": "phi3:14b",
        # Add any other models you might need
    }
    return model_mapping.get(model_name, model_name)  # Default to input if not found


# Function to check if a model is installed
def is_model_installed(model_name):
    try:
        # Use subprocess to call 'ollama list' command
        result = subprocess.run(['/usr/local/bin/ollama', 'list'], stdout=subprocess.PIPE, text=True)
        installed_models = result.stdout.splitlines()
        
               
        # Check if the model's CLI name is in the installed models list
        cli_model_name = map_model_name(model_name)
        
        for installed_model in installed_models:
            if cli_model_name in installed_model:
                return True
        return False
    except Exception as e:
        print(f"Error checking model: {e}")
        print(traceback.format_exc())

        return False


import subprocess
from flask import jsonify, request
import time

# Store subprocess processes to manage cancellation
processes = {}

def pull_model(model_name):
    # Map the model name (add actual mapping logic)
    cli_model_name = map_model_name(model_name)

    # Simulating subprocess call and streaming its output
    process = subprocess.Popen(
        ['ollama', 'pull', cli_model_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # Line-buffered output
    )

    for line in iter(process.stdout.readline, ''):
        time.sleep(0.1)  # Simulate delay for demonstration purposes
        yield line  # Yield each line of progress

    # When done
    yield 'Model pull completed.'


# Route to cancel a model pull
@app.route('/api/cancel-pull', methods=['POST'])
def cancel_model_pull():
    data = request.get_json()
    model = data.get('model')
    
    cli_model_name = map_model_name(model)
    process = processes.get(cli_model_name)
    
    if process:
        process.terminate()  # Terminate the process
        processes.pop(cli_model_name, None)  # Remove from tracking
        return jsonify({'success': True, 'message': f'Pull for {model} canceled.'})
    
    return jsonify({'success': False, 'message': f'No pull process found for {model}.'}), 404



# Route to check if the model is installed
@app.route('/api/check-model', methods=['GET'])
def check_model():
    model = request.args.get('model')
    if not model:
        return jsonify({'error': 'Model name is required'}), 400

    if is_model_installed(model):
        return jsonify({'installed': True})
    else:
        return jsonify({'installed': False})

# Route to pull a model
@app.route('/api/pull-model', methods=['POST'])
def pull_model_route():
    data = request.get_json()
    model = data.get('model')
    if not model:
        return jsonify({'error': 'Model name is required'}), 400

    return Response(stream_with_context(pull_model(model)), mimetype='text/plain')



# Method 1 Sliding Window
def sliding_window_translate(source_code: str, from_language: str, to_language: str, translator_func,selected_model, window_size: int = 1500, overlap_size: int = 500):
    """
    Translates a large codebase using a sliding window approach for better context management.
    
    Args:
        source_code (str): The original source code to translate.
        from_language (str): The source programming language.
        to_language (str): The target programming language.
        translator_func: The function to call the selected translator API.
        window_size (int): The number of tokens to include in each window.
        overlap_size (int): The number of tokens to overlap between consecutive windows.

    Returns:
        str: The fully translated code.
    """
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(source_code)
    
    translated_code = ""
    start_idx = 0
    total_tokens = len(tokens)
    
    while start_idx < total_tokens:
        end_idx = min(start_idx + window_size, total_tokens)  # Define window bounds
        
        # Extract the window's code, including the overlapping context
        window_tokens = tokens[start_idx:end_idx]
        window_code = enc.decode(window_tokens)
        
        # Translate the current window
        translated_window = translator_func("Code Window", window_code, from_language, to_language,selected_model=selected_model)
        translated_code += translated_window + "\n"
        
        # Slide the window by moving the start index forward
        start_idx += (window_size - overlap_size)
    
    return translated_code.strip()

# Method 2 Segmentation of Code
def translate_code(source_code,from_language,to_language,translator,selected_model):
     # Tokenize the source code to estimate token count
        enc = tiktoken.get_encoding("cl100k_base")  # Choose the encoding based on the model you're using
        tokenized_code = enc.encode(source_code)
        token_length = len(tokenized_code)
        translated_code = ""

        if token_length <= MAX_TOKEN_LIMIT:
            # If the token length is below the limit, translate the full code
            skeleton = extract_code_skeleton(source_code, from_language)
            translated_code = translator('Full Code', source_code, from_language, to_language, skeleton,selected_model)
        else:
            # If the token length exceeds the limit, segment the code
            try:
                segments, class_methods = get_segments(source_code, from_language)
                skeleton = extract_code_skeleton(source_code, from_language)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            accumulated_context = skeleton  # Use the skeleton as the initial context

            # Function to translate a segment with essential context
            def translate_segment(name, segment, context):
                return translator(name, segment, from_language, to_language, context,selected_model)

            # Iterate over the segments and translate each one
            for name, segment in segments.items():
                if isinstance(segment, str) and segment.strip():
                    translated_segment = translate_segment(name, segment, accumulated_context)
                    accumulated_context += translated_segment
                    translated_code += translated_segment + "\n"
                elif isinstance(segment, list) and segment:
                    for idx, code_block in enumerate(segment, start=1):
                        if code_block.strip():
                            translated_segment = translate_segment(f"{name} {idx}", code_block, accumulated_context)
                            accumulated_context += translated_segment
                            translated_code += translated_segment + "\n"

            # Translate class methods if any
            for class_name, methods in class_methods.items():
                for method in methods:
                    translated_method = translate_segment(f"Method {class_name}.{method}", method, accumulated_context)
                    accumulated_context += translated_method
                    translated_code += translated_method + "\n"
                    
            return translated_code.strip()




@app.route('/api/translate', methods=['POST', 'OPTIONS'])
def translate_code_route():
    if request.method == 'OPTIONS':
        return '', 200

    elif request.method == 'POST': 
        data = request.json
        source_code = data.get('source_code')
        from_language = data.get('from_language', 'python')
        to_language = data.get('to_language', 'java')
        selected_api = data.get('api', 'openai').lower()
        selected_model_ = data.get('model','')
        
        selected_model = map_model_name(selected_model_)
        if not source_code:
            return jsonify({"error": "No code provided"}), 400
       
        translator = get_translator(selected_api)
        if not translator:
            return jsonify({"error": f"Unsupported API: {selected_api}"}), 400

        translated_code = sliding_window_translate(source_code,from_language,to_language,translator,selected_model)
        #translated_code = translate_code(source_code,from_language,to_language,translator,selected_model)
        # After processing the translated code
        if translated_code.strip():
            return jsonify({"translated_code": translated_code}), 200
        else:
            return jsonify({"error": "Translation failed"}), 404
    else:
        return jsonify({"error": "Translation failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
