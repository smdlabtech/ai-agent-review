.PHONY: setup run docker-build docker-run lint

setup:
\tpython -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run:
\tstreamlit run app/streamlit_app.py

docker-build:
\tdocker build -t smdlabtech/ai-agent-review:latest -f docker/Dockerfile .

docker-run:
\tdocker run -p 8501:8501 --env-file .env smdlabtech/ai-agent-review:latest

lint:
\tpython -m pip install ruff && ruff check .