#!/usr/bin/env python3
"""
Test SLM initialization
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

try:
    from app.slm.engine import inference_engine
    print("SLM engine imported successfully")
    
    # Check if engine is initialized
    if inference_engine.is_initialized:
        print("SLM engine is already initialized")
    else:
        print("SLM engine is not initialized")
        print("Available models:")
        models = inference_engine.get_available_models()
        for name, info in models.items():
            status = "✓ Downloaded" if inference_engine.is_model_available(name) else "○ Not downloaded"
            print(f"  {name} ({info['size']}) - {status}")
    
except Exception as e:
    print(f"Error importing SLM engine: {e}")
    import traceback
    traceback.print_exc()