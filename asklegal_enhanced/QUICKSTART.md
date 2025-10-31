# AskLegal Enhanced - Quick Start Guide

## 🎯 What's New (August 2025)

Your AskLegal system has been upgraded with:

### ✅ **Smart Tax Calculator**
- Precise financial calculations
- Step-by-step methodology
- Detailed tax breakdown

### ✅ **Gemini LLM Integration**
- Accurate responses for complex queries
- Better reasoning for calculations
- Fallback system for reliability

### ✅ **Dynamic Context Loading**
- Faster responses
- Lower token usage
- More focused answers

### ✅ **Fixed Document Generation**
- Proper file serving
- Reliable downloads
- Document ID tracking

---

## 🚀 Quick Setup

### 1. **Configure Gemini API Key**

Get your free Gemini API key:
1. Go to: https://ai.google.dev/
2. Click "Get API Key"
3. Create a key (free tier available)

Add to your environment:
```bash
export GOOGLE_API_KEY="your_gemini_api_key_here"
```

Or create a `.env` file in `/app/asklegal_enhanced/`:
```bash
cp .env.template .env
# Edit .env and add your GOOGLE_API_KEY
```

### 2. **Install Dependencies** (Already Done)

```bash
pip install google-generativeai
```

### 3. **Test the System**

Run the test scripts:

```bash
# Test calculation engine
python test_calculation.py

# Test routing logic
python test_routing.py
```

---

## 📊 Example Queries

### **Tax Calculation**
```
Query: "A company has 1 crore turnover, 20 employees with 20 lpa salary, 
        50 lpa resources, rest miscellaneous. Calculate taxes."

Response: Detailed breakdown with exact amounts, legal advice, compliance requirements
```

### **Simple MSME Query**
```
Query: "What is MSME classification?"

Response: Quick, focused answer from SLM
```

### **Complex Legal Query**
```
Query: "Explain GST compliance for manufacturing MSMEs"

Response: Detailed explanation from Gemini LLM
```

---

## 🏗️ System Architecture

```
User Query
    ↓
Privacy Layer (Sensitivity Check)
    ↓
Hybrid Retriever (Context Extraction)
    ↓
Model Router (Smart Decision)
    ├─→ Calculation Query? → Gemini LLM → Precise Answer
    ├─→ Complex Query? → Gemini LLM → Detailed Analysis
    └─→ Simple Query? → SLM → Quick Response
```

---

## 📝 Document Generation

### Available Templates:
1. **NDA** - Non-Disclosure Agreement
2. **Employment Contract**
3. **Service Agreement**
4. **Loan Agreement**
5. **Legal Notice**

### API Usage:

```python
# Generate document
POST /api/v1/documents/generate
{
    "template_type": "nda",
    "details": {
        "disclosing_party": "Company A",
        "receiving_party": "Company B",
        "effective_date": "January 1, 2025",
        "term": "2 years"
    }
}

# Response includes document_id
# Download using: GET /api/v1/documents/generated/{document_id}
```

---

## 🧪 Testing

### Test Files Created:
1. **`test_calculation.py`** - Test tax calculation engine
2. **`test_routing.py`** - Test smart routing logic

### Manual Testing:

```bash
# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8001

# Test with curl
curl -X POST http://localhost:8001/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Company with 1cr turnover, 20 employees, 20 lpa salary, 50 lpa resources. Calculate taxes",
    "chat_id": "test123"
  }'
```

---

## 📁 Important Files

### New Files:
- `/app/slm/calculation_engine.py` - Financial calculation logic
- `/app/slm/gemini_engine.py` - Gemini LLM integration
- `/process.md` - Development log and architecture
- `.env.template` - Environment configuration template

### Modified Files:
- `/app/slm/model_router.py` - Smart routing with calculation detection
- `/app/api/api_v1/endpoints/document_generation.py` - Fixed file serving
- `requirements.txt` - Added google-generativeai

---

## 🔧 Configuration

### Environment Variables:

```bash
# Required
GOOGLE_API_KEY=your_key_here

# Optional (defaults provided)
APP_PORT=8001
DEBUG=False
TEMPERATURE=0.7
MAX_TOKENS=512
```

### Tax Rates (FY 2024-25):

The calculation engine uses current Indian tax rates:
- **Income Tax**: 25% (turnover < ₹400 Cr), 30% (turnover ≥ ₹400 Cr)
- **GST**: 18% (standard rate)
- **Professional Tax**: ₹2,500/employee/year
- **TDS on Salaries**: 10% (average)

---

## 💡 How It Works

### Calculation Queries:
1. Router detects calculation keywords and numbers
2. Extracts financial data (turnover, expenses, employees)
3. Routes to Gemini LLM (if available) or Calculation Engine
4. Returns detailed breakdown with legal advice

### Simple Queries:
1. Router detects MSME keywords and low complexity
2. Uses SLM for fast, efficient responses
3. Loads only relevant context (dynamic)

### Complex Queries:
1. Router detects high complexity or reasoning needs
2. Routes to Gemini LLM for detailed analysis
3. Includes comprehensive context

---

## 🐛 Troubleshooting

### Gemini Not Available?
```
Error: "Google API key not found"
Solution: Set GOOGLE_API_KEY environment variable
```

### Calculation Not Working?
```
Check: Is query detected as calculation?
Run: python test_routing.py
Look for: "Routed to: CALC" or "calculation query detected"
```

### Documents Not Downloading?
```
Check: Document ID mapping exists
Run: curl http://localhost:8001/api/v1/documents/list
```

---

## 📚 Resources

- **Process Log**: `/app/asklegal_enhanced/process.md`
- **Gemini Docs**: https://ai.google.dev/
- **MSME Portal**: https://udyamregistration.gov.in/
- **Tax Info**: https://www.incometax.gov.in/

---

## 🎯 Next Steps

1. **Add Gemini API Key** (if not done)
2. **Test with example query**
3. **Try document generation**
4. **Explore different query types**

---

## 📞 Support

For issues or questions:
1. Check `process.md` for detailed architecture
2. Run test scripts to diagnose
3. Review logs in `/var/log/` (if deployed)

---

**Version**: 2.0 (August 2025)
**Status**: Production Ready (with Gemini API key)
**Open Source**: Yes
**Free**: Yes (uses free Gemini tier)
