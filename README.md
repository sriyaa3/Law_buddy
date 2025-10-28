# AskLegal.ai - AI Legal Assistant for MSMEs

## Overview
AskLegal.ai is an advanced AI-powered legal assistant specifically designed for Micro, Small, and Medium Enterprises (MSMEs) in India. This comprehensive solution combines multimodal Retrieval-Augmented Generation (RAG), Small Language Models (SLMs), and domain-specific legal knowledge to provide accessible, privacy-preserving legal assistance.

## Key Features
- **Multimodal RAG**: Process text, PDFs, DOCX, and scanned documents
- **SLM Integration**: Local inference with privacy preservation using TinyLlama
- **MSME Focus**: Industry-specific legal compliance and recommendations
- **Document Processing**: Advanced parsing with entity and clause extraction
- **Legal Chatbot**: Interactive context-aware legal assistant
- **Judgment Prediction**: Case outcome analysis with legal precedents
- **Document Generation**: Template-based legal document creation
- **Compliance Management**: Industry-specific checklists and tracking

## Technical Architecture

### Backend (FastAPI - Python 3.12)
- **API Layer**: RESTful endpoints for all services
- **Document Processing**: pdfplumber, python-docx, pytesseract
- **NLP Engine**: spaCy, transformers, sentence-transformers
- **Vector Store**: FAISS for similarity search
- **Metadata Store**: Redis for fast lookups
- **Graph Database**: Neo4j for legal knowledge representation

### Frontend (React)
- **User Interface**: Modern, responsive design with styled-components
- **Chat Interface**: Interactive legal assistant
- **Document Management**: Upload, process, and generate legal documents
- **MSME Dashboard**: Industry-specific legal compliance tools
- **Judgment Analysis**: Case prediction and legal insights

### AI/ML Components
- **Small Language Model**: TinyLlama 1.1B (local inference)
- **Legal Embeddings**: InLegalBERT fine-tuned on Indian case law
- **Hybrid Retrieval**: BM25 + FAISS + Redis combination
- **Privacy Layer**: Sensitivity classification and data anonymization

## Prerequisites
- Python 3.12+
- Node.js 14+
- pip package manager

## Installation

1. Install backend requirements:
```bash
cd asklegal_enhanced
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
cd asklegal_enhanced
python start_app.py
```

2. Access the application:
- Frontend: http://localhost:8001
- API Documentation: http://localhost:8001/docs

## API Endpoints
- `POST /api/v1/chat/message` - Legal chat assistant
- `POST /api/v1/documents/upload` - Document processing
- `POST /api/v1/document-generation/generate` - Document generation
- `POST /api/v1/judgment/predict` - Judgment prediction
- `POST /api/v1/msme/profile` - MSME business profile

## Project Structure
```
.
├── asklegal_enhanced/
│   ├── app/                 # Backend application
│   │   ├── api/            # REST API endpoints
│   │   ├── core/           # Configuration and settings
│   │   ├── document_processing/  # Document parsing and processing
│   │   ├── slm/            # Small Language Model integration
│   │   ├── vector_store/   # FAISS vector storage
│   │   └── ...
│   ├── frontend/           # React frontend application
│   ├── models/             # SLM model files
│   └── data/               # Legal knowledge base
├── laws_json/              # Legal acts and regulations in JSON format
└── data/                   # Additional legal data and indexes
```

## Implementation Highlights

### Multimodal Data Ingestion
- PDF processing with layout awareness
- DOCX parsing with structure preservation
- OCR preprocessing for scanned documents
- Entity and clause extraction with spaCy

### Advanced RAG System
- Hybrid retrieval combining FAISS, Redis, and BM25
- Context window construction for generation
- Similarity search with fallback mechanisms
- Legal document indexing and metadata storage

### Privacy-Preserving SLM
- Local inference with TinyLlama 1.1B model
- Sensitivity classification for legal queries
- Data anonymization for sensitive information
- Model routing based on query complexity

### MSME-Specific Features
- Industry taxonomy with legal requirements
- Compliance checklists and recommendations
- Risk assessment tools
- Workflow automation for legal processes

## Documentation
- [Implementation Completion Summary](IMPLEMENTATION_COMPLETION_SUMMARY.md)
- [Project Clean Structure](PROJECT_CLEAN_STRUCTURE.md)
- [Enhanced README](asklegal_enhanced/README.md)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Legal knowledge base derived from Indian legal acts and regulations
- InLegalBERT model for legal domain embeddings
- TinyLlama for efficient local language modeling
- Open source libraries and frameworks that made this project possible