# syntax=docker/dockerfile:1

# --- Build stage (optional slim) ---
FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies (add poppler-utils etc if later needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (note: Ollama officially targets host install; inside container this is a lightweight client)
# For full model serving in container we use the official ollama image in docker-compose instead.

WORKDIR /app

# Copy project files
COPY pyproject.toml /app/
# No dependencies declared besides PyPDF2 (add here if updated)
RUN pip install --upgrade pip \
    && pip install PyPDF2

COPY analyze_pdf_with_ollama.py /app/

# Default command (overridden via docker compose for interactive usage)
CMD ["python", "analyze_pdf_with_ollama.py"]
