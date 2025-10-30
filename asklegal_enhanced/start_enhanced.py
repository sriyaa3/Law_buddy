#!/usr/bin/env python3
"""
Enhanced startup script with comprehensive checks and initialization
"""
import os
import sys
import subprocess
import time
import socket
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("="*70)
    print("  AskLegal Enhanced - AI Legal Assistant for MSMEs")
    print("  Starting comprehensive application setup...")
    print("="*70)
    print()

def check_port_available(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def check_models():
    """Check if models are downloaded"""
    print("🤖 Checking models...")
    
    model_files = [
        './models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf',
    ]
    
    missing_models = []
    for model_file in model_files:
        if Path(model_file).exists():
            print(f"  ✓ {Path(model_file).name}")
        else:
            print(f"  ✗ {Path(model_file).name} (missing)")
            missing_models.append(model_file)
    
    if missing_models:
        print("\n⚠️  Some models are missing!")
        response = input("Run model setup now? (y/n): ")
        if response.lower() == 'y':
            print("\nRunning model setup...")
            result = subprocess.run([sys.executable, "setup_models.py"])
            return result.returncode == 0
        else:
            print("⚠️  Continuing without all models...")
            return True
    else:
        print("✓ All models ready")
        return True

def check_database():
    """Check if database is initialized"""
    print("\n💾 Checking database...")
    
    db_path = Path('./asklegal.db')
    if db_path.exists():
        print("  ✓ Database exists")
        return True
    else:
        print("  ⚠️  Database not found")
        response = input("Initialize services now? (y/n): ")
        if response.lower() == 'y':
            print("\nInitializing services...")
            result = subprocess.run([sys.executable, "initialize_services.py"])
            return result.returncode == 0
        else:
            print("⚠️  Continuing without database initialization...")
            return True

def check_frontend():
    """Check frontend build status"""
    print("\n💻 Checking frontend...")
    
    build_dir = Path('./frontend/build')
    if build_dir.exists():
        print("  ✓ Frontend build exists")
        return True
    else:
        print("  ⚠️  Frontend not built")
        print("  Note: You can build with: cd frontend && npm run build")
        return True

def start_backend(port=8000, dev_mode=True):
    """Start the FastAPI backend server"""
    print(f"\n🚀 Starting backend server on port {port}...")
    
    if not check_port_available(port):
        print(f"  ✗ Port {port} is already in use")
        # Try to find an available port
        for i in range(10):
            new_port = port + i
            if check_port_available(new_port):
                port = new_port
                print(f"  Using port {port} instead")
                break
        else:
            print("  Could not find an available port")
            return False
    
    try:
        # Start uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", str(port)
        ]
        
        if dev_mode:
            cmd.append("--reload")
        
        print(f"\n✓ Starting server with command: {' '.join(cmd)}")
        print()
        print("="*70)
        print("✅ AskLegal Enhanced is running!")
        print("="*70)
        print()
        print("Access URLs:")
        print(f"  🌐 Frontend:  http://localhost:{port}")
        print(f"  📚 API Docs:  http://localhost:{port}/api/v1/docs")
        print(f"  🔍 Health:    http://localhost:{port}/api/v1/health")
        print()
        print("Press Ctrl+C to stop the server")
        print("="*70)
        print()
        
        # Start the server
        subprocess.run(cmd)
        return True
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"\n✗ Failed to start server: {e}")
        return False

def main():
    """Main startup function"""
    print_banner()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Parse arguments
    dev_mode = '--prod' not in sys.argv and '--production' not in sys.argv
    skip_checks = '--skip-checks' in sys.argv
    
    if not skip_checks:
        # Run all checks
        if not check_models():
            print("\n⚠️  Model check failed, but continuing...")
        
        if not check_database():
            print("\n⚠️  Database check failed, but continuing...")
        
        check_frontend()
    else:
        print("⚠️  Skipping pre-flight checks...\n")
    
    # Start the backend
    success = start_backend(dev_mode=dev_mode)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()