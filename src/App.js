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
import { ClipLoader } from 'react-spinners';

import axios from 'axios';
import './App.css';

// Import languages and helper functions from languages.js
import { languages, getEditorMode, languageMappings } from './language';

function App() {
    const [sourceCode, setSourceCode] = useState('');
    const [translatedCode, setTranslatedCode] = useState('');
    const [selectedApi, setSelectedApi] = useState('openai');  // Default to OpenAI
    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/translate';
    const [fromLanguage, setFromLanguage] = useState('python'); // Default source language
    const [toLanguage, setToLanguage] = useState('java'); // Default target language
    const [availableToLanguages, setAvailableToLanguages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);


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
        const response = await axios.post(API_URL, {
            source_code: sourceCode,
            api: selectedApi, // Pass the selected API to the backend
            from_language: fromLanguage,
            to_language: toLanguage
        });
        const translatedCode =
            response.data.translated_code || '// Translation failed. Please try again.';
        setTranslatedCode(translatedCode);
        } catch (error) {
        console.error('Error translating code:', error);
        setTranslatedCode('// Error during translation. Please try again.');
        } finally {
        setIsLoading(false); // Translation is done
        }
    };
    
    const handleApiChange = (event) => {
        setSelectedApi(event.target.value);  // Update the selected API when the user selects an option
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
