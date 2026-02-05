# VocalSense: Real-Time Emotion Detection from Voice

VocalSense is a web-based application that predicts human emotions in real-time based on voice input. The system uses a Flask-based backend with a pre-trained ML model, and a responsive frontend built using HTML, CSS, and JavaScript.

### 📁 Project Structure

- **frontend/**
  - Contains the user-facing interface built with HTML, CSS, and JavaScript.
  - Handles microphone input and sends recorded audio to the backend.
  
- **backend/**
  - Contains the Flask server logic.
  - Includes:
    - `app.py`: The main Flask application.
    - `model.pkl`: The trained ML model for emotion prediction.
    - `utils.py`: Logic for audio feature extraction.
    - `requirements.txt`: Python dependencies.

## Features

- Records user's voice from browser
- Predicts emotions like happy, sad, angry, neutral
- Uses machine learning for real-time inference
- Clean and responsive web interface

## Installation & Setup

1. Clone the Repository

   git clone https://github.com/PYB05/VocalSense.git
   cd VocalSense

2. Backend Setup (Flask)

   cd backend
   pip install -r requirements.txt
   python app.py

   The backend will run on http://127.0.0.1:5000/

3. Frontend Setup

   Open frontend/index.html in a browser (use Live Server in VS Code or any HTTP server if needed)

## Machine Learning Model

- Extracts audio features like MFCCs
- Trained using Scikit-learn with labeled voice emotion dataset
- Model stored as model.pkl and loaded on backend

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- ML: Scikit-learn, Librosa
- Others: Web Audio API

## Author

https://github.com/PYB05, 
https://github.com/RyanFlame27

## Future Improvements

- Support for multi-language emotion detection
- Mobile-friendly UI
- Real-time dashboard to track mood trends
