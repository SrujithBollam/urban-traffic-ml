import streamlit as st
import pydeck as pdk
import pandas as pd
import time

st.set_page_config(page_title="Pydeck Signal Animation", layout="centered")
st.title("🚥 Real-Time Traffic Signal Animation (Pydeck)")

# Define mock intersections
intersections = [
    {"id": "A", "lat": 43.651, "lon": -79.381},
    {"id": "B", "lat": 43.659, "lon": -79.387},
    {"id": "C", "lat": 43.667, "lon": -79.377},
    {"id": "D", "lat": 43.645, "lon": -79.375},
]

df = pd.DataFrame(intersections)

# Simulate current green intersection
green_interval = st.slider("Signal Duration per Intersection (s)", 3, 10, 5)
current_index = int(time.time() / green_interval) % len(df)
df["color"] = [
    [0, 255, 0] if i == current_index else [255, 0, 0] for i in range(len(df))
]

# Pydeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position="[lon, lat]",
    get_color="color",
    get_radius=50,
    pickable=True,
    auto_highlight=True,
)

# Render map
view_state = pdk.ViewState(
    latitude=df["lat"].mean(),
    longitude=df["lon"].mean(),
    zoom=13,
    pitch=0,
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
st.caption(f"🟢 Green signal at intersection: {df.loc[current_index, 'id']}")
