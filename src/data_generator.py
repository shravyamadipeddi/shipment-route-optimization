
import csv
import random
import os

# Make the dataset reproducible
random.seed(42)

# Possible shipment locations
locations = [
    "Hyderabad", "Mumbai", "Chennai",
    "Singapore", "Dubai", "London",
    "New York", "Rotterdam", "Shanghai",
    "Tokyo"
]

# Possible intermediate hubs
hubs = [
    "Colombo", "Hamburg", "Port Klang",
    "Jebel Ali", "Hong Kong", "Singapore",
    "Dubai", "Rotterdam"
]

# Four simulated route profiles
route_profiles = {
    "Economy": {
        "cost": (0.75, 0.90),
        "time": (1.15, 1.40),
        "delay": (0.15, 0.35),
        "congestion": (2, 4),
        "geopolitical": (1, 4)
    },

    "Express": {
        "cost": (1.20, 1.45),
        "time": (0.55, 0.80),
        "delay": (0.05, 0.15),
        "congestion": (1, 3),
        "geopolitical": (1, 3)
    },

    "Balanced": {
        "cost": (0.95, 1.10),
        "time": (0.90, 1.10),
        "delay": (0.10, 0.25),
        "congestion": (1, 3),
        "geopolitical": (1, 3)
    },

    "Risky": {
        "cost": (0.65, 0.90),
        "time": (1.20, 1.60),
        "delay": (0.30, 0.55),
        "congestion": (3, 5),
        "geopolitical": (3, 5)
    }
}

shipments = []

# Generate 30 shipments
for shipment_num in range(1, 31):

    shipment_id = f"SH{shipment_num:03d}"

    # Select different origin and destination
    origin, destination = random.sample(locations, 2)

    # Base values for this shipment
    base_cost = random.randint(45000, 75000)
    base_time = random.randint(18, 28)

    # Each shipment receives all four profiles
    profiles = list(route_profiles.keys())
    random.shuffle(profiles)

    for route_num, profile_name in enumerate(profiles, start=1):

        profile = route_profiles[profile_name]

        # Calculate cost using the profile
        cost_factor = random.uniform(*profile["cost"])
        cost = round(base_cost * cost_factor)

        # Calculate transit time
        time_factor = random.uniform(*profile["time"])
        transit_time = max(1, round(base_time * time_factor))

        # Generate delay probability
        delay_probability = round(
            random.uniform(*profile["delay"]), 2
        )

        # Generate route risk indicators
        congestion_risk = random.randint(
            *profile["congestion"]
        )

        geopolitical_risk = random.randint(
            *profile["geopolitical"]
        )

        # Select a hub different from origin and destination
        available_hubs = [
            hub for hub in hubs
            if hub != origin and hub != destination
        ]

        intermediate_hub = random.choice(available_hubs)

        # Create route record
        route = {
            "shipment_id": shipment_id,
            "origin": origin,
            "destination": destination,
            "route_id": f"R{route_num}",
            "route_profile": profile_name,
            "intermediate_hub": intermediate_hub,
            "cost": cost,
            "transit_time": transit_time,
            "delay_probability": delay_probability,
            "congestion_risk": congestion_risk,
            "geopolitical_risk": geopolitical_risk
        }

        shipments.append(route)


# Save dataset
os.makedirs("data", exist_ok=True)

output_path = os.path.join("data", "shipments.csv")

with open(output_path, "w", newline="") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=shipments[0].keys()
    )

    writer.writeheader()
    writer.writerows(shipments)


# Display generation summary
df_profiles = {}

for route in shipments:
    profile = route["route_profile"]
    df_profiles[profile] = df_profiles.get(profile, 0) + 1

print("Improved shipment dataset generated successfully!")
print("Total shipments:", 30)
print("Total route records:", len(shipments))
print("\nRoute profile distribution:")

for profile, count in df_profiles.items():
    print(f"{profile}: {count}")

print("\nDataset saved at:", output_path)
