from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from predictor import predict_news, predict_image
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

# ---- TEXT ENDPOINT ----
@app.post("/predict-text")
def predict_text(req: TextRequest):
    return predict_news(req.text)

# ---- IMAGE ENDPOINT ----
@app.post("/predict-image")
async def predict_img(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = predict_image(temp_path)
    os.remove(temp_path)
    return result

# ---- FUSION ENDPOINT ----
@app.post("/predict-fusion")
async def predict_fusion(file: UploadFile = File(...), text: str = ""):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text_result = predict_news(text)
    image_result = predict_image(temp_path)
    os.remove(temp_path)
    return {
        "text_result": text_result,
        "image_result": image_result
    }
from pipeline import main as run_pipeline

@app.post("/retrain")
def retrain_model():
    try:
        run_pipeline()
        return {"status": "success", "message": "Model retrained successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
