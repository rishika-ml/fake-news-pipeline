import React, { useState } from 'react';
import NewsForm from './components/NewsForm';
import Result from './components/Result';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="app">
      <div className="hero">
        <h1 className="title">
          🔍 Fake News <span>Detector</span>
        </h1>
        <p className="subtitle">
          AI-powered detection using Machine Learning & LLM Explanation
        </p>
      </div>
      <NewsForm setResult={setResult} setLoading={setLoading} />
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Analyzing...</p>
        </div>
      )}
      {result && !loading && <Result result={result} />}
      <footer className="footer">
        <p>© 2026 Fake News Detector | Created by Rishika</p>
      </footer>
    </div>
  );
}

export default App;
