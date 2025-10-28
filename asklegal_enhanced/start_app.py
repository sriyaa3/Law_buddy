#!/usr/bin/env python3
"""
Startup script for AskLegal Enhanced
"""
import os
import sys
import subprocess
import time

def install_requirements():
    """Install required packages"""
    print("1. Installing requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        return False
    return True

def check_docker():
    """Check if Docker is installed and running"""
    print("2. Checking Docker...")
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Docker is installed: {result.stdout.strip()}")
            
            # Check if Docker daemon is running
            try:
                subprocess.run(["docker", "info"], capture_output=True, check=True)
                print("Docker daemon is running")
                return True
            except subprocess.CalledProcessError:
                print("Docker daemon is not running")
                return False
        else:
            print("Docker is not installed")
            return False
    except FileNotFoundError:
        print("Docker is not installed")
        return False

def start_qdrant():
    """Start Qdrant vector database"""
    print("3. Starting Qdrant...")
    try:
        subprocess.run([
            "docker", "run", "-d",
            "--name", "asklegal-qdrant",
            "-p", "6333:6333",
            "-p", "6334:6334",
            "qdrant/qdrant:latest"
        ], check=True, capture_output=True)
        print("Qdrant started successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Qdrant container: {e}")
        return False

def start_application():
    """Start the FastAPI application"""
    print("4. Starting application...")
    print("Starting FastAPI server...")
    print("Server will be available at http://localhost:8001")
    
    try:
        # Start the application with uvicorn on port 8001
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8001",
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start FastAPI server: {e}")
        return False
    return True

def main():
    """Main startup function"""
    print("AskLegal Enhanced - Startup Script")
    print("========================================")
    print(f"Working directory: {os.getcwd()}")
    
    # Install requirements
    if not install_requirements():
        return
    
    # Check Docker
    docker_available = check_docker()
    
    # Start Qdrant if Docker is available
    if docker_available:
        start_qdrant()
    else:
        print("Skipping Qdrant startup due to Docker unavailability")
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()