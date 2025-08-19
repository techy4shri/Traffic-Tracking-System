# Traffic Tracking System

A web application that detects and tracks vehicles in images and videos using machine learning.

## Features
- Upload images/videos for vehicle detection
- Count vehicles in media
- Extract vehicle numbers using OCR
- Real-time processing feedback
- Download processed results

## Tech Stack
### Frontend
- React 18
- TypeScript
- Vite
- Styled Components

### Backend
- Flask
- OpenCV
- TensorFlow
- Python-OCR

## Project Structure
```
traffic-tracking-system/
├── frontend/                # React + TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API integration
│   │   ├── styles/         # Global styles
│   │   └── types/         # TypeScript definitions
│   └── ...
├── backend/                # Flask backend
│   ├── api/               # API endpoints
│   ├── models/            # ML model interfaces
│   └── utils/             # Helper functions
└── models/                # ML model weights
```

## Setup Instructions

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Development
- Frontend runs on http://localhost:5173
- Backend runs on http://localhost:5000

## Contributors
- [Garima Shrivastava]

## License
MIT License