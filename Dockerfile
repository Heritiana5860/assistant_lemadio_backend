FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_prod.txt .
RUN pip install --no-cache-dir -r requirements_prod.txt

COPY . .

RUN mkdir -p logs rag/data

EXPOSE 5000

CMD ["gunicorn", "app_lc:app", "--workers", "1", "--timeout", "180", "--bind", "0.0.0.0:5000"]