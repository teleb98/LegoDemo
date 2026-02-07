import http.server
import socketserver
import json
import os
import random
import cgi
import time
import sqlite3

PORT = 3000
MOBILE_DIR = os.path.join(os.path.dirname(__file__), '../mobile')
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
DB_FILE = os.path.join(os.path.dirname(__file__), 'lego.db')

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, setNumber TEXT, image TEXT, created_at INTEGER)''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

class LegoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # API: Get Products
        if self.path == '/api/products':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                conn = sqlite3.connect(DB_FILE)
                conn.row_factory = sqlite3.Row # Access columns by name
                c = conn.cursor()
                c.execute("SELECT * FROM products ORDER BY created_at DESC")
                rows = c.fetchall()
                products = [dict(row) for row in rows]
                conn.close()
                
                self.wfile.write(json.dumps(products).encode())
            except Exception as e:
                print(f"DB Error: {e}")
                self.wfile.write(b'[]')
            return

        # Serve Uploads
        if self.path.startswith('/uploads/'):
            filename = os.path.basename(self.path)
            filepath = os.path.join(UPLOADS_DIR, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
            return

        # Serve Mobile App Static Files
        path_to_serve = self.path
        if path_to_serve == '/' or path_to_serve == '/index.html':
            path_to_serve = '/index.html'
        
        safe_path = path_to_serve.lstrip('/')
        full_path = os.path.join(MOBILE_DIR, safe_path)
        
        if os.path.exists(full_path) and os.path.isfile(full_path):
            self.send_response(200)
            if full_path.endswith('.css'): self.send_header('Content-type', 'text/css')
            elif full_path.endswith('.js'): self.send_header('Content-type', 'application/javascript')
            elif full_path.endswith('.html'): self.send_header('Content-type', 'text/html')
            elif full_path.endswith('.png'): self.send_header('Content-type', 'image/png')
            elif full_path.endswith('.jpg'): self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            with open(full_path, 'rb') as f:
                self.wfile.write(f.read())
            return

        self.send_error(404, "File not found")


    def do_POST(self):
        if self.path == '/api/scan':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                fields = cgi.parse_multipart(self.rfile, pdict)
                
                if 'image' in fields:
                    image_data = fields['image'][0]
                    filename = f"scan_{int(time.time())}.jpg"
                    filepath = os.path.join(UPLOADS_DIR, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                    
                    # Mock logic
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
                    
                    # Insert into DB
                    conn = sqlite3.connect(DB_FILE)
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
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(new_product).encode())
                    return
            
            self.send_error(400, "Bad Request")

    def do_DELETE(self):
        # API: Delete Product
        if self.path.startswith('/api/products/'):
            try:
                product_id = int(self.path.split('/')[-1])
                
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("DELETE FROM products WHERE id=?", (product_id,))
                conn.commit()
                changes = c.rowcount
                conn.close()
                
                if changes == 0:
                    self.send_error(404, "Product not found")
                    return

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"success": true}')
                return
            except ValueError:
                self.send_error(400, "Invalid ID")
                return
            except Exception as e:
                print(e)
                self.send_error(500, "Server Error")
                return
        
        self.send_error(405, "Method Not Allowed")

print(f"Serving at http://0.0.0.0:{PORT}")
print(f"Mobile App: {MOBILE_DIR}")
print(f"Database: {DB_FILE}")

with socketserver.TCPServer(("", PORT), LegoHandler) as httpd:
    httpd.serve_forever()
