# Inference Service

FastAPI service that loads an MLflow model and exposes `/predict`.

## Local Run

1. Place the MLflow model folder in `inference/model` (contains `MLmodel`).
2. Create venv and install deps:

```bash
cd inference
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Docker Build & Run

```bash
cd inference
docker build -t spam-classifier-api:local .
docker run -p 8000:8000 spam-classifier-api:local
```

## API

- `POST /predict` with JSON: `{ "text": "..." }`
- Response: `{ "prediction": "spam|ham", "confidence": 0.95 }`
