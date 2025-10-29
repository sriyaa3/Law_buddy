#!/bin/bash
# Quick verification script to check all components

echo "========================================"
echo "AskLegal Enhanced - System Verification"
echo "========================================"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f "setup_models.py" ]; then
    echo -e "${RED}Error: Please run from /app/asklegal_enhanced directory${NC}"
    exit 1
fi

echo "1. Checking models..."
if [ -f "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" ]; then
    echo -e "  ${GREEN}✓${NC} TinyLlama model found"
else
    echo -e "  ${RED}✗${NC} TinyLlama model missing"
fi

if [ -d "models/embeddings" ]; then
    echo -e "  ${GREEN}✓${NC} Embedding models directory exists"
else
    echo -e "  ${YELLOW}⚠${NC} Embedding models directory missing"
fi

echo ""
echo "2. Checking database..."
if [ -f "asklegal.db" ]; then
    echo -e "  ${GREEN}✓${NC} Database file exists"
else
    echo -e "  ${RED}✗${NC} Database not initialized"
fi

echo ""
echo "3. Checking vector store..."
if [ -f "data/legal_documents.index" ]; then
    echo -e "  ${GREEN}✓${NC} FAISS index exists"
else
    echo -e "  ${YELLOW}⚠${NC} Vector store not initialized"
fi

echo ""
echo "4. Checking backend service..."
if sudo supervisorctl status asklegal_backend | grep -q "RUNNING"; then
    echo -e "  ${GREEN}✓${NC} Backend is running"
    
    # Test health endpoint
    if curl -s -f http://localhost:8001/api/v1/health > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Health endpoint responding"
    else
        echo -e "  ${YELLOW}⚠${NC} Health endpoint not responding"
    fi
else
    echo -e "  ${RED}✗${NC} Backend is not running"
    echo "    Run: sudo supervisorctl start asklegal_backend"
fi

echo ""
echo "5. Checking frontend build..."
if [ -d "frontend/build" ]; then
    echo -e "  ${GREEN}✓${NC} Frontend build exists"
else
    echo -e "  ${YELLOW}⚠${NC} Frontend not built (optional)"
    echo "    Build with: cd frontend && npm run build"
fi

echo ""
echo "========================================"
echo "System Verification Complete"
echo "========================================"
echo ""
echo "Access the application:"
echo "  - Frontend: http://localhost:8001"
echo "  - API Docs: http://localhost:8001/docs"
echo "  - Health:   http://localhost:8001/api/v1/health"
echo ""
