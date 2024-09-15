import React, { useState, useEffect } from 'react';
import AceEditor from 'react-ace';
// Import the required Ace build files
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-c_cpp';
import 'ace-builds/src-noconflict/mode-ruby';
import 'ace-builds/src-noconflict/mode-php';
import 'ace-builds/src-noconflict/mode-csharp';
import 'ace-builds/src-noconflict/mode-typescript';
import 'ace-builds/src-noconflict/mode-swift';
import 'ace-builds/src-noconflict/mode-sh';
// Import other modes as needed
import 'ace-builds/src-noconflict/theme-monokai';
import ModelManager from './ModelManager';
import { ClipLoader } from 'react-spinners';
import axios from 'axios';
import './App.css';

// Import languages and helper functions from languages.js
import { languages, getEditorMode, languageMappings } from './language';

const apiModels = {
    openai: ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"],
    groq: [
      "gemma-7b-it", 
      "gemma2-9b-it", 
      "llama-3.1-70b-versatile", 
      "llama-3.1-8b-instant", 
      "llama-guard-3-8b", 
      "llama3-70b-8192", 
      "llama3-8b-8192", 
      "llama3-groq-70b-8192-tool-use-preview", 
      "llama3-groq-8b-8192-tool-use-preview", 
      "llava-v1.5-7b-4096-preview", 
      "mixtral-8x7b-32768"
    ],
    ollama: [
      "Llama 3.1 - 8B", 
      "Llama 3.1 - 70B", 
      "Gemma 2 - 2B", 
      "Gemma 2 - 9B", 
      "Mistral-Nemo - 12B", 
      "Mistral Large 2 - 123B", 
      "Qwen 2 - 0.5B", 
      "Qwen 2 - 72B", 
      "DeepSeek-Coder V2 - 16B", 
      "Phi-3 - 3B", 
      "Phi-3 - 14B"
    ],
    llama3: ["Meta Llama-3-8B", "Meta Llama-3-13B", "Meta Llama-3-70B"],
    custom: [] // Custom models can be added here by user input or other means
  };

function App() {
    const [sourceCode, setSourceCode] = useState('');
    const [translatedCode, setTranslatedCode] = useState('');
    const [selectedApi, setSelectedApi] = useState('openai');  // Default to OpenAI
    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/translate';
    const [fromLanguage, setFromLanguage] = useState('python'); // Default source language
    const [toLanguage, setToLanguage] = useState('java'); // Default target language
    const [availableToLanguages, setAvailableToLanguages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [models, setModels] = useState(apiModels[selectedApi]);
    const [selectedModel, setSelectedModel] = useState('');
    const [customModelFile, setCustomModelFile] = useState(null); // Custom model file state



    // First useEffect: Update availableToLanguages when fromLanguage changes
    useEffect(() => {
        const mappedLanguages = languageMappings[fromLanguage] || [];
        const filteredLanguages = languages.filter((lang) =>
        mappedLanguages.includes(lang.value)
        );
        setAvailableToLanguages(filteredLanguages);
    }, [fromLanguage]);
    
    // Second useEffect: Ensure toLanguage is valid
    useEffect(() => {
        if (availableToLanguages.length > 0 && !availableToLanguages.some(lang => lang.value === toLanguage)) {
        setToLanguage(availableToLanguages[0].value);
        }
    }, [toLanguage, availableToLanguages]);
    // Create an object to group languages by category
    const groupedLanguages = languages.reduce((groups, lang) => {
        const category = lang.category || 'Others';
        if (!groups[category]) {
        groups[category] = [];
        }
        groups[category].push(lang);
        return groups;
    }, {});
    const translateCode = async () => {
        if (!sourceCode.trim()) {
            console.error('Source code is empty');
            return; // Don't proceed if source code is empty
        }
        
        setIsLoading(true); // Translation is starting
        setTranslatedCode(''); // Clear previous translation
    
        try {
            const payload = {
                source_code: sourceCode,
                api: selectedApi, // Pass the selected API to the backend
                from_language: fromLanguage,
                to_language: toLanguage
            };
    
            // Conditionally include the model if it's not 'custom'
            if (selectedApi !== 'custom' && selectedModel) {
                payload.model = selectedModel; // Pass the selected model only for non-custom APIs
            }
    
            const response = await axios.post(API_URL, payload);
    
            const translatedCode = response.data.translated_code || '// Translation failed. Please try again.';
            setTranslatedCode(translatedCode);
        } catch (error) {
            console.error('Error translating code:', error);
            setTranslatedCode('// Error during translation. Please try again.');
        } finally {
            setIsLoading(false); // Translation is done
        }
    };
    
    
    const handleApiChange = (event) => {
        const api = event.target.value;
        setSelectedApi(api);
        setModels(apiModels[api]);
        setSelectedModel(''); // Reset model selection
    };

    // Handle Model change
    const handleModelChange = (event) => {
        const model = event.target.value;
        setSelectedModel(model);
    };
    // Handle custom model file selection
  const handleCustomModelChange = (event) => {
    const file = event.target.files[0];
    setCustomModelFile(file); // Store the uploaded custom model file
  };
  
  return (
    <div className="App">
        <h1>Programming Language Translator</h1>
        <div className="api-selector">
                <label htmlFor="api">Choose your AI:</label>
                <select id="api" value={selectedApi} onChange={handleApiChange}>
                    <option value="openai">OpenAI</option>
                    <option value="groq">Groq</option>
                    <option value="ollama">Ollama</option>
                    <option value="llama3">Llama3.1</option>
                    <option value="Custom">Custom</option>

                </select>
            </div>
        {/* Model Selector */}
        {selectedApi !== 'custom' && models && models.length > 0 && (
            <div className="model-selector">
            <label htmlFor="model">Choose a Model:</label>
            <select id="model" value={selectedModel} onChange={handleModelChange}>
                <option value="">--Select a Model--</option>
                {models.map((model, index) => (
                <option key={index} value={model}>{model}</option>
                ))}
            </select>
            </div>
        )}

        {/* Custom Model File Upload */}
        {selectedApi === 'custom' && (
            <div className="custom-model-upload">
            <label htmlFor="customModel">Upload your custom model:</label>
            <input type="file" id="customModel" accept=".bin,.pt,.onnx" onChange={handleCustomModelChange} />
            {customModelFile && <p>Selected model: {customModelFile.name}</p>}
            </div>
        )}

      {/* Model Manager Component */}
      {selectedModel && (
                <ModelManager selectedModel={selectedModel} selectedApi={selectedApi} />
            )}
        <div className="language-selectors">
            <div className="selector">
            <label htmlFor="fromLanguage">From:</label>
            <select
                id="fromLanguage"
                value={fromLanguage}
                onChange={(e) => setFromLanguage(e.target.value)}
            >
            {Object.keys(groupedLanguages).map((category) => (
            <optgroup key={category} label={category}>
                {groupedLanguages[category].map((lang) => (
                <option key={lang.value} value={lang.value}>
                    {lang.name}
                </option>
                ))}
                </optgroup>
            ))}
            </select>
            </div>
            <div className="selector">
                <label htmlFor="toLanguage">To:</label>
                <select
                    id="toLanguage"
                    value={toLanguage}
                    onChange={(e) => setToLanguage(e.target.value)}
                    disabled={availableToLanguages.length === 0}
                >
                    {availableToLanguages.length > 0 ? (
                    availableToLanguages.map((lang) => (
                        <option key={lang.value} value={lang.value}>
                        {lang.name}
                        </option>
                    ))
                    ) : (
                    <option value="">No available languages</option>
                    )}
                </select>
            </div>
        </div>

        <div className="editor-container">
            <div className="editor">
                <h3>{fromLanguage.charAt(0).toUpperCase() + fromLanguage.slice(1)} Code</h3>
                <AceEditor
                    mode={getEditorMode(fromLanguage)}
                    theme="monokai"
                    name="sourceEditor"
                    width="100%"  // Full width of the half container
                    height="100%" // Full height of the half container
                    onChange={setSourceCode}
                    fontSize={14}
                    showPrintMargin={true}
                    showGutter={true}
                    highlightActiveLine={true}
                    value={sourceCode}
                    setOptions={{
                        enableBasicAutocompletion: false,
                        enableLiveAutocompletion: false,
                        enableSnippets: false,
                        showLineNumbers: true,
                        tabSize: 2,
                    }}
                />
            </div>
            <div className="editor editor-wrapper"> {/* Add editor-wrapper class */}
                <h3>
                    {toLanguage ? toLanguage.charAt(0).toUpperCase() + toLanguage.slice(1) : 'Target'} Code
                </h3>
                <AceEditor
                    mode={getEditorMode(toLanguage)}
                    theme="monokai"
                    name="translatedEditor"
                    width="100%" // Full width of the half container
                    height="100%" // Full height of the half container
                    readOnly={true}
                    value={translatedCode}
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
                {isLoading && (
                    <div className="spinner-overlay">
                        <ClipLoader color="#ffffff" loading={isLoading} size={50} />
                        <p>Translating code...</p>
                    </div>
                )}
            </div>
        </div>

        <button
            className="translate-button"
            onClick={translateCode}
            disabled={!toLanguage || isLoading}
        >
            {isLoading ? 'Translating...' : 'Translate Code'}
        </button>
        </div>
);
}

export default App;
