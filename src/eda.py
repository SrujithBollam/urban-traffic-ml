import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load preprocessed data
df = pd.read_csv("data/processed/final_processed.csv")

# Set output folder
output_dir = "reports/figures"
os.makedirs(output_dir, exist_ok=True)

# Plot 1: Hourly volume trend
plt.figure(figsize=(10, 6))
sns.boxplot(x="hour", y="volume_15min", data=df)
plt.title("Traffic Volume by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Volume (15 min)")
plt.savefig(f"{output_dir}/volume_by_hour.png")
plt.close()

# Plot 2: Day of week volume trend
plt.figure(figsize=(10, 6))
sns.boxplot(
    x="day_of_week",
    y="volume_15min",
    data=df,
    order=[
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ],
)
plt.title("Traffic Volume by Day of Week")
plt.xlabel("Day")
plt.ylabel("Volume (15 min)")
plt.savefig(f"{output_dir}/volume_by_day.png")
plt.close()

# Plot 3: Congestion level count
plt.figure(figsize=(6, 6))
df["congestion_level"].value_counts().plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Distribution of Congestion Levels")
plt.ylabel("")
plt.savefig(f"{output_dir}/congestion_level_pie.png")
plt.close()

# Plot 4: Rush hour comparison
plt.figure(figsize=(8, 6))
sns.boxplot(x="is_rush_hour", y="volume_15min", data=df)
plt.title("Rush Hour vs Non-Rush Hour Volume")
plt.xlabel("Is Rush Hour")
plt.ylabel("Volume (15 min)")
plt.savefig(f"{output_dir}/rush_hour_vs_volume.png")
plt.close()

print("EDA visualizations saved in: reports/figures/")
