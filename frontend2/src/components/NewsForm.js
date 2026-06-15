import React, { useState } from 'react';
import './NewsForm.css';

function NewsForm({ setResult, setLoading }) {
  const [text, setText] = useState('');
  const [image, setImage] = useState(null);
  const [mode, setMode] = useState('text');

  const handleSubmit = async () => {
    setLoading(true);
    setResult(null);

    try {
      if (mode === 'text') {
        const response = await fetch('https://fake-news-pipeline.onrender.com/predict-text', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        const data = await response.json();
        setResult(data);

      } else if (mode === 'image') {
        const formData = new FormData();
        formData.append('file', image);
        const response = await fetch('https://fake-news-pipeline.onrender.com/predict-image', {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        setResult(data);

      } else if (mode === 'fusion') {
        const formData = new FormData();
        formData.append('file', image);
        formData.append('text', text);
        const response = await fetch('https://fake-news-pipeline.onrender.com/predict-fusion', {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        setResult(data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="form-container">
      <div className="mode-tabs">
        <button className={mode === 'text' ? 'active' : ''} 
          onClick={() => setMode('text')}>📝 Text</button>
        <button className={mode === 'image' ? 'active' : ''} 
          onClick={() => setMode('image')}>🖼️ Image</button>
        <button className={mode === 'fusion' ? 'active' : ''} 
          onClick={() => setMode('fusion')}>🔀 Fusion</button>
      </div>

      {(mode === 'text' || mode === 'fusion') && (
        <textarea
          className="text-input"
          placeholder="Paste your news article here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={6}
        />
      )}

      {(mode === 'image' || mode === 'fusion') && (
        <div className="image-upload">
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImage(e.target.files[0])}
          />
        </div>
      )}

      <button className="submit-btn" onClick={handleSubmit}>
        🔍 Analyze
      </button>
    </div>
  );
}

export default NewsForm;
