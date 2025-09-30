#!/bin/bash

# Render.com start script for FastAPI

uvicorn main:app \
  --host 0.0.0.0 \
  --port ${PORT:-8000}
