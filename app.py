import os
import logging
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory
try:
    from views.chatbotLegalv2 import process_input, create_new_chat, get_chat_list, load_chat
except Exception as e:
    print(f"❌ Failed to import chatbotLegalv2: {e}", file=sys.stderr)
    raise
try:
    from views.judgmentPred import extract_text_from_file, predict_verdict
except Exception as e:
    print(f"❌ Failed to import judgementPred: {e}", file=sys.stderr)
    raise
try:
    from views.docGen import generate_legal_document
except Exception as e:
    print(f"❌ Failed to import docGen: {e}", file=sys.stderr)
    raise
    
print("🚀 Starting Flask app...", file=sys.stderr)

app = Flask(__name__)

# Clear any existing handlers
for handler in app.logger.handlers:
    app.logger.removeHandler(handler)

# Configure Flask logger to output INFO level to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
console_handler.setFormatter(formatter)

app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    raw_chat_names = get_chat_list()
    chat_list = []

    for name in raw_chat_names:
        chat_data = load_chat(name)
        first_q = chat_data["past"][0] if chat_data["past"] else "New chat"
        truncated_q = first_q[:30] + '...' if len(first_q) > 30 else first_q
        chat_list.append({
            "name": name,
            "title": truncated_q
        })

    chat_name = chat_list[0]["name"] if chat_list else create_new_chat()
    chat_data = load_chat(chat_name) if chat_list else {"past": [], "generated": []}

    return render_template('index.html', chat_name=chat_name, chat_list=reversed(chat_list), chat_data=chat_data)

@app.route('/chat_list')
def chat_list():
    raw_chat_names = get_chat_list()
    chat_list = []
    for name in (raw_chat_names):  # reverse to show latest first
        chat_data = load_chat(name)
        first_q = chat_data["past"][0] if chat_data["past"] else "New chat"
        truncated_q = first_q[:30] + '...' if len(first_q) > 30 else first_q
        chat_list.append({
            "name": name,
            "title": truncated_q
        })
    return jsonify({"chat_list": reversed(chat_list)})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('user_input', '')
    chat_name = data.get('chat_name', '')

    if not user_input or not chat_name:
        return jsonify({"error": "Missing input or chat name"}), 400

    # Get response and source
    response, source_type = process_input(chat_name, user_input, return_source=True)

    # Log the source explicitly
    app.logger.info(f"⚡ Answer Source: {source_type} | Chat: {chat_name} | Input: {user_input}")
    app.logger.info(f"Response preview: {response[:100]}")  # optional

    return jsonify({
        "response": response,
        "source": source_type
    })

@app.route('/new_chat', methods=['POST'])
def new_chat():
    chat_name = create_new_chat()
    return jsonify({"chat_name": chat_name})

@app.route('/load_chat', methods=['POST'])
def load_existing_chat():
    data = request.json
    chat_name = data.get('chat_name')
    if not chat_name:
        return jsonify({"error": "Chat name required"}), 400

    chat_data = load_chat(chat_name)
    return jsonify({"chat_data": chat_data})

@app.route('/predict', methods=['GET', 'POST'])
def predict_judgment():
    raw_chat_names = get_chat_list()
    chat_list = []
    for name in raw_chat_names:
        chat_data = load_chat(name)
        first_q = chat_data["past"][0] if chat_data["past"] else "New chat"
        truncated_q = first_q[:30] + '...' if len(first_q) > 30 else first_q
        chat_list.append({
            "name": name,
            "title": truncated_q
        })

    error = None
    text = ""
    result = None

    if request.method == 'POST':
        file = request.files.get('file')
        file_type = request.form.get('file_type')

        if not file or not file_type:
            return jsonify({"error": "File and file type required."}), 400

        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)

        try:
            text = extract_text_from_file(temp_path, file_type)
            result = predict_verdict(text)
            return jsonify({
                "text": text,
                "result": result
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            try:
                os.remove(temp_path)
            except:
                pass

    # For GET request: render page
    return render_template('predict.html', chat_list=chat_list)


@app.route('/generate')
def generate():
    raw_chat_names = get_chat_list()
    chat_list = []
    for name in raw_chat_names:
        chat_data = load_chat(name)
        first_q = chat_data["past"][0] if chat_data["past"] else "New chat"
        truncated_q = first_q[:30] + '...' if len(first_q) > 30 else first_q
        chat_list.append({
            "name": name,
            "title": truncated_q
        })
    return render_template('generate.html',chat_list=chat_list)

@app.route('/generate_document', methods=['POST'])
def generate_document():
    data = request.json
    prompt = data.get('doc_prompt', '')
    if not prompt:
        return jsonify({'error': 'Prompt required'}), 400

    try:
        file_path, file_name = generate_legal_document(prompt)
        return jsonify({
            'download_url': f'/download/{file_name}',
            'file_name': file_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('static/generated_docs', filename, as_attachment=True)
