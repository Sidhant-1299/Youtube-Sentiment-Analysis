FROM python:3.12-slim-bookworm

WORKDIR /app
COPY flask_api/ .
COPY *.pkl .
COPY flask-requirements.txt .

RUN pip install --no-cache-dir -r flask-requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "flask_api/app.py"]
