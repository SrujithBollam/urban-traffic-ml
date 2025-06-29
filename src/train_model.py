import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Load processed data
df = pd.read_csv("data/processed/final_processed.csv")

# -------------------------------
# Define feature columns FIRST
# -------------------------------
feature_cols = [
    "hour",
    "is_weekend",
    "is_rush_hour",
    "volume_15min",
    "vol_1_19kph",
    "vol_20_25kph",
    "vol_26_30kph",
    "vol_31_35kph",
    "vol_36_40kph",
    "vol_41_45kph",
    "vol_46_50kph",
    "vol_51_55kph",
    "vol_56_60kph",
    "vol_61_65kph",
    "vol_66_70kph",
    "vol_71_75kph",
    "vol_76_80kph",
    "vol_81_160kph",
]

print(f"Before dropna: {len(df)} rows")

# Drop rows only if core values are missing
df = df.dropna(subset=["congestion_level", "volume_15min", "hour"])
speed_cols = [col for col in feature_cols if "vol_" in col]
df[speed_cols] = df[speed_cols].fillna(0)

print(f"After dropna: {len(df)} rows")

#  Manual label encoding (Low=0, Medium=1, High=2)
label_map = {"Low": 0, "Medium": 1, "High": 2}
df["label"] = df["congestion_level"].map(label_map)

# Split features and target
X = df[feature_cols]
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------
# 1. Logistic Regression
# ------------------------
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)
y_pred_log = logreg.predict(X_test)
print("\n--- Logistic Regression Results ---")
print(classification_report(y_test, y_pred_log))

# ------------------------
# 2. Random Forest
# ------------------------
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print("\n--- Random Forest Results ---")
print(classification_report(y_test, y_pred_rf))

# ------------------------
# 3. XGBoost
# ------------------------
xgb = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)
print("\n--- XGBoost Results ---")
print(classification_report(y_test, y_pred_xgb))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(xgb, "models/model.pkl")
joblib.dump(label_map, "models/label_map.pkl")  # save label map as well
print("\n Model and label map saved in models/")

# Debug sample
print("\nSample volumes & labels around 49:")
sample = df[df["volume_15min"].between(45, 52)][
    ["volume_15min", "congestion_level", "label"]
]
print(sample.sort_values("volume_15min"))
