#!/bin/bash

# AskLegal Enhanced - Startup Script

echo "🚀 Starting AskLegal Enhanced..."

# Kill any existing processes on port 8006
echo "Stopping any existing processes on port 8006..."
lsof -ti:8006 | xargs kill -9 2>/dev/null || true

# Wait a moment
sleep 2

# Start the backend server
echo "Starting backend server..."
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -c "import sys; sys.path.insert(0, '.'); from app.main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8006)" &

# Wait a moment for the server to start
sleep 3

echo "✅ AskLegal Enhanced is running!"
echo "🌐 Frontend: http://localhost:8006"
echo "📚 API Docs: http://localhost:8006/docs"
echo "🔄 Press Ctrl+C to stop"

# Wait for the background process
wait