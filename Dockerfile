FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir uv && uv pip install . --no-cache

CMD ["uv", "run", "flask_api/app.py"]
