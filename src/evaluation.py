
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load processed dataset
df = pd.read_csv("data/processed_shipments.csv")

# 2. Define optimization scenarios
scenarios = {
    "Cost-focused": {
        "cost_norm": 0.60,
        "transit_time_norm": 0.15,
        "delay_probability_norm": 0.10,
        "congestion_risk_norm": 0.10,
        "geopolitical_risk_norm": 0.05
    },

    "Time-focused": {
        "cost_norm": 0.15,
        "transit_time_norm": 0.60,
        "delay_probability_norm": 0.10,
        "congestion_risk_norm": 0.10,
        "geopolitical_risk_norm": 0.05
    },

    "Balanced": {
        "cost_norm": 0.35,
        "transit_time_norm": 0.25,
        "delay_probability_norm": 0.20,
        "congestion_risk_norm": 0.10,
        "geopolitical_risk_norm": 0.10
    }
}

# 3. Validate scenario weights
for name, weights in scenarios.items():
    assert abs(sum(weights.values()) - 1.0) < 1e-9, (
        f"Weights for {name} must sum to 1."
    )

# 4. Calculate scores for each scenario
all_results = []

for scenario_name, weights in scenarios.items():

    temp = df.copy()

    temp["score"] = 0.0

    for feature, weight in weights.items():
        temp["score"] += temp[feature] * weight

    temp["score"] *= 100

    # Select best route for each shipment
    best_routes = (
        temp.sort_values(
            ["shipment_id", "score", "route_id"]
        )
        .groupby("shipment_id")
        .first()
        .reset_index()
    )

    best_routes["scenario"] = scenario_name

    all_results.append(best_routes)

# 5. Combine recommendations
results = pd.concat(all_results, ignore_index=True)

# Count selected route profiles in each scenario
profile_comparison = pd.crosstab(
    results["scenario"],
    results["route_profile"]
)

print("\n========== ROUTE PROFILE COMPARISON ==========")
print(profile_comparison)

# Save profile comparison
profile_comparison.to_csv(
    "outputs/profile_comparison.csv"
)

# 6. Calculate evaluation metrics
summary = (
    results.groupby("scenario")
    .agg(
        average_cost=("cost", "mean"),
        average_transit_time=("transit_time", "mean"),
        average_delay_probability=("delay_probability", "mean"),
        average_congestion_risk=("congestion_risk", "mean"),
        average_geopolitical_risk=("geopolitical_risk", "mean"),
        average_route_score=("score", "mean")
    )
    .round(2)
)

print("\n========== SCENARIO COMPARISON ==========")
print(summary)

# 7. Compare route selection changes
route_comparison = results.pivot(
    index="shipment_id",
    columns="scenario",
    values="route_id"
)

print("\n========== ROUTE SELECTION COMPARISON ==========")
print(route_comparison)

# 8. Calculate number of route changes
baseline = route_comparison["Balanced"]

print("\n========== SENSITIVITY ANALYSIS ==========")

for scenario in ["Cost-focused", "Time-focused"]:

    changes = (route_comparison[scenario] != baseline).sum()

    print(
        f"{scenario}: {changes} out of "
        f"{len(route_comparison)} shipments "
        "received a different recommendation."
    )

# 9. Save evaluation results
results.to_csv(
    "outputs/scenario_recommendations.csv",
    index=False
)

summary.to_csv(
    "outputs/sensitivity_summary.csv"
)

route_comparison.to_csv(
    "outputs/route_comparison.csv"
)

# 10. Visualize average cost by scenario
plt.figure(figsize=(8, 5))

summary["average_cost"].plot(
    kind="bar",
    title="Average Recommended Shipping Cost by Scenario",
    xlabel="Optimization Scenario",
    ylabel="Average Shipping Cost"
)

plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("outputs/scenario_cost_comparison.png")
plt.show()

# 11. Visualize average transit time
plt.figure(figsize=(8, 5))

summary["average_transit_time"].plot(
    kind="bar",
    title="Average Recommended Transit Time by Scenario",
    xlabel="Optimization Scenario",
    ylabel="Average Transit Time (Days)"
)

plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("outputs/scenario_time_comparison.png")
plt.show()

print("\nEvaluation completed successfully!")
