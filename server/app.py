import os
import time
import json
import sqlite3
import random
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__, static_folder='../mobile')
CORS(app)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOBILE_DIR = os.path.join(BASE_DIR, '../mobile')
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
DB_FILE = os.path.join(BASE_DIR, 'lego.db')

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, setNumber TEXT, image TEXT, created_at INTEGER)''')
    conn.commit()
    conn.close()

# Initialize DB
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# State File
STATE_FILE = os.path.join(BASE_DIR, 'state.json')

def get_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"current_theme": "default", "detected_set": null}

@app.route('/')
def serve_tv_app():
    # Serve the TV App (index.html) from the project root
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory(os.path.join(BASE_DIR, 'css'), path)

@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory(os.path.join(BASE_DIR, 'js'), path)

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(os.path.join(BASE_DIR, 'assets'), path)

@app.route('/<path:path>')
def serve_root_files(path):
    # Serve other root files if needed
    return send_from_directory(BASE_DIR, path)

@app.route('/mobile/<path:path>')
def serve_mobile(path):
    return send_from_directory(MOBILE_DIR, path)

@app.route('/uploads/<filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOADS_DIR, filename)

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
        conn.close()
        return jsonify([dict(row) for row in products])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify([])

@app.route('/api/state', methods=['GET'])
def get_app_state():
    return jsonify(get_state())

@app.route('/api/scan', methods=['POST'])
def scan_product():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(f"scan_{int(time.time())}.jpg")
        filepath = os.path.join(UPLOADS_DIR, filename)
        file.save(filepath)

        # Mock Logic
        mock_sets = [
            {"name": "Millennium Falcon", "setNumber": "75192"},
            {"name": "Hogwarts Castle", "setNumber": "71043"},
            {"name": "Bugatti Chiron", "setNumber": "42083"},
            {"name": "Tree House", "setNumber": "21318"},
            {"name": "Saturn V", "setNumber": "92176"}
        ]
        random_set = random.choice(mock_sets)
        created_at = int(time.time())
        image_url = f"/uploads/{filename}"

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO products (name, setNumber, image, created_at) VALUES (?, ?, ?, ?)",
                  (random_set['name'], random_set['setNumber'], image_url, created_at))
        new_id = c.lastrowid
        conn.commit()
        conn.close()

        new_product = {
            "id": new_id,
            "name": random_set['name'],
            "setNumber": random_set['setNumber'],
            "image": image_url,
            "created_at": created_at
        }
        return jsonify(new_product)

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE id=?", (id,))
        conn.commit()
        changes = c.rowcount
        conn.close()

        if changes == 0:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
