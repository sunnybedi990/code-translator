import React, { useState, useEffect } from 'react';

function ModelManager({ selectedModel, selectedApi }) {
    const [isModelInstalled, setIsModelInstalled] = useState(null);
    const [isPulling, setIsPulling] = useState(false);
    const [progress, setProgress] = useState([]);
    const [isCanceled, setIsCanceled] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false); // New state for success tracking

    // Check if the model is installed
    const checkModelInstallation = async (model) => {
        try {
            const response = await fetch(`http://localhost:5000/api/check-model?model=${model}`);
            const data = await response.json();
            setIsModelInstalled(data.installed);
        } catch (error) {
            console.error('Error checking model installation:', error);
        }
    };

    // Pull the model and capture progress
    const handlePullModel = async () => {
        setIsPulling(true);
        setProgress([]); // Clear previous progress
        setIsSuccess(false); // Reset success state

        try {
            const response = await fetch('http://localhost:5000/api/pull-model', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: selectedModel })
            });

            // Handle streaming response
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let done = false;

            while (!done) {
                const { value, done: readerDone } = await reader.read();
                done = readerDone;
                if (value) {
                    const text = decoder.decode(value, { stream: true });
                    setProgress((prevProgress) => [...prevProgress, text]);
                }
            }

            // If done pulling, set success state
            setIsSuccess(true);
            checkModelInstallation(selectedModel)

        } catch (error) {
            console.error('Error pulling model:', error);
        } finally {
            setIsPulling(false);
        }
    };

    // Cancel model pull (future implementation)
    const cancelPull = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/cancel-pull', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: selectedModel })
            });
            const data = await response.json();
            console.log(data);
            setIsCanceled(true);
            setIsPulling(false);  // Stop pulling process
        } catch (error) {
            console.error('Error canceling pull:', error);
        }
    };

    useEffect(() => {
        if (selectedModel && selectedApi === 'ollama') {
            checkModelInstallation(selectedModel);
        }
    }, [selectedModel, selectedApi]);

    return (
        <div>
            {isModelInstalled === false && !isSuccess && (
                <div>
                    <p>{selectedModel} is not installed. Would you like to pull it?</p>
                    <button onClick={handlePullModel} disabled={isPulling}>
                        {isPulling ? 'Pulling...' : 'Pull Model'}
                    </button>
                </div>
            )}
            {isPulling && (
                <>
                    <div style={{ whiteSpace: 'pre-wrap' }}>
                        {progress.map((line, index) => (
                            <div key={index}>{line}</div>
                        ))}
                    </div>
                    <button onClick={cancelPull}>Cancel</button>
                </>
            )}
            {isSuccess && (
                <p>Model {selectedModel} pulled successfully!</p>
            )}
            {isCanceled && <p>Pull canceled.</p>}
        </div>
    );
}

export default ModelManager;
