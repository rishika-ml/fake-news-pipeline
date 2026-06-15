import gdown
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def download_models():
    print("Downloading fake_news_model.pkl...")
    gdown.download(
        "https://drive.google.com/uc?id=12IHQMoaZAdcwzf5p0brdB-BHrdNtNW7G",
        os.path.join(BASE_DIR, "fake_news_model.pkl"), quiet=False
    )
    
    print("Downloading tfidf_vectorizer.pkl...")
    gdown.download(
        "https://drive.google.com/uc?id=1tZanRBlZw6CUd6pTpxZI-NkM6emM3gWi",
        os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"), quiet=False
    )
    
    print("Downloading image_model.keras...")
    gdown.download(
        "https://drive.google.com/uc?id=1VI3Uohk7jrbD0Ec7r00Q3UyNNab8RW0R",
        os.path.join(BASE_DIR, "image_model.keras"), quiet=False
    )
    print("All models downloaded!")

if __name__ == "__main__":
    download_models()
