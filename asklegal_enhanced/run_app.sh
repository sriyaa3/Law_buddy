#!/bin/bash

# Run AskLegal Enhanced Application
# This script starts the FastAPI backend server

echo "=========================================="
echo "  AskLegal Enhanced - AI Legal Assistant"
echo "=========================================="
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Check if backend process is already running
if pgrep -f "uvicorn app.main:app" > /dev/null; then
    echo "⚠️  Backend is already running!"
    echo "   To stop: pkill -f 'uvicorn app.main:app'"
    echo ""
    existing_pid=$(pgrep -f "uvicorn app.main:app")
    echo "   Running PID: $existing_pid"
    echo ""
else
    echo "🚀 Starting backend server..."
    
    # Start backend server
    nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/asklegal_backend.log 2>&1 &
    backend_pid=$!
    
    # Wait a bit for server to start
    sleep 3
    
    # Check if server started successfully
    if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
        echo "✅ Backend server started successfully!"
        echo "   PID: $backend_pid"
    else
        echo "❌ Backend server failed to start"
        echo "   Check logs: tail -f /tmp/asklegal_backend.log"
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "  Application URLs:"
echo "=========================================="
echo "  🌐 Frontend:     http://localhost:8000"
echo "  📚 API Docs:     http://localhost:8000/api/v1/docs"
echo "  🔍 Health Check: http://localhost:8000/api/v1/health"
echo "=========================================="
echo ""
echo "📝 Logs:"
echo "   Backend: tail -f /tmp/asklegal_backend.log"
echo ""
echo "🛑 To stop the server:"
echo "   pkill -f 'uvicorn app.main:app'"
echo ""
echo "✅ Application is ready to use!"
echo ""
