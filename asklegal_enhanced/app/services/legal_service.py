"""
Legal Service - Business Logic Layer
Handles all legal assistant operations
"""

import logging
import hashlib
from typing import Dict, Any, List, Optional
from app.models.model_manager import get_model_manager, SensitivityLevel
from app.graph_db.neo4j_manager import get_clause_graph_manager
from app.cache.redis_manager import get_redis_manager
from app.document_processing.enhanced_processor import get_document_processor
from app.retrieval.hybrid_retriever import get_hybrid_retriever

logger = logging.getLogger(__name__)

class LegalService:
    """
    Main service for legal assistant operations:
    - Query handling with RAG
    - Document processing and analysis
    - Document generation
    - Compliance checking
    - Judgment prediction
    """
    
    def __init__(self):
        self.model_manager = get_model_manager()
        self.redis_manager = get_redis_manager()
        self.clause_graph = get_clause_graph_manager()
        self.doc_processor = get_document_processor()
        self.retriever = get_hybrid_retriever()
    
    def handle_query(self, query: str, session_id: str) -> Dict[str, Any]:
        """
        Handle legal query with RAG and privacy-aware routing
        """
        try:
            # Check cache first
            query_hash = hashlib.md5(query.encode()).hexdigest()
            cached_result = self.redis_manager.get_cached_query_result(query_hash)
            
            if cached_result:
                logger.info("Returning cached result")
                cached_result['cached'] = True
                return cached_result
            
            # Retrieve relevant context
            context_docs = self.retriever.retrieve(query, top_k=5)
            
            # Build context string
            context_str = self._build_context_string(context_docs)
            
            # Build prompt
            prompt = self._build_legal_prompt(query, context_str)
            
            # Classify sensitivity and generate response
            sensitivity = self.model_manager.classify_sensitivity(query)
            response = self.model_manager.generate(prompt)
            
            # Extract sources
            sources = [
                {
                    'text': doc.get('text', '')[:200],
                    'source': doc.get('source', 'Legal Database'),
                    'relevance': doc.get('score', 0.0)
                }
                for doc in context_docs[:3]
            ]
            
            result = {
                'answer': response,
                'sources': sources,
                'sensitivity': sensitivity.value,
                'model': str(self.model_manager.route_query(sensitivity).value),
                'cached': False
            }
            
            # Cache result
            self.redis_manager.cache_query_result(query_hash, result, ttl=3600)
            
            return result
            
        except Exception as e:
            logger.error(f"Query handling error: {e}")
            return {
                'answer': f"I apologize, but I encountered an error processing your query: {str(e)}",
                'sources': [],
                'error': str(e)
            }
    
    def process_document(
        self,
        filepath: str,
        doc_id: str,
        session_id: str,
        filename: str
    ) -> Dict[str, Any]:
        """
        Process uploaded document
        """
        try:
            # Process document
            processed_doc = self.doc_processor.process_document(
                filepath, doc_id
            )
            
            # Store in clause graph
            self.clause_graph.create_document_node(
                doc_id,
                {
                    'filename': filename,
                    'uploaded_by': session_id,
                    'upload_date': str(datetime.now()),
                    **processed_doc.metadata
                }
            )
            
            # Create clause nodes
            for idx, clause in enumerate(processed_doc.clauses):
                self.clause_graph.create_clause_node(
                    clause_id=clause['id'],
                    doc_id=doc_id,
                    text=clause['text'],
                    clause_type=clause['type'],
                    position=idx
                )
                
                # Create entity nodes and links
                for entity in processed_doc.entities:
                    self.clause_graph.create_entity_node(
                        entity['text'],
                        entity['type']
                    )
                    self.clause_graph.link_clause_to_entity(
                        clause['id'],
                        entity['text']
                    )
            
            # Store metadata in Redis
            doc_metadata = {
                'doc_id': doc_id,
                'filename': filename,
                'session_id': session_id,
                'num_clauses': len(processed_doc.clauses),
                'num_entities': len(processed_doc.entities),
                'num_tables': len(processed_doc.tables),
                'text_length': len(processed_doc.text)
            }
            self.redis_manager.save_document_metadata(doc_id, doc_metadata)
            self.redis_manager.add_user_document(session_id, doc_id)
            
            # Index document for retrieval
            self.retriever.add_document(
                doc_id=doc_id,
                text=processed_doc.text,
                metadata=doc_metadata
            )
            
            return {
                'success': True,
                'doc_id': doc_id,
                'summary': {
                    'num_clauses': len(processed_doc.clauses),
                    'num_entities': len(processed_doc.entities),
                    'num_tables': len(processed_doc.tables),
                    'key_entities': processed_doc.entities[:10]
                }
            }
            
        except Exception as e:
            logger.error(f"Document processing error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Analyze document structure and relationships
        """
        try:
            # Get document structure from Neo4j
            structure = self.clause_graph.get_document_structure(doc_id)
            
            # Get metadata from Redis
            metadata = self.redis_manager.get_document_metadata(doc_id)
            
            return {
                'success': True,
                'structure': structure,
                'metadata': metadata
            }
            
        except Exception as e:
            logger.error(f"Document analysis error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_document(
        self,
        doc_type: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate legal document from template
        """
        try:
            templates = {
                'legal_notice': self._generate_legal_notice,
                'nda': self._generate_nda,
                'contract': self._generate_contract,
                'agreement': self._generate_agreement
            }
            
            if doc_type not in templates:
                return {
                    'success': False,
                    'error': f'Unknown document type: {doc_type}'
                }
            
            document = templates[doc_type](parameters)
            
            return {
                'success': True,
                'document': document,
                'type': doc_type
            }
            
        except Exception as e:
            logger.error(f"Document generation error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_compliance(
        self,
        industry: str,
        company_type: str
    ) -> Dict[str, Any]:
        """
        Check compliance requirements for industry and company type
        """
        try:
            # Define compliance requirements
            compliance_data = self._get_compliance_requirements(industry, company_type)
            
            return {
                'success': True,
                'industry': industry,
                'company_type': company_type,
                'requirements': compliance_data['requirements'],
                'checklists': compliance_data['checklists'],
                'recommendations': compliance_data['recommendations']
            }
            
        except Exception as e:
            logger.error(f"Compliance check error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_judgment(
        self,
        case_description: str,
        case_type: str
    ) -> Dict[str, Any]:
        """
        Predict case judgment outcome
        """
        try:
            # Use model to analyze case
            prompt = f\"\"\"Analyze the following legal case and predict the likely outcome.

Case Type: {case_type}
Case Description: {case_description}

Provide:
1. Likely outcome (favorable/unfavorable/uncertain)
2. Probability estimate
3. Key factors influencing the outcome
4. Relevant legal precedents
5. Recommendations

Analysis:\"\"\"
            
            analysis = self.model_manager.generate(prompt, max_tokens=1024)
            
            return {
                'success': True,
                'case_type': case_type,
                'analysis': analysis,
                'disclaimer': 'This is an AI-generated prediction and should not be considered legal advice.'
            }
            
        except Exception as e:
            logger.error(f\"Judgment prediction error: {e}\")
            return {
                'success': False,
                'error': str(e)
            }
    
    # Helper methods
    
    def _build_context_string(self, context_docs: List[Dict[str, Any]]) -> str:
        \"\"\"Build context string from retrieved documents\"\"\"
        if not context_docs:
            return \"No relevant legal context found.\"
        
        context_parts = []
        for idx, doc in enumerate(context_docs[:5], 1):
            text = doc.get('text', '')
            source = doc.get('source', 'Legal Database')
            context_parts.append(f\"[Source {idx}: {source}]\\n{text}\\n\")
        
        return \"\\n\".join(context_parts)
    
    def _build_legal_prompt(self, query: str, context: str) -> str:
        \"\"\"Build prompt for legal query\"\"\"
        return f\"\"\"You are an expert legal AI assistant specializing in Indian law. 
Provide accurate, helpful legal guidance based on the context provided.

Context from legal sources:
{context}

User Query: {query}

Instructions:
1. Answer based primarily on the provided context
2. Cite relevant sections or clauses
3. Be clear if information is not in the context
4. Provide practical advice for MSMEs and startups
5. Include relevant legal precedents if available

Answer:\"\"\"
    
    def _generate_legal_notice(self, params: Dict[str, Any]) -> str:
        \"\"\"Generate legal notice\"\"\"
        return f\"\"\"LEGAL NOTICE

To: {params.get('recipient_name', '[Recipient Name]')}
{params.get('recipient_address', '[Address]')}

From: {params.get('sender_name', '[Sender Name]')}
{params.get('sender_address', '[Address]')}

Date: {params.get('date', '[Date]')}

Subject: {params.get('subject', '[Subject]')}

Dear Sir/Madam,

{params.get('content', '[Notice content]')}

This notice is being sent to you under the provisions of applicable law.

You are hereby required to {params.get('demand', '[specific demand]')} within {params.get('timeframe', '30')} days from the receipt of this notice, failing which appropriate legal action will be initiated against you without further notice.

Please treat this matter with utmost urgency.

Yours sincerely,
{params.get('sender_name', '[Sender Name]')}
\"\"\"
    
    def _generate_nda(self, params: Dict[str, Any]) -> str:
        \"\"\"Generate Non-Disclosure Agreement\"\"\"
        return f\"\"\"NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement (\"Agreement\") is entered into on {params.get('date', '[Date]')}

BETWEEN:
{params.get('party1_name', '[Party 1]')} (\"Disclosing Party\")
AND
{params.get('party2_name', '[Party 2]')} (\"Receiving Party\")

1. CONFIDENTIAL INFORMATION
The parties agree that confidential information includes: {params.get('scope', '[define scope]')}

2. OBLIGATIONS
The Receiving Party agrees to:
- Maintain strict confidentiality
- Use information only for authorized purposes
- Not disclose to third parties without written consent

3. TERM
This Agreement shall remain in effect for {params.get('duration', '2')} years from the date of signing.

4. GOVERNING LAW
This Agreement shall be governed by the laws of India.

SIGNATURES:

Disclosing Party: _________________
Name: {params.get('party1_name', '[Party 1]')}
Date: _________________

Receiving Party: _________________
Name: {params.get('party2_name', '[Party 2]')}
Date: _________________
\"\"\"
    
    def _generate_contract(self, params: Dict[str, Any]) -> str:
        \"\"\"Generate general contract\"\"\"
        return f\"\"\"CONTRACT AGREEMENT

This Agreement is made on {params.get('date', '[Date]')}

BETWEEN:
{params.get('party1', '[Party 1]')}
AND
{params.get('party2', '[Party 2]')}

WHEREAS the parties wish to enter into an agreement for {params.get('purpose', '[purpose]')}

NOW THEREFORE, in consideration of the mutual covenants, the parties agree:

1. SCOPE OF WORK
{params.get('scope', '[Define scope of work]')}

2. PAYMENT TERMS
{params.get('payment', '[Payment terms]')}

3. TIMELINE
{params.get('timeline', '[Project timeline]')}

4. TERMINATION
Either party may terminate with {params.get('notice_period', '30')} days written notice.

5. GOVERNING LAW
This Agreement is governed by Indian law.

SIGNATURES:

Party 1: _________________
Date: _________________

Party 2: _________________
Date: _________________
\"\"\"
    
    def _generate_agreement(self, params: Dict[str, Any]) -> str:
        \"\"\"Generate general agreement\"\"\"
        return self._generate_contract(params)
    
    def _get_compliance_requirements(
        self,
        industry: str,
        company_type: str
    ) -> Dict[str, Any]:
        \"\"\"Get compliance requirements for industry and company type\"\"\"
        
        # Comprehensive compliance data
        compliance_db = {
            'technology': {
                'startup': {
                    'requirements': [
                        'Startup India Registration',
                        'GST Registration (if turnover > 20L)',
                        'Income Tax Registration',
                        'Professional Tax Registration',
                        'Data Protection Compliance',
                        'IT Act 2000 Compliance'
                    ],
                    'checklists': [
                        'Company incorporation documents',
                        'PAN and TAN registration',
                        'Bank account opening',
                        'Privacy policy and terms of service',
                        'Employee contracts',
                        'IP protection documents'
                    ],
                    'recommendations': [
                        'Register for Startup India benefits',
                        'Protect intellectual property early',
                        'Implement data protection measures',
                        'Maintain proper employee agreements',
                        'Regular compliance audits'
                    ]
                },
                'msme': {
                    'requirements': [
                        'MSME/Udyam Registration',
                        'GST Registration',
                        'Shop and Establishment License',
                        'Professional Tax Registration',
                        'ESI and PF Registration (if employees > 10)',
                        'IT Act 2000 Compliance'
                    ],
                    'checklists': [
                        'Udyam registration certificate',
                        'GST compliance',
                        'Employee statutory registrations',
                        'Annual returns filing',
                        'Tax deduction at source (TDS) compliance',
                        'Book keeping records'
                    ],
                    'recommendations': [
                        'Avail MSME benefits and subsidies',
                        'Maintain proper accounting records',
                        'File returns timely',
                        'Implement workplace safety measures',
                        'Get business insurance'
                    ]
                }
            },
            'manufacturing': {
                'msme': {
                    'requirements': [
                        'MSME Registration',
                        'Factory License',
                        'GST Registration',
                        'Pollution Control Board clearance',
                        'Fire Safety Certificate',
                        'Labor License',
                        'ESI and PF Registration'
                    ],
                    'checklists': [
                        'Factory Act compliance',
                        'Environmental clearances',
                        'Worker safety measures',
                        'Waste disposal compliance',
                        'Quality certifications (ISO)',
                        'Labor welfare compliance'
                    ],
                    'recommendations': [
                        'Regular safety audits',
                        'Maintain environmental compliance',
                        'Worker welfare programs',
                        'Quality management systems',
                        'Energy efficiency measures'
                    ]
                }
            },
            'retail': {
                'msme': {
                    'requirements': [
                        'Shop and Establishment License',
                        'GST Registration',
                        'FSSAI License (if food items)',
                        'Trade License',
                        'Professional Tax',
                        'Fire NOC'
                    ],
                    'checklists': [
                        'Business premises compliance',
                        'Product quality standards',
                        'Consumer protection compliance',
                        'Employee regulations',
                        'Tax compliance',
                        'Health and safety standards'
                    ],
                    'recommendations': [
                        'Digital payment compliance',
                        'Customer data protection',
                        'Regular stock audits',
                        'Employee training programs',
                        'Insurance coverage'
                    ]
                }
            }
        }
        
        # Get specific compliance or return default
        industry_data = compliance_db.get(industry.lower(), {})
        company_data = industry_data.get(company_type.lower(), {})
        
        if not company_data:
            # Return general compliance
            return {
                'requirements': [
                    'Business Registration',
                    'GST Registration',
                    'Income Tax Registration',
                    'Professional Tax Registration',
                    'Shop and Establishment License'
                ],
                'checklists': [
                    'Legal entity formation',
                    'Tax registrations',
                    'Employee compliance',
                    'Contract management',
                    'Record keeping'
                ],
                'recommendations': [
                    'Consult with legal advisor',
                    'Maintain proper documentation',
                    'Regular compliance reviews',
                    'Stay updated with regulatory changes'
                ]
            }
        
        return company_data

from datetime import datetime
