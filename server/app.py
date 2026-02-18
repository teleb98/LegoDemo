"""
LegoWorld V3 - Backend Server
Flask API for photo management and TV sync
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
import time
from werkzeug.utils import secure_filename
import google.generativeai as genai
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
DB_FILE = os.path.join(BASE_DIR, 'lego.db')

# Ensure uploads directory exists
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use gemini-2.5-flash - supports vision and generateContent
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("✅ Gemini AI configured (gemini-2.5-flash)")
else:
    model = None
    print("⚠️  GEMINI_API_KEY not set - AI identification disabled")

# Database initialization
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS photos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT NOT NULL,
                  caption TEXT,
                  created_at INTEGER NOT NULL,
                  ai_identified_name TEXT,
                  theme TEXT)''')
    conn.commit()
    conn.close()
    print(f"SQLite database initialized: {DB_FILE}")

# Initialize database on startup
init_db()

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# AI Identification Function
def identify_lego_with_ai(file_object):
    """
    Use Gemini Vision to identify LEGO set from image
    
    Args:
        file_object: File object (from request.files) or file path string
    
    Returns:
        str: Identified LEGO set name or None if failed
    """
    if not model:
        return None
    
    try:
        # Prepare prompt
        prompt = """Analyze this image and identify the LEGO set.
        
Please provide ONLY the LEGO set name and number if visible.
If you can identify it, respond in this format: "LEGO [Set Name] ([Set Number])"
If you cannot identify it, respond: "Unknown LEGO Set"

Examples:
- "LEGO Star Wars Millennium Falcon (75192)"
- "LEGO Creator Expert Taj Mahal (10256)"
- "LEGO City Fire Truck (60331)"
- "Unknown LEGO Set"

Keep the response concise and in English."""
        
        # Gemini can accept file objects directly or file paths
        # For file objects, read the bytes
        if isinstance(file_object, str):
            # File path - read file
            with open(file_object, 'rb') as f:
                image_data = f.read()
        else:
            # File object from request.files - read bytes
            file_object.seek(0)  # Reset to beginning
            image_data = file_object.read()
        
        # Upload to Gemini
        image_part = {"mime_type": "image/jpeg", "data": image_data}
        
        # Generate content with prompt and image
        response = model.generate_content([prompt, image_part])
        
        if response and response.text:
            identified_name = response.text.strip()
            print(f"🤖 AI identified: {identified_name}")
            return identified_name
        
    except Exception as e:
        print(f"❌ AI identification failed: {e}")
        import traceback
        traceback.print_exc()
    
    return None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "service": "LegoWorld V3 Backend"})

@app.route('/api/photos', methods=['GET'])
def get_photos():
    conn = get_db()
    photos = conn.execute('SELECT * FROM photos ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(photo) for photo in photos])

@app.route('/api/photos/<filename>', methods=['GET'])
def get_photo(filename):
    return send_file(os.path.join(UPLOADS_DIR, filename))

@app.route('/api/photos', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        timestamp = int(time.time())
        original_filename = secure_filename(file.filename)
        extension = os.path.splitext(original_filename)[1]
        new_filename = f"lego_{timestamp}{extension}"
        
        # AI Identification
        ai_name = None
        if model:
            print(f"🤖 Analyzing photo with Gemini AI...")
            # We pass the file object directly to our helper function
            ai_name = identify_lego_with_ai(file)
            # Reset file pointer to beginning after AI reads it, so we can save it
            file.seek(0)
        
        # Save file locally
        file.save(os.path.join(UPLOADS_DIR, new_filename))
        
        caption = request.form.get('caption', '')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO photos (filename, caption, created_at, ai_identified_name) VALUES (?, ?, ?, ?)',
            (new_filename, caption, timestamp, ai_name)
        )
        photo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            "id": photo_id,
            "filename": new_filename,
            "caption": caption,
            "created_at": timestamp,
            "ai_identified_name": ai_name,
            "message": "Photo uploaded successfully"
        })

@app.route('/api/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    conn = get_db()
    photo = conn.execute('SELECT * FROM photos WHERE id = ?', (photo_id,)).fetchone()
    
    if photo:
        # Delete file
        try:
            os.remove(os.path.join(UPLOADS_DIR, photo['filename']))
        except OSError:
            pass  # File might not exist
            
        # Delete from DB
        conn.execute('DELETE FROM photos WHERE id = ?', (photo_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Photo deleted"})
    else:
        conn.close()
        return jsonify({"error": "Photo not found"}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print(f"🚀 LegoWorld V3 Server running on port {port}")
    app.run(host='0.0.0.0', port=port)
