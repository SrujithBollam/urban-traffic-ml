import streamlit as st
import pulp

st.set_page_config(page_title="Signal Optimizer", layout="centered")
st.title("🚥 Intersection Signal Optimizer")

st.markdown(
    "Enter traffic volumes from each direction to calculate optimal green light durations for a 120-second signal cycle."
)

# --- User Inputs ---
st.subheader("🔢 Traffic Volume Input")
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

    # Ideal calculation and deviation setup
    ideal_total = sum(traffic_volume.values())
    deviations = {}

    for direction in traffic_volume:
        ideal = (traffic_volume[direction] / ideal_total) * total_cycle_time
        dev = pulp.LpVariable(f"dev_{direction}", lowBound=0, cat="Continuous")
        deviations[direction] = dev

        prob += green_time[direction] - ideal <= dev
        prob += ideal - green_time[direction] <= dev

    prob += pulp.lpSum(deviations.values())  # minimize total deviation
    prob += pulp.lpSum(green_time.values()) == total_cycle_time

    prob.solve()

    # --- Results ---
    st.subheader(" Optimized Green Light Durations")
    for direction in traffic_volume:
        st.write(f"**{direction}:** {green_time[direction].varValue:.2f} seconds")

    st.subheader(" Target vs Optimized")
    for direction in traffic_volume:
        ideal = (traffic_volume[direction] / ideal_total) * total_cycle_time
        actual = green_time[direction].varValue
        st.write(f"{direction}: Ideal = {ideal:.2f}s | Optimized = {actual:.2f}s")
