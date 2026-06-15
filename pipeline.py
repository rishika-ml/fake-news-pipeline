import requests
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from datetime import datetime, timedelta
import os
import re
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")   
MODEL_PATH = "fake_news_model.pkl"            
VECTORIZER_PATH = "tfidf_vectorizer.pkl"      
DATA_PATH = "training_data.csv" 
DAYS_BACK = 30             
def clean_text(text):
    """Simple text cleaning – adjust to match your original preprocessing"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
def fetch_new_claims(since_days=DAYS_BACK):
    """Fetch fact-checked claims from last 'since_days' days"""
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    all_claims = []
    next_page_token = None
    
    while True:
        params = {
            "key": API_KEY,
            "maxAgeDays": since_days,
            "pageSize": 100,
            "query": "news",
            "languageCode": "und"
        }
        if next_page_token:
            params["pageToken"] = next_page_token
        
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            print(f"API error: {resp.status_code}")
            break
        
        data = resp.json()
        claims = data.get("claims", [])
        if not claims:
            break
        
        for claim in claims:
            text = claim.get("text", "")
            if not text or len(text) < 20:
                continue
            reviews = claim.get("claimReview", [])
            if not reviews:
                continue
            rating = reviews[0].get("textualRating", "").lower()
            # Map rating to label (0 = fake, 1 = real)
            if "true" in rating:
                label = 1
            elif any(w in rating for w in ["false", "fake", "misleading", "incorrect"]):
                label = 0
            else:
                continue
            all_claims.append({"text": text, "label": label})
        
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
    
    if all_claims:
        new_df = pd.DataFrame(all_claims)
        print(f"Fetched {len(new_df)} new claims")
        return new_df
    else:
        print("No new claims fetched")
        return pd.DataFrame()
def load_existing_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()
def save_data(df, path):
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} total rows to {path}")
def load_old_vectorizer_and_model(v_path, m_path):
    """Load your existing .pkl files if they exist"""
    if os.path.exists(v_path) and os.path.exists(m_path):
        vectorizer = joblib.load(v_path)
        model = joblib.load(m_path)
        print(f"Loaded existing vectorizer from {v_path} and model from {m_path}")
        return vectorizer, model
    else:
        print("No existing .pkl files found. Will create new ones.")
        return None, None
def train_model(df, old_vectorizer=None, old_model=None):
    """
    Retrain TfidfVectorizer and classifier on the entire dataset.
    If old_vectorizer and old_model are provided, they are ignored (full retrain).
    """
    print("Starting full retraining using TF-IDF + Logistic Regression...")
    
    # Clean texts (adjust cleaning to match your original)
    df['clean_text'] = df['text'].apply(clean_text)
    
    # Split chronological (last 20% as test)
    split = int(0.8 * len(df))
    train_df = df.iloc[:split]
    test_df = df.iloc[split:]
    
    # Fit vectorizer on all training texts
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2), stop_words='english')
    X_train = vectorizer.fit_transform(train_df['clean_text'])
    X_test = vectorizer.transform(test_df['clean_text'])
    
    y_train = train_df['label'].values
    y_test = test_df['label'].values
    
    # Train classifier
    clf = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    clf.fit(X_train, y_train)
    
    # Calibrate
    calibrated = CalibratedClassifierCV(clf, method='sigmoid', cv='prefit')
    calibrated.fit(X_train, y_train)
    
    # Evaluate
    acc = calibrated.score(X_test, y_test)
    print(f"Test accuracy on recent data: {acc:.4f}")
    
    # Save new .pkl files (overwrites old ones)
    joblib.dump(calibrated, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"Saved updated model to {MODEL_PATH}")
    print(f"Saved updated vectorizer to {VECTORIZER_PATH}")
    
    return calibrated, vectorizer
def main():
    # 1. Fetch new fact-checks
    new_data = fetch_new_claims()
    
    # 2. Load existing training data (CSV)
    existing_data = load_existing_data(DATA_PATH)
    
    # 3. Merge
    if not new_data.empty:
        combined = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        combined = existing_data
    
    if combined.empty:
        print("No data available. Exiting.")
        return
    
    # Remove duplicates based on text
    combined = combined.drop_duplicates(subset=['text'])
    print(f"Total unique samples: {len(combined)}")
    
    # 4. Save merged data for next run
    save_data(combined, DATA_PATH)
    
    train_model(combined)
    
    print("Pipeline finished successfully. Model and vectorizer updated.")
if __name__ == "__main__":
    main()