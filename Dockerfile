# ---------- Stage 1: Builder ----------
FROM python:3.12-slim-bookworm AS builder
# Install build dependencies only here
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# Copy dependency file first for better caching
COPY flask-requirements.txt .
# Install dependencies in a temporary directory
RUN pip install --no-cache-dir --prefix=/install -r flask-requirements.txt

# ---------- Stage 2: Runtime ----------
FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*
# Copy installed Python packages from builder
COPY --from=builder /install /usr/local
# Copy only what’s needed for runtime
COPY *.pkl .
COPY flask_api/ .
EXPOSE 5555

CMD ["python", "app.py"]
