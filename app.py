from flask import Flask, request, jsonify
from flask_cors import CORS
# Set your OpenAI API key
from dotenv import load_dotenv
from openai import OpenAI
import os
import re

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/translate": {"origins": ["http://localhost:3000"]}})


# Initialize the OpenAI client with your API key
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
@app.route('/api/translate', methods=['POST', 'OPTIONS'])
def translate_code():
    if request.method == 'OPTIONS':
        return '', 200

    elif request.method == 'POST': 
        data = request.json
        python_code = data.get('python_code')

        if not python_code:
            return jsonify({"error": "No code provided"}), 400

        # Split the Python code into identifiable parts
        segments = {
            "Imports": '\n'.join(re.findall(r'^\s*import.*|^\s*from.*import.*', python_code, flags=re.MULTILINE)),
            "Global Variables": '\n'.join(re.findall(r'^(?!.*def|.*class|if __name__|^\s*import|from.*import)(.*=.*)', python_code, flags=re.MULTILINE)),
            "Classes": re.findall(r'^\s*class\s+[\s\S]+?(?=\n^\s*class|\Z)', python_code, flags=re.MULTILINE | re.DOTALL),
            "Functions": re.findall(r'^(def\s[\s\S]+?)(?=\ndef|\Z|$)', python_code, flags=re.MULTILINE),
            "Main Block": '\n'.join(re.findall(r'if __name__ == ["\']__main__["\']:\s*([\s\S]+)', python_code))
        }
        translated_code = ""
        java_code_regex = r"```java\n(.*?)\n```"

        # Function to translate a segment
        def translate_segment(name, segment):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are a code translator. Translate this segment of Python code into Java. Segment: {name}. Do not provide any explanations just provide the code."},
                    {"role": "user", "content": f"""Please translate the following Python code into Java. Ensure the Java code is correctly formatted and enclosed in triple backticks (` ``` `) to indicate the start and end of the Java code block:

                                            ```python
                                            {segment}
                                            ```

                                            Please provide the Java output:
                                            """}
                ],
                temperature=0.3,
                max_tokens=2000,
                top_p=1
            )
            
            if response.choices:
                content = response.choices[0].message.content.strip()
                match = re.search(r"```java\n(.*?)(?:\n```|$)", content, re.DOTALL)
                if match:
                    java_code = match.group(1).strip()
                    return f"// {name}\n{java_code}\n\n"
                else:
                    return f"// {name} - Java translation failed\n\n"

        # Iterate over the segments and translate based on the segment type
        for name, segment in segments.items():
            print(f"{name}: {segment}")
            
            # Check if the segment is a string and not empty before translating
            if isinstance(segment, str) and segment.strip():
                # Translate Imports and Global Variables directly
                if name == "Imports":
                    translated_code += translate_segment("Imports", segment)

                elif name == "Global Variables":
                    translated_code += translate_segment("Global Variables", segment)

            # Check if the segment is a list and contains non-empty items
            elif isinstance(segment, list) and segment:
                # Translate each class individually
                if name == "Classes":
                    for idx, class_code in enumerate(segment, start=1):
                        if class_code.strip():
                            translated_code += translate_segment(f"Class {idx}", class_code)

                # Translate each function individually
                elif name == "Functions":
                    for idx, function_code in enumerate(segment, start=1):
                        if function_code.strip():
                            translated_code += translate_segment(f"Function {idx}", function_code)

            # Translate the main block if it's present
            elif name == "Main Block" and isinstance(segment, str) and segment.strip():
                translated_code += translate_segment("Main Block", segment)



        print(translated_code)

        # After processing the translated code
        if translated_code.strip():  # Check if there's any translated code
            return jsonify({"translated_code": translated_code}), 200
        else:
            return jsonify({"error": "Java code not found in the response"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
