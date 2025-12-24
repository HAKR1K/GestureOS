import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# =========================
# LOAD DATA
# =========================
DATA_PATH = "gesture_data.csv"

df = pd.read_csv(DATA_PATH)

X = df.drop("label", axis=1).values
y = df["label"].values

print("Total samples:", len(df))
print("Classes:", set(y))

# =========================
# NORMALIZE DATA
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# TRAIN / TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# =========================
# TRAIN MODEL
# =========================
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=22,
    class_weight="balanced",  # 🔥 KEY FIX
    random_state=42
)


model.fit(X_train, y_train)

# =========================
# EVALUATE
# =========================
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("\nAccuracy:", acc)
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# =========================
# SAVE MODEL + SCALER
# =========================
joblib.dump(model, "gesture_model.pkl")
joblib.dump(scaler, "gesture_scaler.pkl")

print("\nModel saved as gesture_model.pkl")
print("Scaler saved as gesture_scaler.pkl")
