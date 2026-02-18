# LegoWorld V3 - Local Setup

## Quick Start

### Terminal 1: Backend Server
```bash
cd /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3
export GEMINI_API_KEY=AIzaSyD7vY3NsBvPgJSJz0oAN80RCxBAex1DSoo
PORT=5001 python3 server/app.py
```

### Terminal 2: Streamlit App (Local)
```bash
cd /Users/chiwon/.gemini/antigravity/scratch/LegoWorld_v3
streamlit run streamlit_app.py
```

### Terminal 3: ngrok (for Tizen TV)
```bash
~/Downloads/ngrok http 5001 --log=stdout
```

## Access

- **Streamlit App (Local)**: http://localhost:8501
- **Backend API**: http://localhost:5001
- **Tizen TV**: Use ngrok URL

## Current Status

✅ **Backend**: Running on port 5001  
✅ **Gemini AI**: Identifying Lego sets  
🔄 **Streamlit**: Run locally instead of Cloud  
✅ **Tizen**: Connected via ngrok
