import streamlit as st
import joblib
import numpy as np

# Load model and label map
model = joblib.load("models/model.pkl")
label_map = joblib.load("models/label_map.pkl")
reverse_map = {v: k for k, v in label_map.items()}

st.set_page_config(page_title="Traffic Congestion Predictor", layout="centered")
st.title("🚦 Urban Traffic Congestion Predictor")

st.markdown("Enter current traffic stats to predict congestion level.")

# --- Inputs ---
hour = st.slider("Hour of Day", 0, 23, 8)
is_weekend = st.selectbox("Is it a weekend?", [0, 1])
is_rush_hour = st.selectbox("Is it rush hour?", [0, 1])
volume_15min = st.number_input("Vehicle volume in last 15 mins", min_value=0, value=50)

st.markdown("#### Speed Band Volumes (number of vehicles)")
speed_inputs = []
speed_bands = [
    "1–19",
    "20–25",
    "26–30",
    "31–35",
    "36–40",
    "41–45",
    "46–50",
    "51–55",
    "56–60",
    "61–65",
    "66–70",
    "71–75",
    "76–80",
    "81–160",
]
for band in speed_bands:
    value = st.number_input(f"{band} km/h", min_value=0, value=5)
    speed_inputs.append(value)

# --- Predict ---
if st.button("Predict Congestion Level"):
    features = np.array([[hour, is_weekend, is_rush_hour, volume_15min] + speed_inputs])
    prediction = model.predict(features)[0]
    label = reverse_map[prediction]

    st.success(f"Predicted Congestion Level: **{label}**")
    st.balloons()
