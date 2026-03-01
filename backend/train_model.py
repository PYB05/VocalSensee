import pickle
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load features and labels
with open("features_xgb.pkl", "rb") as f:
    features, labels = pickle.load(f)

# Encode string labels to numbers
le = LabelEncoder()
labels_encoded = le.fit_transform(labels)

# Standardize features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Train/test split
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_idx, test_idx in sss.split(features_scaled, labels_encoded):
    X_train, X_test = features_scaled[train_idx], features_scaled[test_idx]
    y_train, y_test = labels_encoded[train_idx], labels_encoded[test_idx]

# Train the model
model = XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, eval_metric='mlogloss')
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Test Accuracy: {acc * 100:.2f}%")

# Save everything
joblib.dump(model, "xgb_model.pkl")
joblib.dump(le, "label_encoder.pkl")
joblib.dump(scaler, "scaler.pkl")
print("✅ Model, LabelEncoder, and Scaler saved successfully!")
