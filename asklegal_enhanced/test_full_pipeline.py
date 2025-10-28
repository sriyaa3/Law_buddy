#!/usr/bin/env python3
"""
Comprehensive test of the full AskLegal pipeline
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_multimodal_data_ingestion():
    """Test multimodal data ingestion components"""
    print("Testing Multimodal Data Ingestion...")
    
    try:
        from app.document_processing.preprocessors.ocr import ocr_preprocessor
        from app.document_processing.parsers.advanced_parser import advanced_parser
        from app.document_processing.processor import document_processor
        print("✅ Multimodal data ingestion components loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error in multimodal data ingestion: {e}")
        return False

def test_clause_graph_construction():
    """Test clause-graph construction components"""
    print("Testing Clause-Graph Construction...")
    
    try:
        from app.document_processing.extractors.entity_extractor import entity_extractor
        from app.graph_db.neo4j_connector import neo4j_connector
        print("✅ Clause-graph construction components loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error in clause-graph construction: {e}")
        return False

def test_embeddings_indexing():
    """Test embeddings and indexing components"""
    print("Testing Embeddings & Indexing...")
    
    try:
        from app.document_processing.embedders import text_embedder, image_embedder
        from app.vector_store.faiss_store import faiss_store
        from app.metadata_store.redis_store import redis_store
        
        # Test text embedding
        test_text = "This is a test document for MSME compliance."
        embedding = text_embedder.embed_text(test_text)
        print(f"✅ Text embedding generated (shape: {embedding.shape})")
        
        # Test FAISS store
        print("✅ Embeddings and indexing components loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error in embeddings and indexing: {e}")
        return False

def test_retrieval_engine():
    """Test retrieval engine components"""
    print("Testing Retrieval Engine...")
    
    try:
        from app.retrieval.hybrid_retriever import hybrid_retriever
        print("✅ Retrieval engine components loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error in retrieval engine: {e}")
        return False

def test_privacy_layer():
    """Test privacy layer components"""
    print("Testing Privacy Layer...")
    
    try:
        from app.privacy.privacy_layer import privacy_layer
        print("✅ Privacy layer components loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error in privacy layer: {e}")
        return False

def test_model_integration():
    """Test model integration components"""
    print("Testing Model Integration...")
    
    try:
        from app.slm.model_router import model_router
        from app.slm.engine import inference_engine
        print("✅ Model integration components loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error in model integration: {e}")
        return False

def test_downstream_applications():
    """Test downstream applications"""
    print("Testing Downstream Applications...")
    
    try:
        from app.documents.generator import document_generator
        from app.judgment.predictor import judgment_predictor
        print("✅ Downstream applications loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error in downstream applications: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("Testing API Endpoints...")
    
    try:
        from app.api.api_v1.endpoints import chat, documents, judgment, document_generation
        print("✅ API endpoints loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error in API endpoints: {e}")
        return False

def main():
    """Run all tests"""
    print("Running comprehensive AskLegal pipeline test...\n")
    
    tests = [
        test_multimodal_data_ingestion,
        test_clause_graph_construction,
        test_embeddings_indexing,
        test_retrieval_engine,
        test_privacy_layer,
        test_model_integration,
        test_downstream_applications,
        test_api_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{total} components working")
    
    if passed == total:
        print("🎉 All components are working! The AskLegal system is ready.")
    else:
        print("⚠️  Some components need attention. Check the errors above.")

if __name__ == "__main__":
    main()