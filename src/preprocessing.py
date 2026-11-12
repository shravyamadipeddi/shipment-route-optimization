
import pandas as pd

# 1. Load the original dataset
df = pd.read_csv("data/shipments.csv")

print("Original dataset shape:", df.shape)

# 2. Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# 3. Remove duplicate records
df = df.drop_duplicates()

# 4. Define numerical criteria
criteria = [
    "cost",
    "transit_time",
    "delay_probability",
    "congestion_risk",
    "geopolitical_risk"
]

# 5. Check for invalid values
if df[criteria].isnull().any().any():
    raise ValueError("Missing values found in route criteria.")

if (df["cost"] < 0).any():
    raise ValueError("Shipping cost cannot be negative.")

if (df["transit_time"] <= 0).any():
    raise ValueError("Transit time must be positive.")

if not df["delay_probability"].between(0, 1).all():
    raise ValueError("Delay probability must be between 0 and 1.")

for column in ["congestion_risk", "geopolitical_risk"]:
    if not df[column].between(1, 5).all():
        raise ValueError(f"Invalid values in {column}.")

# 6. Normalize each criterion within each shipment
def normalize_group(series):
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(0.0, index=series.index)

    return (series - min_value) / (max_value - min_value)


for column in criteria:
    normalized_column = column + "_norm"

    df[normalized_column] = (
        df.groupby("shipment_id")[column]
        .transform(normalize_group)
    )

# 7. Display processed dataset
print("\nProcessed dataset:")
print(df.head())

# 8. Save processed dataset
df.to_csv("data/processed_shipments.csv", index=False)

print("\nPreprocessing completed successfully!")

print("Processed dataset shape:", df.shape)

print("\nNormalized feature summary:")
print(df[[column + "_norm" for column in criteria]].describe())

print("\nSaved to: data/processed_shipments.csv")
