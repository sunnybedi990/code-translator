from flask import Flask, request, jsonify
from flask_cors import CORS
# Set your OpenAI API key
from dotenv import load_dotenv
from openai import OpenAI
import os
import re
from translations import get_translator
from segments import get_segments  # Import the get_segments function


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def get_relevant_context(segment, context_map):
    # Analyze the segment for class, method, or variable references
    relevant_context = ""
    if "class" in segment:
        relevant_context += context_map.get("classes", "")
    if "def" in segment or "function" in segment:
        relevant_context += context_map.get("methods", "")
    return relevant_context

def update_context_map(translated_segment, context_map):
    # Extract class names, method signatures, and global variables from the translated segment
    class_match = re.search(r'class\s+(\w+)', translated_segment)
    if class_match:
        context_map['classes'] = translated_segment  # Store the class in context

    method_match = re.search(r'(public|private|protected)?\s+\w+\s+(\w+)\(', translated_segment)
    if method_match:
        context_map['methods'] = translated_segment  # Store the method in context


@app.route('/api/translate', methods=['POST', 'OPTIONS'])
def translate_code():
    if request.method == 'OPTIONS':
        return '', 200

    elif request.method == 'POST': 
        data = request.json
        source_code = data.get('source_code')
        from_language = data.get('from_language', 'python')
        to_language = data.get('to_language', 'java')
        selected_api = data.get('api', 'openai').lower()


        if not source_code:
            return jsonify({"error": "No code provided"}), 400

        try:
            # Segment the source code based on the source language
            segments = get_segments(source_code, from_language)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        translator = get_translator(selected_api)
        if not translator:
            return jsonify({"error": f"Unsupported API: {selected_api}"}), 400
        
        accumulated_context = ""  # Initialize an empty context to accumulate translated code
        translated_code = ""
        context_map = {}  # Initialize an empty map to store accumulated context

        
        # Function to translate a segment with essential context
        def translate_segment(name, segment):
            # Get the relevant context for the current segment
            relevant_context = get_relevant_context(segment, context_map)
            return translator(name, segment, from_language, to_language, relevant_context)


        # Iterate over the segments and translate each one
        for name, segment in segments.items():
            if isinstance(segment, str) and segment.strip():
                translated_segment = translate_segment(name, segment)
                
                # Update the context map after translating each segment
                update_context_map(translated_segment, context_map)

                # Append the translated segment to the overall translated code
                translated_code += translated_segment + "\n"

            elif isinstance(segment, list) and segment:
                for idx, code_block in enumerate(segment, start=1):
                    if code_block.strip():
                        translated_segment = translate_segment(f"{name} {idx}", code_block)
                        
                        # Update the context map and accumulate translated segments
                        update_context_map(translated_segment, context_map)
                        translated_code += translated_segment + "\n"

                            
        print(translated_code)

        # After processing the translated code
        if translated_code.strip():  # Check if there's any translated code
            return jsonify({"translated_code": translated_code}), 200
        else:
            return jsonify({"error": "Java code not found in the response"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
