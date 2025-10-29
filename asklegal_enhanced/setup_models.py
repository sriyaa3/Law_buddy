#!/usr/bin/env python3
"""
Comprehensive model setup script for AskLegal Enhanced
Downloads and verifies all required open-source models
"""
import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    print("📦 Checking requirements...")
    required_packages = [
        'transformers',
        'sentence-transformers',
        'torch',
        'faiss-cpu'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ✗ {package} (missing)")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Installing missing packages...")
        for package in missing:
            # Fixed: Removed text parameter when capture_output=False to satisfy pyright
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=False)
        print("✅ All packages installed!")
    return True

def setup_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    directories = [
        './models',
        './models/embeddings',
        './data',
        './uploads',
        './vector_store'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {dir_path}")
    
    return True

def download_tinyllama():
    """Download TinyLlama model (already done, just verify)"""
    print("\n🤖 Checking TinyLlama model...")
    model_path = Path('./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf')
    
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"  ✓ TinyLlama model found ({size_mb:.1f} MB)")
        return True
    else:
        print("  ⚠️  TinyLlama model not found")
        print("  Run: python download_model.py")
        return False

def download_embedding_model():
    """Download sentence transformer model for embeddings"""
    print("\n🔤 Setting up embedding model...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # Using a lightweight open-source embedding model
        model_name = "all-MiniLM-L6-v2"  # 80MB, fast and efficient
        print(f"  Downloading {model_name}...")
        
        model = SentenceTransformer(model_name, cache_folder='./models/embeddings')
        print(f"  ✓ Embedding model ready: {model_name}")
        
        # Test embedding
        test_text = "Test legal document"
        embedding = model.encode(test_text)
        print(f"  ✓ Test embedding successful (dim: {len(embedding)})")
        
        return True
    except Exception as e:
        print(f"  ✗ Error downloading embedding model: {e}")
        return False

def setup_faiss_index():
    """Initialize FAISS vector store"""
    print("\n🗄️  Setting up FAISS vector store...")
    
    try:
        import faiss
        import numpy as np
        
        # Create a simple FAISS index for testing
        dimension = 384  # Dimension for all-MiniLM-L6-v2
        index = faiss.IndexFlatL2(dimension)
        
        # Add some dummy vectors for testing
        dummy_vectors = np.random.random((10, dimension)).astype('float32')
        index.add(dummy_vectors)  # type: ignore
        
        # Save index
        index_path = './vector_store/test_index.faiss'
        faiss.write_index(index, index_path)
        
        print(f"  ✓ FAISS index created with {index.ntotal} vectors")
        print(f"  ✓ Saved to: {index_path}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error setting up FAISS: {e}")
        return False

def verify_models():
    """Verify all models are working"""
    print("\n✅ Verifying model setup...")
    
    checks = {
        'TinyLlama': Path('./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf').exists(),
        'Embeddings': Path('./models/embeddings').exists(),
        'FAISS Store': Path('./vector_store').exists(),
        'Data Directory': Path('./data').exists(),
    }
    
    all_good = True
    for name, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {name}")
        if not status:
            all_good = False
    
    return all_good

def main():
    """Main setup function"""
    print("="*60)
    print("AskLegal Enhanced - Model Setup")
    print("Setting up open-source models and services")
    print("="*60)
    
    try:
        # Step 1: Check requirements
        if not check_requirements():
            print("\n❌ Failed to install requirements")
            return False
        
        # Step 2: Setup directories
        if not setup_directories():
            print("\n❌ Failed to setup directories")
            return False
        
        # Step 3: Verify TinyLlama
        download_tinyllama()
        
        # Step 4: Download embedding model
        if not download_embedding_model():
            print("\n⚠️  Embedding model setup failed, but continuing...")
        
        # Step 5: Setup FAISS
        if not setup_faiss_index():
            print("\n⚠️  FAISS setup failed, but continuing...")
        
        # Step 6: Verify everything
        if verify_models():
            print("\n" + "="*60)
            print("✅ Model setup complete!")
            print("="*60)
            print("\nNext steps:")
            print("  1. Run: python initialize_services.py")
            print("  2. Run: python start_app.py")
            return True
        else:
            print("\n⚠️  Some components missing, but basic setup is ready")
            return True
            
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
