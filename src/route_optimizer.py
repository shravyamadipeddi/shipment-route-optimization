
import pandas as pd

# 1. Load processed shipment data
df = pd.read_csv("data/processed_shipments.csv")

# 2. Define weights for optimization criteria
weights = {
    "cost_norm": 0.35,
    "transit_time_norm": 0.25,
    "delay_probability_norm": 0.20,
    "congestion_risk_norm": 0.10,
    "geopolitical_risk_norm": 0.10
}

# 3. Calculate weighted score for every route
df["route_score"] = 0

for feature, weight in weights.items():
    df["route_score"] += df[feature] * weight

# Convert score to a scale of 0-100
df["route_score"] = df["route_score"] * 100

# 4. Rank routes separately for each shipment
df["route_rank"] = (
    df.groupby("shipment_id")["route_score"]
    .rank(method="min", ascending=True)
    .astype(int)
)

# 5. Select the best route for each shipment
recommendations = (
    df.sort_values(["shipment_id", "route_score", "route_id"])
    .groupby("shipment_id")
    .first()
    .reset_index()
)

# 6. Create an explanation for the recommendation
def explain_recommendation(best_route, alternatives):

    explanation = (
        f"Recommended {best_route['route_id']} because it "
        f"has the lowest weighted score of "
        f"{best_route['route_score']:.2f}."
    )

    if not alternatives.empty:

        second_best = alternatives.iloc[0]

        score_difference = (
            second_best["route_score"] - best_route["route_score"]
        )

        explanation += (
            f" It scores {score_difference:.2f} points "
            f"better than the next-ranked route "
            f"{second_best['route_id']}."
        )

    return explanation


# 7. Display recommendation for each shipment
print("\n========== SHIPMENT ROUTE RECOMMENDATIONS ==========")

for shipment_id in recommendations["shipment_id"]:

    best_route = recommendations[
        recommendations["shipment_id"] == shipment_id
    ].iloc[0]

    alternatives = (
        df[
            (df["shipment_id"] == shipment_id)
            & (df["route_id"] != best_route["route_id"])
        ]
        .sort_values("route_score")
    )

    explanation = explain_recommendation(
        best_route, alternatives
    )

    print(f"\nShipment ID: {shipment_id}")
    print(f"Origin: {best_route['origin']}")
    print(f"Destination: {best_route['destination']}")
    print(f"Recommended Route: {best_route['route_id']}")
    print(f"Route Profile: {best_route['route_profile']}")
    print(f"Intermediate Hub: {best_route['intermediate_hub']}")
    print(f"Shipping Cost: {best_route['cost']}")
    print(f"Transit Time: {best_route['transit_time']} days")
    print(f"Delay Probability: {best_route['delay_probability'] * 100:.1f}%")
    print(f"Route Score: {best_route['route_score']:.2f}")
    print("Explanation:", explanation)

# 8. Save all route scores
df.to_csv("outputs/route_scores.csv", index=False)

# 9. Save final recommendations
recommendations.to_csv(
    "outputs/route_recommendations.csv",
    index=False
)

print("\nOptimization completed successfully!")
print("Total recommendations:", len(recommendations))
print("Saved route scores and recommendations in outputs/")
