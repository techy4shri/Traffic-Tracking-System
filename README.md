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

## Testing:

Access the application in your web browser. Use the upload form to select an image from your local machine. The application will process the image and display both the original and the processed image with detected objects highlighted. Additional Notes:

You can stop the containers using docker-compose down. To detach from the running containers and keep them running in the background, use docker-compose up -d. Dockerfile and docker-compose.yml:

The project includes separate Dockerfiles for the frontend and backend, along with a docker-compose.yml file that specifies the environment and services. These files define how the application is packaged and run within Docker containers.

## Further Development:

This project provides a foundation for building a web application with object detection capabilities.

## License
MIT License
