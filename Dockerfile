FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir uv &&\
    uv venv &&\
    uv pip install . --no-cache

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

CMD ["uv", "run", "flask_api/app.py"]
