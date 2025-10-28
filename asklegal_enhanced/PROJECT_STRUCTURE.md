# AskLegal Enhanced - Project Structure

## Overview
This project implements an AI Legal Assistant specifically tailored for Micro, Small, and Medium Enterprises (MSMEs) with advanced multimodal RAG capabilities using FAISS, Neo4j, Redis, and Small Language Models (SLMs).

## Directory Structure
```
asklegal_enhanced/
├── app/                        # Backend application
│   ├── api/                   # API endpoints
│   │   └── api_v1/           # Version 1 API
│   │       ├── endpoints/    # API endpoint implementations
│   │       └── api.py        # API router
│   ├── core/                 # Core configuration
│   ├── document_processing/  # Document processing modules
│   │   ├── parsers/          # Advanced document parsers
│   │   ├── preprocessors/    # OCR and image preprocessing
│   │   ├── embedders/        # Text and multimodal embedding
│   │   ├── extractors/       # Entity and clause extraction
│   │   ├── processor.py      # Main document processor
│   │   └── embedders.py      # Main embedding interface
│   ├── documents/            # Document generation
│   ├── graph_db/             # Neo4j graph database connector
│   ├── judgment/             # Judgment prediction
│   ├── metadata_store/       # Redis metadata storage
│   ├── models/               # Database models
│   ├── msme/                 # MSME-specific features
│   ├── privacy/              # Privacy layer implementation
│   ├── retrieval/            # Hybrid retrieval engine
│   ├── slm/                  # Small Language Models integration
│   └── vector_store/         # Vector store implementation (FAISS only)
├── data/                     # FAISS index data and generated documents
├── frontend/                 # React frontend
│   ├── build/                # Production build
│   ├── public/               # Static assets
│   └── src/                  # React components and pages
├── models/                   # Downloaded SLM models
├── uploads/                  # Uploaded documents
├── requirements.txt          # Python dependencies
├── start.sh                 # Application startup script
└── README.md                # Project documentation
```

## Key Components

### 1. Advanced Multimodal Document Processing
- Process PDF, DOCX, TXT, and scanned documents
- OCR with Tesseract for scanned documents
- Layout-aware parsing with LayoutLMv3
- Clause and entity extraction with spaCy Legal NER
- Metadata extraction with pdfplumber and python-docx

### 2. Privacy-Preserving AI Models
- Local SLM inference with ctransformers (Phi-3, TinyLlama)
- Quantized models for reduced memory usage
- No external API calls for maximum privacy
- Privacy layer with sensitivity classification and data anonymization

### 3. Hybrid Retrieval System
- FAISS vector store for similarity search
- Redis metadata store for fast filtering
- BM25 keyword search integration
- Re-ranking with weighted scoring

### 4. Knowledge Graph
- Neo4j graph database for legal relationships
- Clause-entity relationship mapping
- Document structure representation

### 5. MSME Customization
- Industry-specific legal knowledge base
- Business context collection
- Personalized recommendations
- Workflow automation

### 6. Downstream Applications
- Legal Document Generator (templates for contracts, notices)
- Chatbot Interface (interactive answers with citations)
- Judgment Predictor (outcome probability with explainable reasoning)

## API Endpoints

- `POST /api/v1/chat/message` - Send a message to the chat assistant
- `GET /api/v1/chat/history/{chat_id}` - Get chat history
- `POST /api/v1/documents/upload` - Upload a document
- `POST /api/v1/documents/upload/scanned` - Upload and process scanned document
- `GET /api/v1/documents/process/{document_id}` - Process a document
- `POST /api/v1/judgment/predict` - Predict judgment outcome
- `POST /api/v1/document-generation/generate` - Generate legal document
- `GET /api/v1/document-generation/generated/{document_id}` - Download document

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Download language models:
   ```bash
   python download_model.py
   ```

3. Install spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Start optional services (for advanced features):
   ```bash
   # Redis for metadata storage
   docker run -d -p 6379:6379 redis:alpine
   
   # Neo4j for knowledge graph
   docker run -d -p 7474:7474 -p 7687:7687 neo4j:latest
   ```

5. Start the application:
   ```bash
   ./start.sh
   ```

## Testing

- `test_chat.py` - Test chat functionality
- `test_slm.py` - Test SLM inference
- `test_vector_store.py` - Test FAISS vector store