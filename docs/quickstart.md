# Quickstart

## Local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Renseignez OPENAI_API_KEY ou GOOGLE_API_KEY
streamlit run app/streamlit_app.py
```

## Docker

```bash
docker build -t ai-agent-review -f docker/Dockerfile .
docker run -p 8501:8501 --env-file .env ai-agent-review
```

## Cloud Run (manual)

```bash
gcloud builds submit --tag gcr.io/$(gcloud config get-value project)/ai-agent-review
gcloud run deploy ai-agent-review \
  --image gcr.io/$(gcloud config get-value project)/ai-agent-review \
  --region europe-west1 --allow-unauthenticated --port 8501
```