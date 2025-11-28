FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps (optional, kept minimal)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy app code and requirements
COPY app.py ./app.py
COPY requirements.txt ./requirements.txt

# Create model directory (model can be mounted or copied later)
RUN mkdir -p /app/model

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV MODEL_PATH=/app/model
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]