import pandas as pd

# Load data
volume_df = pd.read_csv("data/raw/toronto_volume_2020_2024.csv")
speed_df = pd.read_csv("data/raw/toronto_speed_2020_2024.csv")

# Show basic info
print("Volume Data:")
print(volume_df.head(), "\n")
print("Speed Data:")
print(speed_df.head())

# Merge using outer join to avoid losing data
merged_df = pd.merge(
    volume_df, speed_df, on="count_id", how="outer", suffixes=("_vol", "_spd")
)

# Drop rows with missing volume data (but allow speed to be missing)
merged_df = merged_df.dropna(subset=["time_start_vol", "volume_15min"])

# Proceed with the rest (datetime, features, labels...)


# Save the merged file
merged_df.to_csv("data/processed/merged_clean.csv", index=False)
print("Merged file saved at data/processed/merged_clean.csv")
# Convert time_start_vol to datetime
merged_df["datetime"] = pd.to_datetime(merged_df["time_start_vol"])

# Extract features
merged_df["hour"] = merged_df["datetime"].dt.hour
merged_df["day_of_week"] = merged_df["datetime"].dt.day_name()
merged_df["is_weekend"] = merged_df["day_of_week"].isin(["Saturday", "Sunday"])
merged_df["is_rush_hour"] = merged_df["hour"].isin([7, 8, 9, 16, 17, 18])

# Label congestion level from volume
merged_df["congestion_level"] = pd.cut(
    merged_df["volume_15min"],
    bins=[-1, 20, 50, float("inf")],
    labels=["Low", "Medium", "High"],
)

print("Label distribution:\n", merged_df["congestion_level"].value_counts())


# Save final processed data
merged_df.to_csv("data/processed/final_processed.csv", index=False)
print("Final cleaned dataset saved to data/processed/final_processed.csv")
