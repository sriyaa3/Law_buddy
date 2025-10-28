import os
import subprocess
import sys

def build_frontend():
    """Build the React frontend"""
    print("Building React frontend...")
    
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    
    if not os.path.exists(frontend_dir):
        print("Frontend directory not found!")
        return False
    
    try:
        # Install dependencies if node_modules doesn't exist
        node_modules_path = os.path.join(frontend_dir, "node_modules")
        if not os.path.exists(node_modules_path):
            print("Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # Build the frontend
        print("Building frontend...")
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
        
        print("Frontend built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error building frontend: {e}")
        return False
    except FileNotFoundError:
        print("npm not found. Please install Node.js and npm.")
        return False

if __name__ == "__main__":
    build_frontend()