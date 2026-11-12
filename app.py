
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Shipment Route Optimization",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Shipment Route Optimization Dashboard")
st.write(
    "Compare shipment routes based on cost, transit time, "
    "delay probability, congestion, and geopolitical risk."
)

# Load data
@st.cache_data
def load_data():
    recommendations = pd.read_csv(
        "outputs/route_recommendations.csv"
    )
    scenarios = pd.read_csv(
        "outputs/scenario_recommendations.csv"
    )
    profiles = pd.read_csv(
        "outputs/profile_comparison.csv",
        index_col=0
    )
    return recommendations, scenarios, profiles


recommendations, scenarios, profiles = load_data()

# Scenario selection
st.sidebar.header("Optimization Settings")

scenario = st.sidebar.selectbox(
    "Choose optimization scenario",
    ["Balanced", "Cost-focused", "Time-focused"]
)

# Filter recommendations
selected = scenarios[
    scenarios["scenario"] == scenario
].copy()

st.header(f"{scenario} Route Recommendations")

# Key metrics
col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Cost",
    f"₹{selected['cost'].mean():,.2f}"
)

col2.metric(
    "Average Transit Time",
    f"{selected['transit_time'].mean():.2f} days"
)

col3.metric(
    "Number of Shipments",
    selected["shipment_id"].nunique()
)

# Route recommendations table
st.subheader("Recommended Routes")
st.dataframe(selected, width="stretch")

# Route profile comparison
st.subheader("Route Profile Distribution")

profile_row = profiles.loc[scenario]

fig, ax = plt.subplots()
profile_row.plot(kind="bar", ax=ax)
ax.set_ylabel("Number of Shipments")
ax.set_xlabel("Route Profile")
ax.set_title(f"Selected Route Profiles - {scenario}")
ax.tick_params(axis="x", rotation=0)

st.pyplot(fig)
plt.close(fig)

# Scenario comparison
st.subheader("Scenario Comparison")

comparison = scenarios.groupby("scenario").agg(
    average_cost=("cost", "mean"),
    average_transit_time=("transit_time", "mean")
).round(2)

st.dataframe(comparison, width="stretch")

st.caption(
    "Note: This project uses synthetic shipment and route data "
    "for demonstration and evaluation."
)
