import pulp

# Simulated traffic volumes from sensors (you can integrate real-time data later)
traffic_volume = {"North": 50, "East": 80, "South": 60, "West": 30}

# Total signal cycle time (in seconds)
total_cycle_time = 120

# Initialize LP problem
prob = pulp.LpProblem("Signal_Timing_Optimization", pulp.LpMinimize)

# Create green time variables for each direction (continuous, ≥ 10s)
green_time = {
    direction: pulp.LpVariable(f"green_{direction}", lowBound=10, cat="Continuous")
    for direction in traffic_volume
}

# Objective: Minimize total delay → indirectly minimize difference between allocation & need
# For now, just keep a dummy objective (we're just interested in the allocation)
# Objective: Minimize squared difference from proportional time
ideal_total = sum(traffic_volume.values())

# Add absolute deviation variables
deviations = {}

for direction in traffic_volume:
    ideal = (traffic_volume[direction] / ideal_total) * total_cycle_time
    dev = pulp.LpVariable(f"dev_{direction}", lowBound=0, cat="Continuous")
    deviations[direction] = dev

    # Add constraints: deviation captures |green - ideal|
    prob += green_time[direction] - ideal <= dev
    prob += ideal - green_time[direction] <= dev

# Objective: minimize total absolute deviation
prob += pulp.lpSum(deviations.values())


# Solve LP
prob.solve()

# Print optimal green times
print(" Optimized Green Light Durations:")
for direction in traffic_volume:
    print(f"{direction}: {green_time[direction].varValue:.2f} seconds")

# Print comparison: ideal vs optimized
print("\n Target vs Optimized:")
for direction in traffic_volume:
    ideal = (traffic_volume[direction] / ideal_total) * total_cycle_time
    actual = green_time[direction].varValue
    print(f"{direction}: Ideal = {ideal:.2f}s | Optimized = {actual:.2f}s")
