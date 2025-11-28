import os
import uvicorn
import mlflow.pyfunc
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime

# Path where the MLflow model folder (containing MLmodel) is located
MODEL_PATH = os.environ.get("MODEL_PATH", os.path.join(os.path.dirname(__file__), "model"))
MODEL_PKL = os.environ.get("MODEL_PKL", os.path.join(os.path.dirname(__file__), "model.pkl"))

# Optional SQLite DB for logging predictions
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "predictions.db"))

app = FastAPI(title="Spam Classifier API", version="1.0.0")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    text: str
    request_id: Optional[str] = None


def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT,
                text TEXT,
                prediction TEXT,
                confidence REAL,
                created_at TEXT
            )
            """
        )
        conn.commit()
        conn.close()
    except Exception:
        # DB is optional; proceed without blocking
        pass


@app.on_event("startup")
def load_model():
    global model
    init_db()
    # Prefer MLflow model folder, else fall back to raw joblib model.pkl
    if os.path.isfile(os.path.join(MODEL_PATH, "MLmodel")):
        model = mlflow.pyfunc.load_model(MODEL_PATH)
    elif os.path.isfile(MODEL_PKL):
        model = joblib.load(MODEL_PKL)
        # Wrap into a minimal interface to provide predict([...]) behavior if needed
        # Many sklearn pipelines already have .predict
    else:
        raise RuntimeError(f"No model found. Expected MLflow at {MODEL_PATH} or joblib at {MODEL_PKL}")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    # Predict label
    preds = model.predict([req.text])
    raw_label = preds[0]

    # Remap numeric labels to friendly strings if needed
    if isinstance(raw_label, (int, float)):
        label = "spam" if int(raw_label) == 1 else "ham"
    else:
        label = str(raw_label)

    confidence = None
    probabilities = None

    # Try to get probabilities
    try:
        if hasattr(model, "predict_proba"):
            prob_array = model.predict_proba([req.text])[0]
            classes = getattr(model, "classes_", [])
            # Map class indices to names (convert numeric to spam/ham if binary)
            mapped = {}
            for i, cls in enumerate(classes):
                if isinstance(cls, (int, float)):
                    cls_name = "spam" if int(cls) == 1 else "ham"
                else:
                    cls_name = str(cls)
                mapped[cls_name] = float(prob_array[i] * 100.0)
            probabilities = mapped
            confidence = mapped.get(label, float(max(prob_array) * 100.0))
        elif hasattr(model, "predict"):
            # Fallback: no probabilities available
            confidence = 100.0
    except Exception:
        confidence = 100.0

    # Optional: persist result
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO predictions (request_id, text, prediction, confidence, created_at) VALUES (?, ?, ?, ?, ?)",
            (req.request_id, req.text, label, confidence, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

    return {"prediction": label, "confidence": confidence, "probabilities": probabilities}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
