import streamlit as st
import numpy as np
import joblib
import pulp
import folium
import pandas as pd
import pydeck as pdk
import streamlit.components.v1 as components
import time

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Urban Traffic AI System", layout="centered")

# ---------------------- SIDEBAR ---------------------
st.sidebar.title("🚦 Urban Traffic Assistant")
page = st.sidebar.radio(
    "Choose Feature",
    [
        "Congestion Predictor",
        "Signal Optimizer",
        "🌍 Congestion Map View",
        "🚦 Pydeck Signal Animation",
    ],
)

# ---------------------- MODEL LOADING ----------------------
model = joblib.load("models/model.pkl")
label_map = joblib.load("models/label_map.pkl")
reverse_map = {v: k for k, v in label_map.items()}

# ---------------------- PAGE 1: Congestion Predictor ----------------------
if page == "Congestion Predictor":
    st.title("Traffic Congestion Predictor")
    st.markdown("Enter traffic features to predict congestion level.")

    hour = st.slider("Hour of Day", 0, 23, 8)
    is_weekend = st.selectbox("Is it a weekend?", [0, 1])
    is_rush_hour = st.selectbox("Is it rush hour?", [0, 1])
    volume_15min = st.number_input(
        "Vehicle volume (last 15 mins)", min_value=0, value=50
    )

    st.markdown("#### Speed Band Volumes")
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
    speed_inputs = [
        st.number_input(f"{band} km/h", min_value=0, value=5) for band in speed_bands
    ]

    if st.button("Predict Congestion Level"):
        features = np.array(
            [[hour, is_weekend, is_rush_hour, volume_15min] + speed_inputs]
        )
        prediction = model.predict(features)[0]
        label = reverse_map[prediction]
        st.success(f"Predicted Congestion Level: **{label}**")
        st.balloons()

# ---------------------- PAGE 2: Signal Optimizer ----------------------
elif page == "Signal Optimizer":
    st.title("🚥 Signal Timing Optimizer")
    st.markdown(
        "Enter traffic volumes from each direction to calculate optimal green time allocation for a 120s cycle."
    )

    vol_N = st.number_input("North Volume", min_value=0, value=50)
    vol_E = st.number_input("East Volume", min_value=0, value=80)
    vol_S = st.number_input("South Volume", min_value=0, value=60)
    vol_W = st.number_input("West Volume", min_value=0, value=30)

    traffic_volume = {"North": vol_N, "East": vol_E, "South": vol_S, "West": vol_W}

    if st.button("Optimize Signal Timings"):
        total_cycle_time = 120
        prob = pulp.LpProblem("Signal_Timing_Optimization", pulp.LpMinimize)

        green_time = {
            dir: pulp.LpVariable(f"green_{dir}", lowBound=10, cat="Continuous")
            for dir in traffic_volume
        }

        ideal_total = sum(traffic_volume.values())
        deviations = {}

        for direction in traffic_volume:
            ideal = (traffic_volume[direction] / ideal_total) * total_cycle_time
            dev = pulp.LpVariable(f"dev_{direction}", lowBound=0, cat="Continuous")
            deviations[direction] = dev

            prob += green_time[direction] - ideal <= dev
            prob += ideal - green_time[direction] <= dev

        prob += pulp.lpSum(deviations.values())
        prob += pulp.lpSum(green_time.values()) == total_cycle_time

        prob.solve()

        st.subheader("Optimized Green Light Durations")
        for direction in traffic_volume:
            st.write(f"**{direction}:** {green_time[direction].varValue:.2f} seconds")


# ---------------------- PAGE 3: Congestion Map View ----------------------
elif page == "🌍 Congestion Map View":
    st.title("Congestion Map")
    st.markdown("Real-time congestion levels across the city.")

    try:
        df = pd.read_csv("data/processed/final_processed.csv")
        df = df.dropna(subset=["latitude_vol", "longitude_vol", "congestion_level"])
        df = df.sample(min(300, len(df)), random_state=42)

        m = folium.Map(
            location=[df["latitude_vol"].mean(), df["longitude_vol"].mean()],
            zoom_start=12,
        )

        color_map = {"Low": "green", "Medium": "orange", "High": "red"}

        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row["latitude_vol"], row["longitude_vol"]],
                radius=5,
                color=color_map.get(row["congestion_level"], "gray"),
                fill=True,
                fill_opacity=0.7,
                popup=f"Level: {row['congestion_level']}<br>Vol: {row['volume_15min']}",
            ).add_to(m)

        m.save("app/congestion_map.html")

        with open("app/congestion_map.html", "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=600, scrolling=True)

    except Exception as e:
        st.error(
            "Failed to load map. Make sure data/processed/final_processed.csv exists and contains lat/long."
        )
        st.exception(e)

# ---------------------- PAGE 4: Pydeck Animated Signals ----------------------
elif page == "🚦 Pydeck Signal Animation":
    st.title("🚦 Real-Time Signal Animation (Pydeck)")
    st.markdown("Simulating signal light transitions using timed blinking.")

    intersections = [
        {"id": "A", "lat": 43.651, "lon": -79.381},
        {"id": "B", "lat": 43.659, "lon": -79.387},
        {"id": "C", "lat": 43.667, "lon": -79.377},
        {"id": "D", "lat": 43.645, "lon": -79.375},
    ]
    df = pd.DataFrame(intersections)

    green_time = st.slider("Green Time Per Signal (seconds)", 3, 10, 5)

    current = int(time.time() / green_time) % len(df)
    df["color"] = [[0, 255, 0] if i == current else [255, 0, 0] for i in range(len(df))]

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[lon, lat]",
        get_color="color",
        get_radius=60,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=df["lat"].mean(), longitude=df["lon"].mean(), zoom=13, pitch=0
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    st.caption(f"🟢 Green signal currently ON at: Intersection {df.loc[current, 'id']}")
