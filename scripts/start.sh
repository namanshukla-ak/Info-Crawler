#!/bin/bash

# Start script for Research Intelligence Platform
# This script starts both backend and frontend services

set -e

echo "🚀 Starting Research Intelligence Platform..."

# Check if Docker is available
if command -v docker-compose &> /dev/null; then
    echo "📦 Using Docker Compose..."
    docker-compose up --build
else
    echo "🐍 Starting services locally..."
    
    # Start backend in background
    echo "Starting backend..."
    cd backend
    if [ ! -d "venv" ]; then
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
    python main.py &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    echo "Waiting for backend to start..."
    sleep 5
    
    # Start frontend
    echo "Starting frontend..."
    cd frontend
    if [ ! -d "venv" ]; then
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
    streamlit run main.py &
    FRONTEND_PID=$!
    cd ..
    
    echo ""
    echo "✅ Services started!"
    echo "📊 Frontend: http://localhost:8501"
    echo "🔌 Backend: http://localhost:8000"
    echo "📖 API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    # Trap SIGINT and SIGTERM to cleanup
    trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM
    
    # Wait for both processes
    wait $BACKEND_PID $FRONTEND_PID
fi
