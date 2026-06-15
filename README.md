# 🔍 Fake News Detector — AI-Powered Multimodal Detection System



![Python](https://img.shields.io/badge/Python-3.11-blue)




![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)




![React](https://img.shields.io/badge/React-18-blue)




![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20-orange)




![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-1.6.1-yellow)



> AI-powered fake news detection using Machine Learning, Deep Learning, and LLM Explanation — supporting Text, Image, and Fusion analysis across multiple languages.

---

## 🌐 Live Demo

🔗 **Frontend:** [https://fake-news-pipeline-7rp2.vercel.app](https://fake-news-pipeline-7rp2.vercel.app)

🔗 **Backend API:** [https://fake-news-pipeline.onrender.com/docs](https://fake-news-pipeline.onrender.com/docs)

---

## ✨ Features

- 📝 **Text Detection** — Detects fake news from news articles in multiple languages
- 🖼️ **Image Detection** — Identifies manipulated or AI-generated fake images
- 🔀 **Fusion Detection** — Combines both text and image analysis for higher accuracy
- 🤖 **AI Explanation** — Uses Groq LLM (LLaMA 3.3) to explain why news is fake or real
- 🌍 **Multilingual Support** — Supports English, Bengali, Urdu, Spanish, Japanese
- 🔄 **Auto Retraining Pipeline** — Automatically fetches new fact-checked data from Google Fact Check API and retrains the model every Sunday
- 📊 **Confidence Score** — Shows fake/real probability with confidence percentage

---

## 🏗️ Project Architecture
---

## 🤖 Models Used

### Text Model
| Model | Accuracy |
|-------|----------|
| Logistic Regression (Calibrated) | **94.1%** |
| TF-IDF Vectorizer (max 100k features) | — |

**Training Data:**
- English fake/real news dataset
- Bengali fake news dataset
- Urdu news dataset
- Spanish fake news dataset
- Japanese fake news dataset
- GlobalFakeNews 2026 dataset
- **Total: ~41,000 multilingual samples**

### Image Model
| Architecture | Training Images |
|-------------|----------------|
| EfficientNetB0 (Transfer Learning) | 80,000 |

- Fine-tuned with 2-phase training
- Phase 1: Frozen base layers
- Phase 2: Fine-tuned top 30 layers

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — REST API framework
- **Scikit-learn** — Text classification model
- **TensorFlow/Keras** — Image classification model
- **Groq API (LLaMA 3.3-70B)** — AI explanations
- **Google Fact Check API** — Auto retraining data source
- **gdown** — Model download from Google Drive

### Frontend
- **React.js** — UI framework
- **CSS3** — Styling

### Deployment
- **Render** — Backend hosting
- **Vercel** — Frontend hosting
- **Google Drive** — Model storage
- **GitHub Actions** — Weekly auto-retraining

---

## 🔄 Auto Retraining Pipeline

The model automatically retrains every Sunday using GitHub Actions:

1. Fetches new fact-checked claims from **Google Fact Check API**
2. Merges with existing training data
3. Retrains TF-IDF + Logistic Regression model
4. Saves updated model files

```yaml
schedule:
  - cron: '0 0 * * 0'  # Every Sunday at midnight
👩‍💻 Created By
Rishika Mandal
