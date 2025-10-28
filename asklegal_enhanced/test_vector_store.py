import numpy as np
from app.vector_store.faiss_store import faiss_store
from app.document_processing.embedders import text_embedder

def test_faiss_vector_store():
    """Test the FAISS vector store"""
    try:
        print("\nTesting FAISS vector store...")
        
        # Delete existing index to start fresh
        faiss_store.delete_index()
        
        # Create some test documents
        documents = [
            {
                "text": "This is a contract for software development services.",
                "type": "contract",
                "metadata": {"category": "software", "party": "ABC Corp"}
            },
            {
                "text": "This is a non-disclosure agreement between two parties.",
                "type": "nda",
                "metadata": {"category": "confidentiality", "party": "XYZ Inc"}
            },
            {
                "text": "This is a lease agreement for office space.",
                "type": "lease",
                "metadata": {"category": "real_estate", "party": "Property Owner"}
            }
        ]
        
        # Generate embeddings for the documents
        texts = [doc["text"] for doc in documents]
        embeddings = text_embedder.embed_texts(texts)
        
        print(f"Generated embeddings with shape: {embeddings.shape}")
        
        # Add documents to FAISS vector store
        doc_ids = faiss_store.add_documents(documents, embeddings)
        print(f"Added {len(doc_ids)} documents with IDs: {doc_ids}")
        
        # Test search
        query_text = "software development contract"
        query_embedding = text_embedder.embed_text(query_text)
        
        results = faiss_store.search(query_embedding, limit=3)
        print(f"\nFAISS search results for '{query_text}':")
        for i, result in enumerate(results):
            print(f"  {i+1}. Score: {result['score']:.4f}")
            print(f"     Content: {result['content']}")
            print(f"     Type: {result['type']}")
            print(f"     Metadata: {result['metadata']}")
        
        print("\nFAISS vector store test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing FAISS vector store: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test FAISS vector store
    faiss_success = test_faiss_vector_store()
    
    if faiss_success:
        print("\n✅ FAISS vector store test passed!")
    else:
        print("\n❌ FAISS vector store test failed!")
