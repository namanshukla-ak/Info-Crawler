#!/bin/bash

# Stop script for Research Intelligence Platform

set -e

echo "🛑 Stopping Research Intelligence Platform..."

# Check if Docker Compose is running
if docker-compose ps | grep -q "Up"; then
    echo "📦 Stopping Docker Compose services..."
    docker-compose down
else
    echo "🐍 Stopping local services..."
    
    # Kill Python processes
    pkill -f "uvicorn main:app" || true
    pkill -f "streamlit run main.py" || true
    
    echo "✅ Services stopped"
fi
