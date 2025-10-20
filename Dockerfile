FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY *.pkl .

COPY flask-requirements.txt .
RUN pip install --no-cache-dir -r flask-requirements.txt

COPY flask_api/ .

EXPOSE 5555
CMD ["python", "flask_api/app.py"]
