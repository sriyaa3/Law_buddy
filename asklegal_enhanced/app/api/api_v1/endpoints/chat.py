from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
import os
from app.core.config import settings
from app.slm.model_router import model_router
from app.retrieval.hybrid_retriever import hybrid_retriever
from app.privacy.privacy_layer import privacy_layer
from app.document_processing.embedders import text_embedder

router = APIRouter()

# In-memory storage for development
chat_storage: Dict[str, dict] = {}

# Load legal knowledge base
def load_legal_knowledge():
    """Load legal knowledge from JSON files"""
    knowledge_base = {}
    
    # Path to laws_json directory
    laws_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "laws_json")
    
    if os.path.exists(laws_dir):
        for filename in os.listdir(laws_dir):
            if filename.endswith(".json"):
                with open(os.path.join(laws_dir, filename), "r") as f:
                    try:
                        knowledge_base[filename] = json.load(f)
                    except:
                        pass
    
    return knowledge_base

# Load knowledge base
legal_knowledge = load_legal_knowledge()

class ChatMessage(BaseModel):
    message: str
    chat_id: str

class ChatResponse(BaseModel):
    response: str
    source: str

def generate_legal_response(user_message: str, chat_id: str) -> tuple:
    """
    Generate a legal response based on user message using enhanced RAG and model routing
    """
    response = ""
    source = "GEN"
    
    try:
        # Apply privacy layer
        sensitivity = privacy_layer.classify_query_sensitivity(user_message)
        
        # Apply privacy measures if needed
        if sensitivity in [privacy_layer.QuerySensitivity.SENSITIVE, privacy_layer.QuerySensitivity.HIGHLY_SENSITIVE]:
            processed_message = privacy_layer.anonymize_text(user_message)
            print(f"Applied privacy measures to sensitive query")
        else:
            processed_message = user_message
        
        # Retrieve relevant context using hybrid retrieval
        search_results = hybrid_retriever.retrieve(processed_message, top_k=5)
        
        # Build context from search results
        context = ""
        if search_results:
            context = "Relevant legal information:\n"
            for i, result in enumerate(search_results):
                context += f"{i+1}. {result['content'][:300]}...\n"
            context += "\n"
            source = "RAG"
        else:
            source = "GEN"
        
        # Create prompt for the model
        prompt = f"""You are an AI Legal Assistant specializing in MSME (Micro, Small, and Medium Enterprises) legal matters in India. 
        Use the following context to answer the question accurately:

        Context: {context}

        Question: {processed_message}

        Provide a detailed, accurate response based on the context and your knowledge of Indian MSME laws and regulations.
        If the context doesn't contain relevant information, use your general knowledge to provide helpful information.
        Keep your response focused on MSME legal matters and avoid speculation.
        """
        
        # Generate response using model router (SLM + RAG)
        response = model_router.generate_response(processed_message, context)
        
        # If we get an error response, provide a fallback
        if not response or "Error:" in response or response.strip() == "":
            # Fallback response with basic legal information
            response = _get_fallback_response(processed_message)
            source = "FALLBACK"
            
    except Exception as e:
        print(f"Error in generating legal response: {e}")
        # Provide fallback response on error
        response = _get_fallback_response(user_message)
        source = "FALLBACK"
    
    return response, source

def _get_fallback_response(query: str) -> str:
    """
    Provide fallback responses for common MSME legal queries
    
    Args:
        query (str): User query
        
    Returns:
        str: Fallback response
    """
    query_lower = query.lower()
    
    if ("what is" in query_lower or "define" in query_lower) and ("msme" in query_lower or "micro small medium enterprise" in query_lower):
        return "MSME stands for Micro, Small, and Medium Enterprises. In India, MSMEs are classified based on investment in plant and machinery/equipment and annual turnover:\n\nMicro Enterprise: Investment up to ₹1 crore and turnover up to ₹5 crore\nSmall Enterprise: Investment up to ₹10 crore and turnover up to ₹50 crore\nMedium Enterprise: Investment up to ₹50 crore and turnover up to ₹250 crore\n\nMSMEs play a crucial role in the Indian economy, contributing significantly to GDP, employment, and exports."
    
    elif "gst" in query_lower:
        return "Goods and Services Tax (GST) is a comprehensive indirect tax levied on the supply of goods and services in India. MSMEs with turnover exceeding ₹40 lakhs (₹10 lakhs for Northeastern states) must register for GST. Benefits for MSMEs include composition scheme (lower tax rates) and delayed payment provisions."
    
    elif "startup" in query_lower and "india" in query_lower:
        return "Startup India is a government initiative to build a strong ecosystem for nurturing innovation and startups. Eligible startups can avail benefits like tax exemptions (3 years), simplified compliance, access to funds, incubation centers, and IPR facilitation. MSMEs can also register as startups if they meet the criteria."
    
    elif "labour" in query_lower or "employee" in query_lower:
        return "MSMEs must comply with various labour laws including Factories Act, Minimum Wages Act, ESIC, PF, and Shops & Establishments Act. Recent reforms have simplified compliance through the Shram Suvidha Portal. Businesses with more than 20 employees must have formal contracts and maintain statutory registers."
    
    elif "ip" in query_lower or "intellectual property" in query_lower:
        return "Intellectual Property protection includes trademarks, copyrights, and patents. MSMEs should register their brand names, logos, and innovations. Copyright automatically protects original works, while trademarks and patents require registration."
    
    elif "compliance" in query_lower:
        return "MSME compliance requirements vary by industry. Common requirements include GST registration, Shops & Establishments registration, professional tax registration, and annual filings. Manufacturing units may need additional licenses like factory licenses."
    
    elif "finance" in query_lower or "loan" in query_lower or "credit" in query_lower:
        return "MSMEs can access various financing options including bank loans, government schemes, and alternative financing. Key government schemes include MUDRA Yojana (loans up to ₹10 lakh), CGTMSE (credit guarantee), and SIDBI initiatives. The MSME Samadhaan portal helps with delayed payment issues."
    
    elif "registration" in query_lower or "udyog aadhar" in query_lower:
        return "MSME registration is done through the Udyam Registration portal (udyamregistration.gov.in). Benefits include lower interest rates on loans, tax incentives, electricity tariff subsidies, and easier access to government tenders. The registration is based on Aadhaar and is free of cost."
    
    elif "tax" in query_lower or "income tax" in query_lower:
        return "MSMEs can opt for presumptive taxation under Section 44AD (8% of turnover) if turnover is less than ₹2 crores. Regular taxation applies for higher turnovers with deductions for business expenses. MSMEs can also claim deductions under Section 80JJAA for new employee hiring."
    
    elif "contract" in query_lower or "agreement" in query_lower:
        return "Essential contracts for MSMEs include employment agreements, vendor/supplier contracts, client agreements, and partnership deeds. Key elements include scope of work, payment terms, delivery timelines, dispute resolution mechanisms, and termination clauses. Always have legal review for significant contracts."
    
    elif "insurance" in query_lower:
        return "Important insurance for MSMEs include:\n1. General Liability Insurance\n2. Property Insurance\n3. Professional Liability Insurance\n4. Workers' Compensation\n5. Cyber Insurance\n6. Directors and Officers (D&O) Insurance\nGovernment schemes like PMJJBY and PMSBY provide affordable life insurance."
    
    elif "export" in query_lower or "import" in query_lower:
        return "MSMEs engaged in export/import must comply with FEMA regulations, obtain IEC code, and follow customs procedures. Benefits include duty drawbacks, export promotion capital goods scheme, and focus market scheme. EPCG scheme allows import of capital goods at concessional rates."
    
    else:
        return "I'm currently unable to generate a detailed response. Please try rephrasing your question or ask about specific MSME legal topics like:\n- MSME definition and classification\n- GST registration and compliance\n- Labour laws and employee contracts\n- Intellectual property protection\n- Business registration (Udyam/Udyog Aadhar)\n- Finance and loan options\n- Tax obligations and benefits\n- Export/import regulations\n- Insurance requirements\n- Startup India benefits"

@router.post("/message", response_model=ChatResponse)
async def chat_message(chat_message: ChatMessage):
    """
    Handle chat messages and generate legal responses
    """
    try:
        # Generate response
        response_text, source = generate_legal_response(chat_message.message, chat_message.chat_id)
        
        # Store in chat history
        if chat_message.chat_id not in chat_storage:
            chat_storage[chat_message.chat_id] = {
                "messages": []
            }
        
        chat_storage[chat_message.chat_id]["messages"].append({
            "role": "user",
            "content": chat_message.message
        })
        
        chat_storage[chat_message.chat_id]["messages"].append({
            "role": "assistant",
            "content": response_text,
            "source": source
        })
        
        return ChatResponse(response=response_text, source=source)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")

@router.get("/history/{chat_id}")
async def get_chat_history(chat_id: str):
    """
    Get chat history for a specific chat
    """
    if chat_id in chat_storage:
        return chat_storage[chat_id]["messages"]
    else:
        return []
