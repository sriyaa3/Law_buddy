# AskLegal Enhanced - AI Legal Assistant for MSMEs

## Overview
AskLegal Enhanced is an advanced AI Legal Assistant specifically designed for Micro, Small, and Medium Enterprises (MSMEs) in India. This system implements a complete multimodal RAG pipeline with privacy-preserving Small Language Models (SLMs) and advanced legal document processing capabilities.

## Key Features

### 1. Multimodal Data Ingestion
- **PDF Processing**: Advanced parsing with pdfplumber and unstructured library
- **DOCX Processing**: Layout-aware document parsing
- **OCR Support**: Tesseract OCR for scanned documents
- **Image Processing**: LayoutLMv3 for document structure retention
- **Text Segmentation**: Clean, clause-aware text blocks with metadata

### 2. Clause-Graph Construction
- **Legal NER**: spaCy-based entity extraction for legal terms
- **Clause Detection**: Pattern-based clause identification
- **Relationship Mapping**: Dependency parsing for clause relationships
- **Neo4j Integration**: Graph database for complex legal knowledge representation

### 3. Embeddings & Indexing
- **InLegalBERT**: Fine-tuned on Indian case law for legal embeddings
- **FAISS Vector Store**: Fast similarity search for document retrieval
- **Redis Metadata Store**: Fast metadata lookup and filtering
- **Hybrid Retrieval**: BM25 + FAISS + Redis for comprehensive search

### 4. Retrieval Engine
- **Multi-source Retrieval**: Combined vector, keyword, and metadata search
- **Re-ranking**: Weighted scoring for optimal result ordering
- **Context-aware Search**: Document structure and clause relationships
- **Fast Lookup**: Redis-based metadata filtering

### 5. RAG Combiner & Privacy Layer
- **Context Windowing**: Structured context assembly for legal reasoning
- **Privacy Classification**: Automatic sensitivity detection
- **Data Anonymization**: Redaction of sensitive information
- **Local Processing**: Privacy-preserving query routing

### 6. Model Integration
- **Small Language Models**: Phi-3 and TinyLlama for local processing
- **Large Language Models**: Mistral 7B for complex reasoning (server-based)
- **Intelligent Routing**: Query complexity-based model selection
- **Fallback Mechanisms**: Graceful degradation to available models

### 7. Downstream Applications
- **Legal Document Generator**: Template-based contracts and notices
- **Chatbot Interface**: Interactive legal assistance with citations
- **Judgment Predictor**: Outcome probability with explainable reasoning
- **Compliance Assistant**: Industry-specific regulatory guidance

## System Architecture

```
User Interface
    ↓
API Layer (FastAPI)
    ↓
Privacy Layer → Local SLM (Phi-3) ↔ Server LLM (Mistral 7B)
    ↓
Hybrid Retriever ←→ FAISS + Redis + BM25
    ↓
Knowledge Graph (Neo4j) ←→ Document Processor
    ↓
Multimodal Ingestion (PDF/DOCX/OCR) → InLegalBERT Embeddings
```

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Language Models**:
   ```bash
   python download_model.py
   ```

3. **Install spaCy Model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Start Services** (Optional for advanced features):
   ```bash
   # Redis for metadata storage
   docker run -d -p 6379:6379 redis:alpine
   
   # Neo4j for knowledge graph
   docker run -d -p 7474:7474 -p 7687:7687 neo4j:latest
   ```

## Usage

1. **Start the Application**:
   ```bash
   ./start.sh
   ```

2. **Access the Interface**:
   - Web Interface: http://localhost:8006
   - API Documentation: http://localhost:8006/docs

## Getting the Chatbot to Work

The chatbot uses Small Language Models (SLMs) for privacy-preserving legal assistance. To get it working:

1. **Download a model** (recommended for full functionality):
   ```bash
   python download_model.py
   ```
   This will download the lightweight TinyLlama model (700MB) which is sufficient for basic legal queries.

2. **Without a downloaded model** (fallback mode):
   The chatbot will still work with pre-programmed responses for common MSME legal queries.

## API Endpoints

### Chat
- `POST /api/v1/chat/message` - Legal chat assistance
- `GET /api/v1/chat/history/{chat_id}` - Chat history

### Document Processing
- `POST /api/v1/documents/upload` - Upload and process documents
- `POST /api/v1/documents/upload/scanned` - Process scanned documents
- `GET /api/v1/documents/process/{document_id}` - Document analysis

### Judgment Prediction
- `POST /api/v1/judgment/predict` - Predict case outcomes

### Document Generation
- `POST /api/v1/document-generation/generate` - Generate legal documents
- `GET /api/v1/document-generation/generated/{document_id}` - Download documents

## Testing

Run the test suite:
```bash
python test_chat_simple.py
python test_slm.py
python test_vector_store.py
```

## Privacy & Security

- **Local Processing**: Sensitive queries processed on-device
- **Data Anonymization**: Automatic redaction of personal information
- **No External APIs**: All processing done locally by default
- **Compliance**: Designed for Indian legal and privacy requirements

## Customization for MSMEs

- **Industry-specific Knowledge**: Manufacturing, retail, services, etc.
- **Regulatory Compliance**: GST, labor laws, licensing requirements
- **Business Context**: Tailored advice based on business size and type
- **Workflow Automation**: Document generation and compliance tracking