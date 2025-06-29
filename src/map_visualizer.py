import folium
import pandas as pd

# Load your processed dataset with coordinates + congestion
df = pd.read_csv("data/processed/final_processed.csv")

# Get a small sample for plotting (optional)
df = df.dropna(subset=["latitude_vol", "longitude_vol", "congestion_level"])
df = df.sample(300, random_state=42)  # limit to 300 points for speed

# Create base map centered around the city
m = folium.Map(location=[43.65, -79.38], zoom_start=12)  # Toronto default center

# Color mapping
color_map = {"Low": "green", "Medium": "orange", "High": "red"}

# Add each point
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude_vol"], row["longitude_vol"]],
        radius=5,
        color=color_map.get(row["congestion_level"], "gray"),
        fill=True,
        fill_opacity=0.7,
        popup=f"Volume: {row['volume_15min']}<br>Level: {row['congestion_level']}",
    ).add_to(m)

# Save to HTML
m.save("app/congestion_map.html")
print(" Map saved to app/congestion_map.html")
