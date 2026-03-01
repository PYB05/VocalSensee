from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import librosa
import numpy as np
import joblib
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model components
model = joblib.load("xgb_model.pkl")
le = joblib.load("label_encoder.pkl")
scaler = joblib.load("scaler.pkl")

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=22050)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    log_mel_spec = librosa.power_to_db(mel_spec)
    mean_spec = np.mean(log_mel_spec, axis=1)
    return mean_spec

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        features = extract_features(filepath)
        features_scaled = scaler.transform([features])
        pred = model.predict(features_scaled)
        label = le.inverse_transform(pred)[0]
        return jsonify({'prediction': label})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
