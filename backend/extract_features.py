import os
import librosa
import pickle
import numpy as np
from tqdm import tqdm

DATA_DIR = "processed_audio"
features, labels = [], []

def extract_features_from_audio(filepath):
    y, sr = librosa.load(filepath, sr=22050)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    log_mel_spec = librosa.power_to_db(mel_spec)
    mean_spec = np.mean(log_mel_spec, axis=1)
    return mean_spec

for label in os.listdir(DATA_DIR):
    folder = os.path.join(DATA_DIR, label)
    if not os.path.isdir(folder):
        continue
    for file in tqdm(os.listdir(folder), desc=f"Processing {label}"):
        if not file.endswith(".wav"):
            continue
        filepath = os.path.join(folder, file)
        try:
            features.append(extract_features_from_audio(filepath))
            labels.append(label)
        except Exception as e:
            print(f"⚠️ Error processing {file}: {e}")

features = np.array(features)
labels = np.array(labels)

with open("features_xgb.pkl", "wb") as f:
    pickle.dump((features, labels), f)

print("✅ Feature extraction complete and saved to features_xgb.pkl")
