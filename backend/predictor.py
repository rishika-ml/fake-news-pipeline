import joblib
import numpy as np
import requests
import os
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "fake_news_model.pkl"))
tfidf = joblib.load(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"))
image_model = load_model(os.path.join(BASE_DIR, "image_model.keras"))

def get_explanation(text, prediction, confidence):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""A fake news detection model analyzed this news text:
    
Text: "{text}"
Prediction: {prediction}
Confidence: {confidence:.2%}

In 2-3 sentences, explain why this news is considered {prediction}. 
Focus on language patterns, claims, and credibility indicators."""

    body = {
        "model": "llama-3.3-70b-versatile",
        "max_tokens": 150,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body
    )
    print("Groq response:", response.json())
    print("Status code:", response.status_code)
    
    data = response.json()
    print("Groq response:", data)  # This will show us what's coming back
    
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return "Explanation unavailable at this time."

# ---- TEXT PREDICTION ----
def predict_news(text):
    X = tfidf.transform([text])
    prob = model.predict_proba(X)[0]

    fake_prob = float(prob[0])
    real_prob = float(prob[1])
    prediction = "REAL" if real_prob > fake_prob else "FAKE"
    confidence = float(max(prob))
    explanation = get_explanation(text, prediction, confidence)

    return {
        "prediction": prediction,
        "fake_probability": fake_prob,
        "real_probability": real_prob,
        "confidence": confidence,
        "explanation": explanation
    }

# ---- IMAGE PREDICTION ----
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    pred = image_model.predict(img_array)[0][0]

    prediction = "FAKE" if pred > 0.5 else "REAL"
    confidence = float(pred) if pred > 0.5 else float(1 - pred)

    # Get explanation 
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "content-type": "application/json"
    }
    prompt = f"""A fake news image detection model analyzed an image:

Prediction: {prediction}
Confidence: {confidence:.2%}

In 2-3 sentences, explain why this image is considered {prediction}.
Focus on common visual manipulation indicators and image credibility."""

    body = {
        "model": "llama-3.3-70b-versatile",
        "max_tokens": 150,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body
    )
    data = response.json()
    if "choices" in data:
        explanation = data["choices"][0]["message"]["content"]
    else:
        explanation = "Explanation unavailable."


    return {
        "prediction": prediction,
        "confidence": confidence,
        "explanation": explanation
    }
