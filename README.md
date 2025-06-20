# Vehicle Number Plate Detection App

## 🚀 Overview
This is a *Vehicle Number Plate Detection App* built using *React.js*, *Flask*, using *YOLO (You Only Look Once)* model for object detection. The app allows users to upload images, detects vehicle number plates, reads the extracted text and keeps count of the vehicle. The application is containerized using *Docker* for easy deployment and scalability.

---

## 🎯 Features
- User-Friendly Interface: Navigation bar, image upload form, and result display for an intuitive user experience.
- Number Plate Detection: Detects vehicle number plates from uploaded images using the YOLO model.
- Text Extraction: Reads the detected number plates using Optical Character Recognition (OCR).
- Responsive Front-End: Built with React.js for a smooth and interactive user experience.
- Scalable Deployment: Packaged with Docker for portability and ease of deployment.
- Backend Powered by Streamlit: Handles image processing and OCR tasks efficiently.

---

## 🛠 Tech Stack
- *Frontend*: React.js
- *Backend*: Streamlit (Python)
- *Containerization*: Docker
- *Machine Learning*: YOLO v3
- *OCR*: Tesseract OCR
- *Computer Vision*: OpenCV, PyTorch

---

## 📦 Prerequisites
- *Node.js* and npm (or yarn)
- *Python* (3.8 or above)
- *Docker Desktop* installed on your system

---

## 📦 Setup & Installation
Follow these steps to set up and run the project locally:

### 1. Clone the Repository
`git clone https://github.com/techy4shri/IMAGE-DETECTION.git`
`cd IMAGE-DETECTION`


### 2. Install Frontend Dependencies
Ensure Node.js is installed:
`npm install  # or yarn install`


### 3. Install Backend Dependencies
Ensure Python is installed:
`pip install -r requirements.txt`


### 4. Running the Application
#### Build with Docker
1. Build the Docker images:
`docker-compose build`

2. Start the application:
`docker-compose up`

The app will be accessible at http://localhost:80 (frontend) and Streamlit backend.

#### Without Docker
1. Run the Streamlit backend:
`streamlit run app.py`

2. Start the React.js frontend:
`npm start`

Access the frontend at http://localhost:3000.

---

## 🖼 Testing the Application
1. Access the app in your web browser.
2. Use the *upload form* to select an image from your local machine.
3. The app processes the image, highlights detected vehicle number plates, and extracts the text.
4. Results, including the processed image and text, will be displayed.

---

## 📄 Dockerfile and docker-compose.yml
The project includes:
- *Frontend Dockerfile*: Defines the React.js container.
- *Backend Dockerfile*: Defines the Streamlit container.
- *docker-compose.yml*: Orchestrates the services and environment configurations.

---

## 🤖 Future Enhancements (This is an ongoing project)
- Improve detection accuracy using *YOLOv5* or *YOLOv7*.
- Integrate real-time *video detection* for live number plate recognition.
- Optimize *OCR logic* for better text accuracy.
- Add support for a *database* to store detected results.
- Deploy the app to cloud platforms like AWS or Azure.

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing
Contributions are welcome! If you find bugs or want to add new features:
1. Fork this repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m "Add some feature").
4. Push to the branch (git push origin feature-branch).
5. Open a Pull Request.

---

## 💻 Connect with Me
- *GitHub*: [techy4shri](https://github.com/techy4shri)
- *LinkedIn*: [Garima Shrivastav](https://linkedin.com/in/garima-shrivastav/)

---

### 🎉 Thank You!
If you like this project, don’t forget to star ⭐ the repository!
You can also sponser this project to help me maintain and develop it further!
