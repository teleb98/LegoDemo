import streamlit as st
import sqlite3
import os
import time
import json
from google import genai
from google.genai import types

# Configuration
st.set_page_config(page_title="Lego World", page_icon="🧱", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, 'server', 'uploads')
DB_FILE = os.path.join(BASE_DIR, 'server', 'lego.db')
STATE_FILE = os.path.join(BASE_DIR, 'server', 'state.json')

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# --- Database Functions ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, setNumber TEXT, image TEXT, created_at INTEGER, theme TEXT, 
                  pieces INTEGER, age TEXT, description TEXT)''')
    # Add new columns if not exists (migration)
    for col in ['theme TEXT', 'pieces INTEGER', 'age TEXT', 'description TEXT']:
        try:
            c.execute(f"ALTER TABLE products ADD COLUMN {col}")
        except:
            pass
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(row) for row in products]

def add_product(image_path, name, set_number, theme, pieces=None, age=None, description=None):
    created_at = int(time.time())
    # Ensure image path is relative for DB
    if image_path.startswith(UPLOADS_DIR):
        db_image_path = os.path.basename(image_path)
    else:
        db_image_path = image_path

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""INSERT INTO products (name, setNumber, image, created_at, theme, pieces, age, description) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
              (name, set_number, db_image_path, created_at, theme, pieces, age, description))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

# --- AI & State Functions ---
def update_tv_state(theme, set_name):
    state = {
        "current_theme": theme,
        "detected_set": set_name,
        "timestamp": time.time()
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def analyze_image(image_path, api_key):
    if not api_key:
        # Mock Response
        time.sleep(1)
        return {
            "name": "Mock Millennium Falcon",
            "setNumber": "75192",
            "theme": "Star Wars"
        }
    
    try:
        client = genai.Client(api_key=api_key)
        
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        prompt = """
        Identify this Lego set and provide detailed information. Return a JSON object with:
        - name: The name of the set
        - setNumber: The set number (e.g., "75192")
        - theme: The main theme (e.g., Star Wars, Harry Potter, City, Technic, Ninjago)
        - pieces: Number of pieces (integer, estimate if unknown)
        - age: Recommended age range (e.g., "9+" or "18+")
        - description: A brief 1-2 sentence description of what the set includes and its key features
        """
        
        response = client.models.generate_content(
            model='models/gemini-flash-latest',
            contents=[
                types.Part(text=prompt),
                types.Part(inline_data=types.Blob(
                    mime_type="image/jpeg",
                    data=image_data
                ))
            ]
        )
        
        text = response.text
        # Clean up code blocks if present
        text = text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None

# --- UI Setup ---
init_db()

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cera+Pro&display=swap');
    
    :root {
        --lego-red: #E3000B;
        --lego-yellow: #FFCF00;
        --lego-blue: #0055BF;
        --lego-white: #FFFFFF;
        --lego-black: #2C2C2C;
    }
    
    .stApp { background-color: var(--lego-white); }
    header[data-testid="stHeader"] { background-color: var(--lego-yellow); }
    
    h1 {
        color: var(--lego-red);
        font-weight: 900;
        text-shadow: 2px 2px 0px var(--lego-yellow), 4px 4px 0px var(--lego-black);
        text-transform: uppercase;
        text-align: center;
        padding: 1rem;
    }
    
    .stButton button {
        background-color: var(--lego-blue);
        color: white;
        border-radius: 20px;
        border: none;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #004499;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Check if key is in secrets
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("API Key loaded from Secrets!")
    else:
        api_key = st.text_input("Google AI API Key", type="password")
        st.info("Enter key to use real AI identification. Leave blank for mock mode.")

st.title("MY LEGO SETS")

# Main Input Area
tab1, tab2 = st.tabs(["📸 Scan New", "📂 Select Saved"])

with tab1:
    uploaded_file = st.file_uploader("Take a photo of a Lego box", type=['jpg', 'png', 'jpeg'])
    if uploaded_file is not None:
        if st.button("Identify & Add"):
            with st.spinner("Analyzing with AI..."):
                # Save first
                filename = f"scan_{int(time.time())}.jpg"
                filepath = os.path.join(UPLOADS_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Analyze
                result = analyze_image(filepath, api_key)
                
                if result:
                    add_product(
                        filename, result['name'], result['setNumber'], result['theme'],
                        result.get('pieces'), result.get('age'), result.get('description')
                    )
                    update_tv_state(result['theme'], result['name'])
                    st.success(f"Identified: {result['name']} ({result['theme']})")
                    time.sleep(1)
                    st.rerun()

with tab2:
    # List files in uploads dir
    files = [f for f in os.listdir(UPLOADS_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))]
    if not files:
        st.write("No saved images found.")
    else:
        selected_file = st.selectbox("Choose an image", files)
        if selected_file:
            filepath = os.path.join(UPLOADS_DIR, selected_file)
            st.image(filepath, width=300)
            if st.button("Identify This Image"):
                with st.spinner("Analyzing..."):
                    result = analyze_image(filepath, api_key)
                    if result:
                        add_product(
                            selected_file, result['name'], result['setNumber'], result['theme'],
                            result.get('pieces'), result.get('age'), result.get('description')
                        )
                        update_tv_state(result['theme'], result['name'])
                        st.success(f"Identified: {result['name']} ({result['theme']})")
                        time.sleep(1)
                        st.rerun()

# Product Grid
st.markdown("---")
products = get_products()

if not products:
    st.info("No sets found. Add one above!")
else:
    cols = st.columns(2) 
    for i, product in enumerate(products):
        col = cols[i % 2]
        with col:
            img_path = product['image']
            if img_path.startswith('/uploads/'): img_path = img_path.replace('/uploads/', '')
            full_img_path = os.path.join(UPLOADS_DIR, img_path)
            
            with st.container(border=True):
                # Display Image with shadow effect
                try:
                    st.image(full_img_path, use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/400x300?text=Lego+Set", use_container_width=True)
                
                # Product Title
                st.markdown(f"### {product['name']}")
                
                # Set Number and Theme Badge
                st.markdown(f"**Set #{product['setNumber']}** · `{product.get('theme', 'Unknown')}`")
                
                # AI Details
                if product.get('pieces') or product.get('age'):
                    details = []
                    if product.get('pieces'):
                        details.append(f"🧱 {product['pieces']} pieces")
                    if product.get('age'):
                        details.append(f"👤 Ages {product['age']}")
                    st.caption(" · ".join(details))
                
                # Description
                if product.get('description'):
                    st.markdown(f"*{product['description']}*")
                
                # Delete Button
                if st.button("🗑️ Delete", key=f"del_{product['id']}", type="secondary", use_container_width=True):
                    delete_product(product['id'])
                    st.rerun()
