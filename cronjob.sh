#!/bin/bash
# Iniciar cron en segundo plano
cron

# Forzar regenerar embeddings al arrancar
python /app/generate_embeddings.py

# Iniciar API
uvicorn main:app --host 0.0.0.0 --port 8000
