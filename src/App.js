import React, { useState } from 'react';
import AceEditor from 'react-ace';

// Import the required Ace build files
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/theme-monokai';
import axios from 'axios';
import './App.css';

function App() {
    const [pythonCode, setPythonCode] = useState('');
    const [javaCode, setJavaCode] = useState('');

    const translateCode = async () => {
      try {
          const response = await axios.post('http://localhost:5000/api/translate', {
              python_code: pythonCode
          });
          setJavaCode(response.data.translated_code);
      } catch (error) {
          console.error('Error translating code:', error);
      }
  };
  

  
  return (
    <div className="App">
        <h1>Python to Java Code Translator</h1>
        <div className="editor-container">
            <div className="editor">
                <h3>Python Code</h3>
                <AceEditor
                    mode="python"
                    theme="monokai"
                    name="pythonEditor"
                    width="600px"
                    height="400px"
                    onChange={setPythonCode}
                    fontSize={14}
                    showPrintMargin={true}
                    showGutter={true}
                    highlightActiveLine={true}
                    value={pythonCode}
                    setOptions={{
                        enableBasicAutocompletion: false,
                        enableLiveAutocompletion: false,
                        enableSnippets: false,
                        showLineNumbers: true,
                        tabSize: 2,
                    }}
                />
            </div>
            <div className="editor">
                <h3>Java Code</h3>
                <AceEditor
                    mode="java"
                    theme="monokai"
                    name="javaEditor"
                    width="600px"
                    height="400px"
                    readOnly={true}
                    value={javaCode}
                    fontSize={14}
                    showPrintMargin={true}
                    showGutter={true}
                    highlightActiveLine={true}
                    setOptions={{
                        showLineNumbers: true,
                        readOnly: true,
                        tabSize: 2,
                    }}
                />
            </div>
        </div>

        <button className="translate-button" onClick={translateCode}>
            Translate to Java
        </button>
    </div>
);
}

export default App;
