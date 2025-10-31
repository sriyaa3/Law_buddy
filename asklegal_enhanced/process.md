# AskLegal Enhanced - Development Process Log

## Project Overview
**AskLegal Enhanced** is an AI-powered legal assistant platform specializing in MSME (Micro, Small, and Medium Enterprises) legal matters in India. The system combines local SLMs, Gemini LLM, and custom calculation engines to provide accurate legal guidance.

---

## Current Architecture (Updated: August 2025)

### System Components

#### 1. **Model Management System**
The system uses a **three-tier model architecture**:

##### A. Small Language Model (SLM) - Primary for Simple Queries
- **Location**: `/app/asklegal_enhanced/app/slm/`
- **Engine**: `hf_engine.py` (Hugging Face Inference API)
- **Fallback**: Rule-based intelligent responses
- **Use Cases**:
  - Simple informational queries about MSME
  - General legal guidance
  - Quick reference questions
  - Domain-specific MSME topics

##### B. Large Language Model (LLM) - For Complex Reasoning & Calculations
- **Location**: `/app/asklegal_enhanced/app/slm/gemini_engine.py`
- **Provider**: Google Gemini Pro
- **Configuration**: Uses `GOOGLE_API_KEY` from environment
- **Use Cases**:
  - Complex tax calculations
  - Financial analysis
  - Detailed legal reasoning
  - Multi-step problem solving

##### C. Calculation Engine - For Precise Financial Computations
- **Location**: `/app/asklegal_enhanced/app/slm/calculation_engine.py`
- **Purpose**: Handles precise tax and financial calculations
- **Features**:
  - Tax rate management (Income Tax, GST, Professional Tax, TDS)
  - Financial data extraction from natural language
  - Step-by-step calculation methodology
  - Detailed breakdown formatting

#### 2. **Smart Routing System**
**Location**: `/app/asklegal_enhanced/app/slm/model_router.py`

The router intelligently decides which model to use based on:

1. **Query Type Detection**:
   - Calculation queries → Gemini LLM
   - Simple info queries → SLM
   - Complex reasoning → Gemini LLM

2. **Complexity Scoring**:
   - Query length
   - Complexity keywords
   - Legal domain terms
   - MSME relevance

3. **Dynamic Context Loading**:
   - Loads only relevant context based on query type
   - Reduces token usage
   - Improves response quality

**Routing Logic**:
```
Query → Is Calculation? 
    ├─ Yes → Gemini (with calculation prompt)
    └─ No → Calculate Complexity
        ├─ High Complexity → Gemini
        ├─ Medium Complexity + MSME Focus → SLM
        └─ Low Complexity → SLM
```

#### 3. **Document Generation System**
**Location**: `/app/asklegal_enhanced/app/documents/generator.py`

**Features**:
- Generates professional legal documents
- Supports 5 document types:
  1. Non-Disclosure Agreement (NDA)
  2. Employment Contract
  3. Service Agreement
  4. Loan Agreement
  5. Legal Notice

**API Endpoints**:
- `POST /api/v1/documents/generate` - Generate document
- `GET /api/v1/documents/templates` - List available templates
- `GET /api/v1/documents/generated/{document_id}` - Download document
- `GET /api/v1/documents/list` - List all generated documents

**Recent Fix**: Implemented proper document ID mapping system for reliable file serving

#### 4. **Chat System**
**Location**: `/app/asklegal_enhanced/app/api/api_v1/endpoints/chat.py`

**Features**:
- Hybrid retrieval (RAG) integration
- Privacy layer for sensitive queries
- Context-aware responses
- Chat history management

**Flow**:
```
User Query → Privacy Layer → Hybrid Retriever → Model Router → Response
```

---

## Recent Changes (August 2025)

### Phase 1: Smart Calculation & LLM Integration ✅

#### Created Files:
1. **`calculation_engine.py`** - Financial calculation engine
   - Tax calculation logic (Income Tax, GST, Professional Tax, TDS)
   - Financial data extraction using regex patterns
   - Step-by-step calculation methodology
   - Human-readable formatting

2. **`gemini_engine.py`** - Gemini LLM integration
   - Proper API configuration
   - Calculation-focused prompt generation
   - Error handling and fallback logic

#### Modified Files:
1. **`model_router.py`** - Enhanced routing logic
   - Added calculation query detection
   - Implemented smart routing to Gemini for calculations
   - Added dynamic context loading (reduces token usage)
   - Created minimal context extraction for specific query types
   - Removed old server LLM endpoint code

2. **`document_generation.py`** - Fixed document serving
   - Implemented document ID to file path mapping
   - Added proper file download functionality
   - Created document listing endpoint

### Key Improvements:

#### 1. Accurate Tax Calculations
**Before**: Generic responses about tax laws
**After**: Exact calculations with step-by-step methodology

Example query:
```
"A company has 1 crore turnover, 20 employees with salary 20 lpa, 
resources 50 lpa, rest miscellaneous. What taxes do I pay?"
```

Response includes:
- Exact tax amounts (Income Tax, GST, Professional Tax, TDS)
- Detailed breakdown of expenses
- Profit before and after tax
- Legal compliance requirements
- Tax-saving opportunities

#### 2. Dynamic Context Loading
**Before**: Always loads full MSME context (increases tokens, slows response)
**After**: Loads only relevant context based on query type

Benefits:
- Faster responses
- Lower token usage
- More focused answers
- Better accuracy

#### 3. Working Document Generation
**Before**: Documents generated but download link didn't work
**After**: Proper ID mapping system ensures reliable downloads

---

## Technical Specifications

### Tax Rates (FY 2024-25)
```python
Company Income Tax:
- Turnover < ₹400 Crore: 25%
- Turnover ≥ ₹400 Crore: 30%

GST: 18% (standard rate)
Professional Tax: ₹2,500/employee/year (average)
TDS on Salaries: 10% (average effective rate)
```

### Model Configuration
```python
SLM (Hugging Face):
- Model: google/flan-t5-large
- Temperature: 0.7
- Max Tokens: 512

Gemini LLM:
- Model: gemini-pro
- Temperature: 0.3 (calculations), 0.7 (reasoning)
- Max Tokens: 2048
```

### API Endpoints

#### Chat Endpoints
- `POST /api/v1/chat/message` - Send chat message
- `GET /api/v1/chat/history/{chat_id}` - Get chat history

#### Document Endpoints
- `POST /api/v1/documents/generate` - Generate document
- `GET /api/v1/documents/templates` - List templates
- `GET /api/v1/documents/generated/{document_id}` - Download
- `GET /api/v1/documents/list` - List all documents

---

## File Structure

```
/app/asklegal_enhanced/
├── app/
│   ├── slm/                           # Model engines
│   │   ├── engine.py                  # Base inference engine
│   │   ├── hf_engine.py              # Hugging Face engine
│   │   ├── gemini_engine.py          # Gemini LLM (NEW)
│   │   ├── calculation_engine.py     # Financial calculations (NEW)
│   │   ├── model_router.py           # Smart routing (UPDATED)
│   │   └── prompts/
│   │       └── msme_legal_prompt.py  # Prompt templates
│   ├── documents/
│   │   └── generator.py              # Document generation
│   ├── api/
│   │   └── api_v1/
│   │       └── endpoints/
│   │           ├── chat.py           # Chat endpoints
│   │           └── document_generation.py  # Doc endpoints (UPDATED)
│   ├── msme/
│   │   └── context/
│   │       └── workflow.py           # Business context collector
│   ├── models/
│   │   └── model_manager.py          # Privacy-aware model manager
│   ├── retrieval/
│   │   └── hybrid_retriever.py       # RAG system
│   └── privacy/
│       └── privacy_layer.py          # Privacy filtering
├── frontend/                          # React frontend
├── data/
│   └── generated_documents/           # Stored documents
└── process.md                         # This file
```

---

## Testing Guidelines

### 1. Test Calculation Queries
```
Query: "Company with 1 crore turnover, 20 employees, 
       20 lpa salary, 50 lpa resources. Calculate taxes."

Expected: Detailed breakdown with exact amounts
```

### 2. Test Simple Queries
```
Query: "What is MSME classification?"

Expected: Quick response from SLM without unnecessary calculations
```

### 3. Test Document Generation
```
1. Call POST /api/v1/documents/generate
2. Receive document_id
3. Call GET /api/v1/documents/generated/{document_id}
4. Verify file downloads
```

### 4. Test Gemini Availability
```python
from app.slm.gemini_engine import gemini_engine

if gemini_engine.is_available():
    print("✓ Gemini is configured")
else:
    print("✗ Check GOOGLE_API_KEY")
```

---

## Environment Variables Required

```bash
# Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here

# Application Settings
APP_PORT=8001
SECRET_KEY=your_secret_key
DEBUG=False

# Database
DATABASE_URL=sqlite:///./ai_law_buddy.db

# Optional: Redis, Neo4j
UPSTASH_REDIS_URL=
UPSTASH_REDIS_TOKEN=
NEO4J_URI=bolt://localhost:7687
```

---

## Future Enhancements

### Planned Features:
1. **Advanced Tax Planning Module**
   - Multi-year tax projections
   - Scenario analysis
   - Tax optimization strategies

2. **Industry-Specific Calculators**
   - Manufacturing cost analysis
   - Retail margin calculations
   - Service pricing models

3. **Enhanced Document Templates**
   - Partnership deeds
   - Shareholder agreements
   - IP licensing agreements

4. **Compliance Calendar**
   - Automated compliance reminders
   - Deadline tracking
   - Form filing assistance

5. **Legal Case Analysis**
   - Citation search
   - Precedent analysis
   - Judgment summaries

---

## System Architecture Diagram

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│   Privacy Layer             │
│   (Sensitivity Detection)   │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│   Hybrid Retriever (RAG)    │
│   (Context Extraction)      │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│   Model Router              │
│   (Smart Routing Decision)  │
└──────┬──────────────────────┘
       │
       ├──► Calculation Query? ──► Gemini LLM ───┐
       │                                          │
       ├──► Complex Query? ─────► Gemini LLM ───┤
       │                                          │
       └──► Simple Query? ──────► SLM ───────────┤
                                                  │
                                                  ▼
                                          ┌────────────┐
                                          │  Response  │
                                          └────────────┘
```

---

## Maintenance Notes

### Model Management:
1. **SLM (Hugging Face)**: Free tier, no maintenance required
2. **Gemini LLM**: Monitor API usage and costs
3. **Calculation Engine**: Update tax rates annually

### Document Templates:
- Review and update templates based on legal changes
- Add new templates as requested by users
- Ensure compliance with latest Indian laws

### Data Storage:
- Generated documents stored in `/data/generated_documents/`
- Implement cleanup policy for old documents
- Consider cloud storage for production

---

## Known Limitations

1. **Tax Calculations**: Simplified for general guidance, actual may vary
2. **SLM Quality**: Limited by Hugging Face free tier model capabilities
3. **Document Generation**: Basic templates, may need legal review
4. **Context Size**: Limited by model token limits

---

## Support & Resources

### Internal Documentation:
- `/app/asklegal_enhanced/README.md` - Setup instructions
- `/app/asklegal_enhanced/DEPLOYMENT.md` - Deployment guide

### External Resources:
- Gemini API: https://ai.google.dev/
- Hugging Face: https://huggingface.co/
- MSME Portal: https://udyamregistration.gov.in/

---

## Changelog

### Version 2.0 (August 2025)
- ✅ Added Gemini LLM integration
- ✅ Implemented calculation engine for tax computations
- ✅ Enhanced model router with smart routing
- ✅ Added dynamic context loading
- ✅ Fixed document generation and serving
- ✅ Improved accuracy for financial queries

### Version 1.0 (Previous)
- Initial release with SLM and basic features
- RAG integration
- Privacy layer
- Basic document generation

---

**Last Updated**: August 2025
**Maintained By**: AskLegal Development Team
**Status**: Active Development
