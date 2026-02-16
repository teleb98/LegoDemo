# LegoWorld V3 - Mobile and TV Photo Integration

![LegoWorld V3](https://img.shields.io/badge/Version-3.0.0-blue) ![Tizen](https://img.shields.io/badge/Tizen-9.0-orange) ![Python](https://img.shields.io/badge/Python-3.8+-green)

**LegoWorld V3** is an interactive mobile-TV integration project that allows users to capture photos of their Lego sets on a mobile device and see them instantly visualized on a Tizen TV using remote control navigation.

## ✨ Features

### 📱 Mobile App (Streamlit)
- **"My Lego Sets"** - Dedicated photo capture interface
- Camera input or file upload
- Photo gallery with real-time sync
- Premium Lego-themed UI design
- Optional captions for each photo
- Delete functionality

### 📺 Tizen TV App
- Navigate existing Lego world scenes (SmartBrick, City, Space, Universe, etc.)
- **NEW: "My Photos" scene** accessible via remote Down arrow
- Photo gallery in 3-column grid layout
- Visual "NEW" indicators for recently added photos
- Fullscreen photo view with Enter button
- Automatic polling for new photos (2-second intervals)
- Smooth animations and transitions

### 🔧 Backend Server (Flask)
- RESTful API for photo management
- SQLite database for metadata storage
- Photo upload/retrieval/deletion endpoints
- State management for TV sync
- CORS enabled for cross-origin requests

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Mobile App     │         │  Backend Server  │         │   Tizen TV      │
│  (Streamlit)    │────────▶│    (Flask)       │◀────────│   Application   │
│                 │  HTTP   │                  │  Polling│                 │
│  - Camera       │         │  - REST API      │         │  - Photo Gallery│
│  - Gallery      │         │  - SQLite DB     │         │  - Remote Nav   │
│  - Upload       │         │  - File Storage  │         │  - Notifications│
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

## 📁 Project Structure

```
LegoWorld_v3/
├── streamlit_app.py          # Mobile web app
├── requirements.txt           # Python dependencies
├── server/
│   ├── app.py                # Flask backend API
│   ├── lego.db               # SQLite database
│   └── uploads/              # Photo storage directory
├── tizen/                    # Tizen TV application
│   ├── index.html            # Main HTML
│   ├── config.xml            # Tizen configuration
│   ├── icon.png              # App icon
│   ├── css/
│   │   └── main.css          # Styles
│   ├── js/
│   │   └── main.js           # Application logic
│   └── assets/               # Scene images and videos
│       ├── smartbrick1.jpg
│       ├── city1.jpg
│       ├── space.png
│       ├── city.mp4
│       └── ...
└── README.md
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- Tizen Studio 9.0 (for TV app development)
- Modern web browser

### 1. Install Python Dependencies

```bash
cd LegoWorld_v3
pip install -r requirements.txt
```

### 2. Start Backend Server

```bash
python server/app.py
```

Server will run on `http://localhost:5000`

### 3. Start Mobile App

In a new terminal:

```bash
streamlit run streamlit_app.py
```

Mobile app will open at `http://localhost:8501`

### 4. TV App Testing (Browser)

Open `tizen/index.html` in a web browser for testing:

```bash
cd tizen
open index.html  # macOS
# or just drag index.html to your browser
```

Use keyboard arrows to simulate remote control:
- **Up/Down**: Navigate scenes
- **Enter**: Play video or view fullscreen photo
- **Esc**: Go back

### 5. Deploy to Tizen TV

1. Open Tizen Studio 9.0
2. Import project:
   - File → Import → Tizen → Existing Tizen Project
   - Select the `tizen/` directory
3. Build the `.wgt` package
4. Install on TV or emulator
5. Test with TV remote control

## 📖 Usage Guide

### Capturing Photos on Mobile

1. Open the Streamlit app at `http://localhost:8501`
2. Go to the **"📸 Add Photo"** tab
3. Either:
   - Use the camera to take a photo
   - Upload a photo from your device
4. Add an optional caption
5. Click **"📤 Add to Collection"**
6. Photo is saved and synced to TV

### Viewing Photos on TV

1. Turn on the Tizen TV with LegoWorld V3 app
2. Press **Down** arrow on remote to navigate through scenes
3. When you reach **"My Photos"** scene:
   - Photo gallery appears in 3-column grid
   - Recently added photos show "NEW" badge
   - New photo indicator animates at top-right
4. Press **Enter** on a photo to view fullscreen
5. Press **Back** to return to gallery or dashboard

## 🎮 Remote Control Keys

| Key | Action |
|-----|--------|
| **Up Arrow** | Navigate to previous scene |
| **Down Arrow** | Navigate to next scene (including My Photos) |
| **Enter** | Play video / View fullscreen photo |
| **Back/Return** | Exit video / Exit gallery / Exit fullscreen |
| **Left/Right** | Navigate photos (future feature) |

## 🔌 API Endpoints

### Backend API (Port 5000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/photos` | Get all photos (newest first) |
| `POST` | `/api/photos` | Upload new photo |
| `DELETE` | `/api/photos/<id>` | Delete specific photo |
| `GET` | `/api/photos/<filename>` | Serve photo file |
| `GET` | `/api/state` | Get current state for TV polling |
| `GET` | `/health` | Health check |

### Example: Upload Photo

```bash
curl -X POST http://localhost:5000/api/photos \
  -F "file=@my_lego.jpg" \
  -F "caption=Millennium Falcon"
```

## 🎨 Design Highlights

- **Lego Color Palette**: Red (#E3000B), Yellow (#FFCF00), Blue (#0055BF)
- **Typography**: Poppins font family
- **Premium Effects**: 3D shadows, pulse animations, smooth transitions
- **Responsive Grid**: Adaptive photo layout
- **Visual Feedback**: New photo indicators, badges, hover effects

## 🔧 Configuration

### Backend URL

Both mobile and TV apps connect to `http://localhost:5000` by default.

To change:
- **Mobile App**: Edit `BACKEND_URL` in `streamlit_app.py`
- **TV App**: Edit `BACKEND_URL` in `tizen/js/main.js`

### Polling Interval

TV app polls for new photos every 2 seconds. To change:

Edit `tizen/js/main.js`:
```javascript
setInterval(async () => {
    // polling logic
}, 2000); // Change this value (in milliseconds)
```

## 🧪 Testing Scenarios

### End-to-End Test

1. **Mobile**: Upload a Lego photo with caption
2. **Backend**: Verify photo saved in `server/uploads/`
3. **TV**: Press Down arrow to "My Photos"
4. **Expected**: 
   - Photo appears in grid
   - "NEW" badge visible
   - "New Photo Added!" indicator shows
   - Photo is clickable for fullscreen view

### Multiple Photos Test

1. Upload 5-10 photos rapidly from mobile
2. Navigate to My Photos on TV
3. Verify all photos display correctly
4. Test scrolling if more than 9 photos
5. Verify newest photos have "NEW" badges

## 🐛 Troubleshooting

### Backend Connection Error

**Symptom**: Mobile app shows "Cannot connect to backend server"

**Solution**: 
- Ensure Flask server is running: `python server/app.py`
- Check port 5000 is not in use

### TV Not Showing Photos

**Symptom**: My Photos scene is empty

**Solution**:
- Check browser console for fetch errors
- Verify backend URL is correct in `tizen/js/main.js`
- Ensure backend server is accessible from TV/browser

### Photos Not Updating on TV

**Symptom**: New photos don't appear automatically

**Solution**:
- Exit and re-enter My Photos scene
- Check browser console for polling errors
- Verify `/api/state` endpoint returns correct data

## 📝 Future Enhancements

- [ ] AI-powered Lego set identification (Gemini API integration)
- [ ] Photo carousel mode with auto-advance
- [ ] Left/Right arrow navigation between photos
- [ ] Photo metadata (set number, theme, piece count)
- [ ] Cloud deployment for remote access
- [ ] Multi-user support
- [ ] Photo tagging and filtering

## 📄 License

This project is for demonstration purposes.

## 👨‍💻 Development

Built with:
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Mobile**: Streamlit (Python)
- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Platform**: Tizen 9.0 for Samsung Smart TV

---

**LegoWorld V3** © 2026 | Built for Samsung Tizen Smart TV
