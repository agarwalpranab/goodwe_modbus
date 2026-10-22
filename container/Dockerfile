# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

# Install build tools needed for some goodwe transitive deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ------------------------------------------------------------------
# Dependency layer (cached unless requirements change)
# ------------------------------------------------------------------
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------------
# Application layer
# ------------------------------------------------------------------
COPY goodwe_mqtt/ ./goodwe_mqtt/
COPY main.py ./

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["python", "main.py"]
