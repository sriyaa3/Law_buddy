# AskLegal Enhanced - Fully Working Version

## 🎯 What Changed

This version now uses **Hugging Face Inference API** (free tier) for intelligent responses instead of local model files.

### Key Improvements:
1. ✅ **Fixed port configuration** - Frontend and backend now communicate properly
2. ✅ **Integrated Hugging Face API** - High-quality AI responses using free models
3. ✅ **Intelligent fallback system** - Comprehensive MSME legal responses when API is unavailable
4. ✅ **Working chat interface** - Full end-to-end functionality
5. ✅ **No heavy model downloads** - Uses API instead of local models

## 🚀 Quick Start

### Option 1: Use the run script (Recommended)
```bash
cd /app/asklegal_enhanced
./run_app.sh
```

### Option 2: Manual start
```bash
cd /app/asklegal_enhanced
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📍 Access URLs

- **Frontend (Chat Interface)**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 🧪 Test the API

### Test Chat Endpoint:
```bash
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "What is MSME?", "chat_id": "test123"}'
```

### Test Health Endpoint:
```bash
curl http://localhost:8000/api/v1/health
```

## 💡 Features

### 1. AI-Powered Chat Assistant
- Specializes in MSME (Micro, Small, Medium Enterprise) legal matters
- Provides detailed answers on:
  - Business registration (Udyam, GST)
  - Compliance requirements
  - Employment and labour laws
  - Contracts and agreements
  - Intellectual property
  - Tax obligations
  - Financing options
  - Startup India benefits

### 2. Intelligent Response System
- **Primary**: Hugging Face API (Mistral-7B-Instruct model)
- **Backup**: Multiple fallback models
- **Offline Mode**: Comprehensive rule-based responses

### 3. Document Processing
- Upload and analyze legal documents
- Extract key information
- Get compliance recommendations

### 4. Document Generation
- Generate legal documents from templates
- NDAs, contracts, agreements
- Customizable based on business needs

## 🔧 Technical Architecture

### Backend
- **Framework**: FastAPI
- **AI Engine**: Hugging Face Inference API
- **Vector Store**: FAISS (for document retrieval)
- **Database**: SQLite (development)

### Frontend
- **Framework**: React
- **Styling**: Styled Components
- **API Client**: Axios

### Free Resources Used
- **Hugging Face Inference API** - Free tier for model inference
- **Mistral-7B-Instruct** - Open source LLM
- **FAISS** - Open source vector similarity search
- **SQLite** - Open source database

## 📊 API Endpoints

### Chat
- `POST /api/v1/chat/message` - Send chat message
- `GET /api/v1/chat/history/{chat_id}` - Get chat history

### Documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/process/{doc_id}` - Process document

### Document Generation
- `GET /api/v1/document-generation/templates` - Get templates
- `POST /api/v1/document-generation/generate` - Generate document

### MSME Services
- `POST /api/v1/msme/profile` - Create business profile
- `GET /api/v1/msme/profile/{user_id}` - Get business profile
- `GET /api/v1/msme/recommendations/{user_id}` - Get recommendations

### System
- `GET /api/v1/health` - Health check
- `GET /api/v1/docs` - API documentation

## 🔑 Optional: Hugging Face API Key

While the free tier works without authentication, you can optionally add your HuggingFace API key for:
- Higher rate limits
- Priority access
- Faster response times

```bash
export HUGGINGFACE_API_KEY="your_key_here"
```

Get a free key at: https://huggingface.co/settings/tokens

## 🛠️ Configuration

### Backend Port
Default: `8000`

To change, edit `/app/asklegal_enhanced/app/core/config.py` or use command line:
```bash
uvicorn app.main:app --host 0.0.0.0 --port YOUR_PORT
```

### Model Selection
Default: `mistralai/Mistral-7B-Instruct-v0.2`

To change, edit `/app/asklegal_enhanced/app/core/config.py`:
```python
HUGGINGFACE_MODEL: str = "your-preferred-model"
```

## 📝 Logs

View backend logs:
```bash
tail -f /tmp/asklegal_backend.log
```

## 🛑 Stop the Application

```bash
pkill -f 'uvicorn app.main:app'
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find the process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### API Not Responding
1. Check if server is running: `curl http://localhost:8000/api/v1/health`
2. Check logs: `tail -f /tmp/asklegal_backend.log`
3. Restart server: `./run_app.sh`

### Frontend Not Loading
1. Ensure frontend is built: `cd frontend && yarn build`
2. Restart backend to serve updated build

### HuggingFace API Errors
- The system automatically falls back to intelligent responses
- Check internet connectivity
- Optionally add HF API key for better reliability

## 📦 Dependencies

### Core Dependencies (Auto-installed)
- fastapi
- uvicorn
- pydantic
- pydantic-settings
- python-multipart
- python-dotenv
- requests
- sqlalchemy
- PyPDF2
- python-docx
- pillow

### Optional Dependencies
- sentence-transformers (for advanced retrieval)
- torch (for local ML features)
- spacy (for NLP features)

## 🎓 Usage Examples

### Basic Chat
```python
import requests

response = requests.post('http://localhost:8000/api/v1/chat/message', json={
    "message": "How do I register my MSME business?",
    "chat_id": "user123"
})

print(response.json()['response'])
```

### Document Upload
```python
import requests

with open('contract.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/v1/documents/upload', files=files)

print(response.json())
```

## 🌟 Next Steps

1. **Customize**: Modify prompts in `/app/asklegal_enhanced/app/slm/prompts/`
2. **Extend**: Add new endpoints in `/app/asklegal_enhanced/app/api/api_v1/endpoints/`
3. **Deploy**: Use the provided Dockerfile for production deployment
4. **Scale**: Add Redis caching, PostgreSQL database for production

## 📞 Support

For issues or questions:
1. Check logs first
2. Review API documentation at `/api/v1/docs`
3. Verify all dependencies are installed

## ✅ Status

- ✅ Backend: Running on port 8000
- ✅ Frontend: Built and served at /
- ✅ AI Engine: Hugging Face API integrated
- ✅ Chat API: Working
- ✅ Health Check: Passing
- ✅ Documentation: Available at /api/v1/docs

---

**Ready to use!** Access the application at http://localhost:8000
