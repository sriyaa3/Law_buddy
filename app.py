"""
AI Law Buddy - Flask Application
Main entry point for the Flask web application
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

# Import managers
from asklegal_enhanced.app.core.config_enhanced import settings
from asklegal_enhanced.app.models.model_manager import get_model_manager
from asklegal_enhanced.app.graph_db.neo4j_manager import get_clause_graph_manager
from asklegal_enhanced.app.cache.redis_manager import get_redis_manager
from asklegal_enhanced.app.document_processing.enhanced_processor import get_document_processor
from asklegal_enhanced.app.retrieval.hybrid_retriever import get_hybrid_retriever
from asklegal_enhanced.app.services.legal_service import LegalService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)
app.secret_key = settings.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = settings.MAX_UPLOAD_SIZE
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

# Initialize services
try:
    model_manager = get_model_manager()
    redis_manager = get_redis_manager()
    clause_graph_manager = get_clause_graph_manager()
    document_processor = get_document_processor()
    retriever = get_hybrid_retriever()
    legal_service = LegalService()
    logger.info("✓ All services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    raise

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        redis_manager.create_session(session['session_id'])
    return session['session_id']

# Routes

@app.route('/')
def index():
    """Home page"""
    session_id = get_session_id()
    return render_template('index.html', 
        project_name=settings.PROJECT_NAME,
        available_models=model_manager.get_available_models()
    )

@app.route('/chat')
def chat():
    """Chat interface"""
    session_id = get_session_id()
    # Get chat history
    history = redis_manager.get_chat_history(session_id, limit=50)
    return render_template('chat.html', 
        history=history,
        session_id=session_id
    )

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        session_id = get_session_id()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Save user message
        redis_manager.save_message(session_id, 'user', query)
        
        # Get response from legal service
        response = legal_service.handle_query(
            query=query,
            session_id=session_id
        )
        
        # Save assistant response
        redis_manager.save_message(
            session_id, 
            'assistant', 
            response['answer'],
            metadata={
                'model': response.get('model'),
                'sources': response.get('sources', [])
            }
        )
        
        # Increment stats
        redis_manager.increment_query_count()
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/documents')
def documents():
    """Document management page"""
    session_id = get_session_id()
    user_docs = redis_manager.list_user_documents(session_id)
    
    # Get metadata for each document
    docs_with_metadata = []
    for doc_id in user_docs:
        metadata = redis_manager.get_document_metadata(doc_id)
        if metadata:
            docs_with_metadata.append(metadata)
    
    return render_template('documents.html', documents=docs_with_metadata)

@app.route('/api/documents/upload', methods=['POST'])
def upload_document():
    """Upload and process document"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        doc_id = str(uuid.uuid4())
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{doc_id}_{filename}")
        file.save(filepath)
        
        # Process document
        session_id = get_session_id()
        result = legal_service.process_document(
            filepath=filepath,
            doc_id=doc_id,
            session_id=session_id,
            filename=filename
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents/<doc_id>/analyze', methods=['GET'])
def analyze_document(doc_id):
    """Analyze document structure"""
    try:
        analysis = legal_service.analyze_document(doc_id)
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/document-generation')
def document_generation():
    """Document generation page"""
    return render_template('document_generation.html')

@app.route('/api/generate-document', methods=['POST'])
def generate_document():
    """Generate legal document"""
    try:
        data = request.get_json()
        doc_type = data.get('type')
        params = data.get('parameters', {})
        
        result = legal_service.generate_document(doc_type, params)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Generation error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/compliance')
def compliance():
    """Compliance monitoring page"""
    return render_template('compliance.html')

@app.route('/api/compliance/check', methods=['POST'])
def check_compliance():
    """Check compliance requirements"""
    try:
        data = request.get_json()
        industry = data.get('industry')
        company_type = data.get('company_type')
        
        result = legal_service.check_compliance(industry, company_type)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Compliance check error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/judgment-prediction')
def judgment_prediction():
    """Judgment prediction page"""
    return render_template('judgment_prediction.html')

@app.route('/api/predict-judgment', methods=['POST'])
def predict_judgment():
    """Predict case judgment"""
    try:
        data = request.get_json()
        case_description = data.get('description')
        case_type = data.get('type')
        
        result = legal_service.predict_judgment(case_description, case_type)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear chat history"""
    try:
        session_id = get_session_id()
        redis_manager.clear_chat_history(session_id)
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Clear history error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': model_manager.get_available_models(),
        'redis_connected': redis_manager.is_connected(),
        'neo4j_connected': clause_graph_manager.driver is not None
    })

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=settings.APP_PORT,
        debug=settings.DEBUG
    )
