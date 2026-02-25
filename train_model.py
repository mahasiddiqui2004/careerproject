"""
train_model.py
Trains a Random Forest classifier on synthetic career guidance data.
Saves: career_model.pkl, career_label_encoder.pkl
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

FEATURES = ["Math", "Science", "Computer", "Urdu", "S_St",
            "Eng_Text", "Eng_Gram", "Drawing", "Islamiat"]

# ── Load training data ────────────────────────────────────────────────────────
df = pd.read_csv("training_data.csv")
X  = df[FEATURES]
y  = df["stream"]

# ── Encode labels ─────────────────────────────────────────────────────────────
le = LabelEncoder()
y_enc = le.fit_transform(y)
print("Classes:", list(le.classes_))

# ── Train / test split ────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
)

# ── Train Random Forest ────────────────────────────────────────────────────────
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
acc    = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy: {acc*100:.1f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# ── Feature importance ────────────────────────────────────────────────────────
imp = sorted(zip(FEATURES, model.feature_importances_), key=lambda x: -x[1])
print("\nFeature Importances:")
for feat, score in imp:
    print(f"  {feat:12s}: {score:.3f}")

# ── Save model ────────────────────────────────────────────────────────────────
with open("career_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("career_label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("\n[OK] career_model.pkl and career_label_encoder.pkl saved!")