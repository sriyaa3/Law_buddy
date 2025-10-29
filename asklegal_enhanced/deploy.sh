#!/bin/bash

# AskLegal Enhanced - Comprehensive Deployment Script
# This script sets up and starts the application with all services

set -e  # Exit on error

echo "========================================"
echo "AskLegal Enhanced - Deployment Script"
echo "========================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Step 1: Check Python version
echo "Step 1: Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_status "Python version is compatible"
else
    print_error "Python 3.8+ is required"
    exit 1
fi

# Step 2: Install Python dependencies
echo ""
echo "Step 2: Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -q -r requirements.txt
    print_status "Python dependencies installed"
else
    print_warning "requirements.txt not found, skipping..."
fi

# Step 3: Setup models
echo ""
echo "Step 3: Setting up models..."
if [ -f "setup_models.py" ]; then
    python3 setup_models.py
    if [ $? -eq 0 ]; then
        print_status "Models setup complete"
    else
        print_warning "Model setup had some issues, but continuing..."
    fi
else
    print_warning "setup_models.py not found, skipping..."
fi

# Step 4: Initialize services
echo ""
echo "Step 4: Initializing services..."
if [ -f "initialize_services.py" ]; then
    python3 initialize_services.py
    if [ $? -eq 0 ]; then
        print_status "Services initialized"
    else
        print_warning "Service initialization had some issues, but continuing..."
    fi
else
    print_warning "initialize_services.py not found, skipping..."
fi

# Step 5: Build frontend (if in production mode)
echo ""
echo "Step 5: Checking frontend..."
if [ "$1" = "--production" ] || [ "$1" = "-p" ]; then
    echo "Building frontend for production..."
    cd frontend
    if [ -d "node_modules" ]; then
        print_status "Node modules found"
    else
        echo "Installing frontend dependencies..."
        npm install
    fi
    
    npm run build
    print_status "Frontend built for production"
    cd ..
else
    print_warning "Skipping frontend build (use --production flag to build)"
fi

# Step 6: Check for supervisor
echo ""
echo "Step 6: Checking supervisor..."
if command -v supervisorctl &> /dev/null; then
    print_status "Supervisor is available"
    
    # Check if supervisor config exists
    if [ -f "supervisord.conf" ]; then
        echo "Starting services with supervisor..."
        
        # Copy config if needed
        if [ -w "/etc/supervisor/conf.d/" ]; then
            sudo cp supervisord.conf /etc/supervisor/conf.d/asklegal.conf
            sudo supervisorctl reread
            sudo supervisorctl update
            sudo supervisorctl restart asklegal_backend
            print_status "Services started with supervisor"
        else
            print_warning "Cannot write to supervisor config directory"
            echo "You can start manually with: supervisord -c supervisord.conf"
        fi
    fi
else
    print_warning "Supervisor not available"
fi

# Step 7: Start application
echo ""
echo "Step 7: Starting application..."

if [ "$1" = "--manual" ] || [ "$1" = "-m" ]; then
    echo "Starting in manual mode..."
    print_status "You can now start the backend with: uvicorn app.main:app --host 0.0.0.0 --port 8001"
else
    echo "Starting backend server..."
    python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload &
    BACKEND_PID=$!
    
    # Wait for backend to start
    sleep 3
    
    if ps -p $BACKEND_PID > /dev/null; then
        print_status "Backend server started (PID: $BACKEND_PID)"
        echo ""
        echo "========================================"
        echo "✅ AskLegal Enhanced is running!"
        echo "========================================"
        echo ""
        echo "Access the application:"
        echo "  - Frontend: http://localhost:8001"
        echo "  - API Docs: http://localhost:8001/api/v1/docs"
        echo ""
        echo "To stop: kill $BACKEND_PID"
        echo ""
        
        # Keep script running
        wait $BACKEND_PID
    else
        print_error "Failed to start backend server"
        exit 1
    fi
fi
