import React from 'react';
import './Result.css';

function Result({ result }) {
  const isFusion = result.text_result || result.image_result;

  if (isFusion) {
    return (
      <div className="result-container">
        <h2>🔀 Fusion Analysis</h2>
        <div className="fusion-grid">
          <div className={`result-card ${result.text_result.prediction === 'FAKE' ? 'fake' : 'real'}`}>
            <h3>📝 Text Analysis</h3>
            <div className="badge">{result.text_result.prediction}</div>
            <p>Confidence: {(result.text_result.confidence * 100).toFixed(1)}%</p>
            <p className="explanation">{result.text_result.explanation}</p>
          </div>
          <div className={`result-card ${result.image_result.prediction === 'FAKE' ? 'fake' : 'real'}`}>
            <h3>🖼️ Image Analysis</h3>
            <div className="badge">{result.image_result.prediction}</div>
            <p>Confidence: {(result.image_result.confidence * 100).toFixed(1)}%</p>
            <p className="explanation">{result.image_result.explanation}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`result-container ${result.prediction === 'FAKE' ? 'fake' : 'real'}`}>
      <div className="result-header">
        <span className="result-icon">
          {result.prediction === 'FAKE' ? '❌' : '✅'}
        </span>
        <h2>{result.prediction}</h2>
      </div>

      <div className="stats">
        <div className="stat">
          <span>Confidence</span>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${(result.confidence * 100).toFixed(1)}%` }}
            ></div>
          </div>
          <span>{(result.confidence * 100).toFixed(1)}%</span>
        </div>

        {result.fake_probability && (
          <>
            <div className="stat">
              <span>Fake Probability</span>
              <div className="progress-bar">
                <div
                  className="progress-fill fake-fill"
                  style={{ width: `${(result.fake_probability * 100).toFixed(1)}%` }}
                ></div>
              </div>
              <span>{(result.fake_probability * 100).toFixed(1)}%</span>
            </div>
            <div className="stat">
              <span>Real Probability</span>
              <div className="progress-bar">
                <div
                  className="progress-fill real-fill"
                  style={{ width: `${(result.real_probability * 100).toFixed(1)}%` }}
                ></div>
              </div>
              <span>{(result.real_probability * 100).toFixed(1)}%</span>
            </div>
          </>
        )}
      </div>

      <div className="explanation-box">
        <h3>🤖 AI Explanation</h3>
        <p>{result.explanation}</p>
      </div>
    </div>
  );
}

export default Result;
