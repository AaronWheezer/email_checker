# Handleiding (kort): Lokaal deployen

Deze verkorte handleiding focust alleen op het lokale deploy-proces.

## Docker (snelste demo)
```pwsh
cd .\inference
docker build -t spam-api:local .
# Als het model (MLflow-map of model.pkl) in de inference-folder staat, wordt het nu meegekopieerd.
# Heb je geen lokaal model? Monteer dan model.pkl:
docker run -d -p 8000:8000 --name spam-api -v "$PWD\model.pkl:/app/model.pkl" spam-api:local
```
Frontend `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Kubernetes met k3d (lokale cluster)
```pwsh
# 1) Cluster maken
k3d cluster create spam-dev
k3d kubeconfig merge spam-dev --switch-context

# 2) Image bouwen + importeren
cd .\inference
docker build -t ghcr.io/aaronwheezer/email-spam-api:local .
k3d image import ghcr.io/aaronwheezer/email-spam-api:local --cluster spam-dev

# 3) Deployen met lokale manifest
cd ..\kubernetes
kubectl apply -f .\deployment.local.yaml
kubectl get pods
kubectl get svc spam-classifier-service-local

# 4) Endpoint bereikbaar maken
kubectl port-forward svc/spam-classifier-service-local 8000:80
```
Frontend `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Opmerking over het model
- In CI/CD wordt het model gedownload naar `inference/`. De Dockerfile kopieert nu de héle `inference/` folder, dus als er een MLflow-map (`model/` met `MLmodel`) of `model.pkl` aanwezig is, komt die in de image.
- Heb je lokaal geen model (bv. je hebt `inference/` leeggemaakt)? Dan kan Docker niets kopiëren. Gebruik dan ofwel een bind-mount van `model.pkl`, of trek de laatste image van GHCR die tijdens CI/CD is gebouwd.
- Kubernetes (k3d) kan de lokale image `ghcr.io/aaronwheezer/email-spam-api:local` gebruiken. Als die zonder model is gebouwd, monteer je een volume of rebuild nadat je het model lokaal hebt (via `az ml model download`).
