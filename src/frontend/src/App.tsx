import React from 'react';
import './App.css';

function App() {
  const handleStartInterview = () => {
    // TODO: Connect to backend API
    console.log('Start Interview clicked - not implemented yet');
  };

  return (
    <div className="App">
      <div className="container">
        <h1>System Design Interview Companion</h1>
        <button
          className="start-button"
          onClick={handleStartInterview}
        >
          Start Interview
        </button>
      </div>
    </div>
  );
}

export default App;
