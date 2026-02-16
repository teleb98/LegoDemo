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

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
DB_FILE = os.path.join(BASE_DIR, 'lego.db')

# Ensure uploads directory exists
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

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
    print(f"Database initialized: {DB_FILE}")

# Initialize database on startup
init_db()

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# API Routes

@app.route('/api/photos', methods=['GET'])
def get_photos():
    """Get all photos ordered by newest first"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM photos ORDER BY created_at DESC")
        rows = c.fetchall()
        photos = [dict(row) for row in rows]
        conn.close()
        return jsonify(photos), 200
    except Exception as e:
        print(f"Error fetching photos: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/photos', methods=['POST'])
def upload_photo():
    """Upload a new photo"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400
        
        # Generate unique filename
        timestamp = int(time.time())
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        filename = f"lego_{timestamp}.{ext}"
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        # Save file
        file.save(filepath)
        
        # Get optional caption
        caption = request.form.get('caption', '')
        
        # Save to database
        conn = get_db()
        c = conn.cursor()
        c.execute("""INSERT INTO photos (filename, caption, created_at) 
                     VALUES (?, ?, ?)""",
                  (filename, caption, timestamp))
        photo_id = c.lastrowid
        conn.commit()
        conn.close()
        
        # Return the new photo data
        new_photo = {
            "id": photo_id,
            "filename": filename,
            "caption": caption,
            "created_at": timestamp
        }
        
        print(f"Photo uploaded: {filename}")
        return jsonify(new_photo), 200
        
    except Exception as e:
        print(f"Error uploading photo: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    """Delete a specific photo"""
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Get filename before deleting
        c.execute("SELECT filename FROM photos WHERE id = ?", (photo_id,))
        row = c.fetchone()
        
        if not row:
            conn.close()
            return jsonify({"error": "Photo not found"}), 404
        
        filename = row['filename']
        
        # Delete from database
        c.execute("DELETE FROM photos WHERE id = ?", (photo_id,))
        conn.commit()
        conn.close()
        
        # Delete file from filesystem
        filepath = os.path.join(UPLOADS_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Photo deleted: {filename}")
        
        return jsonify({"success": True}), 200
        
    except Exception as e:
        print(f"Error deleting photo: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/photos/<filename>', methods=['GET'])
def serve_photo(filename):
    """Serve a specific photo file"""
    try:
        filepath = os.path.join(UPLOADS_DIR, filename)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/jpeg')
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        print(f"Error serving photo: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current state for TV polling (latest photo info)"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM photos ORDER BY created_at DESC LIMIT 1")
        row = c.fetchone()
        conn.close()
        
        if row:
            latest_photo = dict(row)
            return jsonify({
                "latest_photo": latest_photo,
                "total_count": get_photo_count(),
                "timestamp": time.time()
            }), 200
        else:
            return jsonify({
                "latest_photo": None,
                "total_count": 0,
                "timestamp": time.time()
            }), 200
            
    except Exception as e:
        print(f"Error getting state: {e}")
        return jsonify({"error": str(e)}), 500

def get_photo_count():
    """Helper function to get total photo count"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as count FROM photos")
        result = c.fetchone()
        conn.close()
        return result['count']
    except:
        return 0

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok", "service": "LegoWorld V3 Backend"}), 200

if __name__ == '__main__':
    # Support cloud deployment with dynamic port
    port = int(os.getenv('PORT', 5000))
    
    print("=" * 60)
    print("LegoWorld V3 Backend Server")
    print("=" * 60)
    print(f"Database: {DB_FILE}")
    print(f"Uploads: {UPLOADS_DIR}")
    print(f"Server: http://0.0.0.0:{port}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=True)
