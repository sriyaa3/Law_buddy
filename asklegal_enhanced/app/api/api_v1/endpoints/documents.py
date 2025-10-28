from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import os
import uuid
from app.core.config import settings
from app.document_processing.processor import document_processor
from app.document_processing.embedders import text_embedder
from app.document_processing.extractors.entity_extractor import entity_extractor
from app.vector_store.faiss_store import faiss_store
from app.metadata_store.redis_store import redis_store
from app.graph_db.neo4j_connector import neo4j_connector
from app.privacy.privacy_layer import privacy_layer

router = APIRouter()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document and process it with enhanced parsing
    """
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process document with enhanced parser
        elements = document_processor.process_document(file_path)
        
        if not elements:
            raise HTTPException(status_code=400, detail="Could not process document")
        
        # Extract entities and clauses
        all_text = " ".join([elem["text"] for elem in elements if "text" in elem])
        entities = entity_extractor.extract_entities(all_text)
        clause_info = entity_extractor.extract_clauses_and_relationships(all_text)
        
        # Apply privacy measures if needed
        sensitivity = privacy_layer.classify_query_sensitivity(all_text)
        processed_text = privacy_layer.process_document(all_text, sensitivity)
        
        # Generate embeddings for each element
        doc_embeddings = []
        doc_data = []
        
        for element in elements:
            if "text" in element and element["text"]:
                # Generate embedding
                embedding = text_embedder.embed_text(element["text"])
                
                # Store element data
                element_data = {
                    "text": element["text"],
                    "metadata": {
                        "filename": file.filename,
                        "file_path": file_path,
                        "element_id": element["id"],
                        "element_type": element["type"],
                        **element.get("metadata", {})
                    },
                    "type": "document_element"
                }
                
                doc_embeddings.append(embedding)
                doc_data.append(element_data)
        
        # Store in FAISS vector store
        if doc_data and doc_embeddings:
            import numpy as np
            embeddings_array = np.array(doc_embeddings)
            doc_ids = faiss_store.add_documents(doc_data, embeddings_array)
        else:
            doc_ids = []
        
        # Store metadata in Redis
        if redis_store:
            metadata = document_processor.extract_metadata(file_path)
            metadata.update({
                "element_count": len(elements),
                "entity_count": len(entities),
                "clause_count": len(clause_info["clauses"]),
                "sensitivity": sensitivity.value
            })
            
            if doc_ids:
                redis_store.store_document_metadata(doc_ids[0], metadata)
        
        # Store in Neo4j graph database
        if neo4j_connector and doc_ids:
            doc_id = doc_ids[0]
            # Create document node
            neo4j_connector.create_document_node(doc_id, metadata)
            
            # Create clause nodes
            for i, clause in enumerate(clause_info["clauses"]):
                clause_id = f"{doc_id}_clause_{i}"
                neo4j_connector.create_clause_node(clause_id, clause["text"], doc_id)
            
            # Create entity nodes
            for i, entity in enumerate(entities):
                entity_id = f"{doc_id}_entity_{i}"
                neo4j_connector.create_entity_node(entity_id, entity["text"], entity["label"])
        
        return JSONResponse(content={
            "document_id": doc_ids[0] if doc_ids else None,
            "filename": file.filename,
            "elements_processed": len(elements),
            "entities_extracted": len(entities),
            "clauses_extracted": len(clause_info["clauses"]),
            "sensitivity_level": sensitivity.value,
            "message": "Document uploaded and processed successfully"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.get("/process/{document_id}")
async def process_document(document_id: str):
    """
    Process a document and return detailed analysis
    """
    try:
        # Retrieve document from FAISS store (simplified)
        # In a real implementation, you would map document_id to FAISS indices
        
        # Retrieve metadata from Redis
        metadata = None
        if redis_store:
            metadata = redis_store.get_document_metadata(document_id)
        
        # Retrieve structure from Neo4j
        structure = {}
        if neo4j_connector:
            structure = neo4j_connector.get_document_structure(document_id)
        
        return JSONResponse(content={
            "document_id": document_id,
            "metadata": metadata,
            "structure": structure,
            "analysis": {
                "summary": "This document has been processed with advanced parsing and entity extraction.",
                "key_points": [
                    "Document structure analyzed with layout awareness",
                    "Legal entities extracted using NER",
                    "Clauses identified and indexed",
                    "Metadata stored for fast retrieval"
                ],
                "entities": structure.get("entities", []),
                "clauses": structure.get("clauses", [])
            }
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.post("/upload/scanned")
async def upload_scanned_document(file: UploadFile = File(...)):
    """
    Upload and process a scanned document using OCR
    """
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process scanned document with OCR
        elements = document_processor.process_scanned_document(file_path)
        
        if not elements:
            raise HTTPException(status_code=400, detail="Could not process scanned document")
        
        # Extract entities and clauses
        all_text = " ".join([elem["text"] for elem in elements if "text" in elem])
        entities = entity_extractor.extract_entities(all_text)
        clause_info = entity_extractor.extract_clauses_and_relationships(all_text)
        
        # Apply privacy measures if needed
        sensitivity = privacy_layer.classify_query_sensitivity(all_text)
        processed_text = privacy_layer.process_document(all_text, sensitivity)
        
        # Generate embeddings for each element
        doc_embeddings = []
        doc_data = []
        
        for element in elements:
            if "text" in element and element["text"]:
                # Generate embedding
                embedding = text_embedder.embed_text(element["text"])
                
                # Store element data
                element_data = {
                    "text": element["text"],
                    "metadata": {
                        "filename": file.filename,
                        "file_path": file_path,
                        "element_id": element["id"],
                        "element_type": element["type"],
                        **element.get("metadata", {})
                    },
                    "type": "scanned_document_element"
                }
                
                doc_embeddings.append(embedding)
                doc_data.append(element_data)
        
        # Store in FAISS vector store
        if doc_data and doc_embeddings:
            import numpy as np
            embeddings_array = np.array(doc_embeddings)
            doc_ids = faiss_store.add_documents(doc_data, embeddings_array)
        else:
            doc_ids = []
        
        # Store metadata in Redis
        if redis_store:
            metadata = document_processor.extract_metadata(file_path)
            metadata.update({
                "element_count": len(elements),
                "entity_count": len(entities),
                "clause_count": len(clause_info["clauses"]),
                "sensitivity": sensitivity.value,
                "is_scanned": True
            })
            
            if doc_ids:
                redis_store.store_document_metadata(doc_ids[0], metadata)
        
        return JSONResponse(content={
            "document_id": doc_ids[0] if doc_ids else None,
            "filename": file.filename,
            "elements_processed": len(elements),
            "entities_extracted": len(entities),
            "clauses_extracted": len(clause_info["clauses"]),
            "sensitivity_level": sensitivity.value,
            "ocr_confidence": elements[0].get("metadata", {}).get("confidence", "N/A") if elements else "N/A",
            "message": "Scanned document uploaded and processed successfully"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing scanned document: {str(e)}")