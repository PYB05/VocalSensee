import librosa
import soundfile as sf
import os

input_folder = "raw_audio/"
output_folder = "processed_audio/"
os.makedirs(output_folder, exist_ok=True)

def preprocess_audio(file_path, output_path, target_sr=16000):
    try:
        y, sr = librosa.load(file_path, sr=target_sr, mono=True)
        sf.write(output_path, y, target_sr)
    except Exception as e:
        print(f"⚠️ Error processing {file_path}: {e}")

for emotion in os.listdir(input_folder):
    emotion_path = os.path.join(input_folder, emotion)
    if os.path.isdir(emotion_path):
        output_emotion_folder = os.path.join(output_folder, emotion)
        os.makedirs(output_emotion_folder, exist_ok=True)

        for file_name in os.listdir(emotion_path):
            if file_name.endswith(".wav"):
                input_path = os.path.join(emotion_path, file_name)
                output_path = os.path.join(output_emotion_folder, file_name)
                preprocess_audio(input_path, output_path)

print("🎯 Preprocessing complete. Check 'processed_audio/' folder.")
