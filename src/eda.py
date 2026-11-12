
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("data/shipments.csv")

# Display first five records
print("\nFirst 5 records:")
print(df.head())

# Dataset information
print("\nDataset Information:")
print(df.info())

# Dataset shape
print("\nDataset Shape:")
print(df.shape)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Check duplicate records
print("\nDuplicate Records:")
print(df.duplicated().sum())

# Average cost and transit time
print("\nAverage Shipping Cost:")
print(df["cost"].mean())

print("\nAverage Transit Time:")
print(df["transit_time"].mean())

# Average delay probability
print("\nAverage Delay Probability:")
print(df["delay_probability"].mean())

# Cost distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["cost"], bins=15, kde=True)
plt.title("Distribution of Shipping Costs")
plt.xlabel("Shipping Cost")
plt.ylabel("Number of Routes")
plt.savefig("outputs/cost_distribution.png")
plt.show()

# Transit time distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["transit_time"], bins=15, kde=True)
plt.title("Distribution of Transit Time")
plt.xlabel("Transit Time (Days)")
plt.ylabel("Number of Routes")
plt.savefig("outputs/transit_distribution.png")
plt.show()

# Correlation heatmap
plt.figure(figsize=(9, 6))
sns.heatmap(
    df.select_dtypes(include=np.number).corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Correlation Between Numerical Features")
plt.savefig("outputs/correlation_heatmap.png")
plt.show()

print("\nEDA completed successfully!")
