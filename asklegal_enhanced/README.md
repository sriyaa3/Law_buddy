# AskLegal Enhanced - AI Legal Assistant for MSMEs

## Overview
AskLegal Enhanced is a comprehensive AI-powered legal assistant specifically designed for Micro, Small, and Medium Enterprises (MSMEs). This enhanced version features multimodal RAG capabilities, Small Language Models for local processing, and industry-specific legal knowledge.

## Key Features
- **Multimodal RAG**: Process text, PDFs, and scanned documents
- **SLM Integration**: Local inference with privacy preservation
- **MSME Focus**: Industry-specific legal compliance and recommendations
- **Document Processing**: Advanced parsing and entity extraction
- **Legal Chatbot**: Interactive legal assistant with context awareness
- **Judgment Prediction**: Case outcome analysis with precedents
- **Document Generation**: Template-based legal document creation

## Technical Architecture
- **Backend**: FastAPI (Python 3.12)
- **Frontend**: React with styled-components
- **Database**: SQLite (development), PostgreSQL (production)
- **Vector Store**: FAISS for similarity search
- **NLP**: spaCy, transformers, sentence-transformers
- **Document Processing**: pdfplumber, python-docx, pytesseract

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
asklegal_enhanced/
├── app/                 # Backend application
│   ├── api/            # REST API endpoints
│   ├── core/           # Configuration and settings
│   ├── document_processing/  # Document parsing and processing
│   ├── slm/            # Small Language Model integration
│   ├── vector_store/   # FAISS vector storage
│   └── ...
├── frontend/           # React frontend application
├── models/             # SLM model files
└── data/               # Legal knowledge base
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
