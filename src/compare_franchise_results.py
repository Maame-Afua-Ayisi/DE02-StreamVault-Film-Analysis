
import pandas as pd

# Load the two franchise analysis results
all_years = pd.read_csv(
    "data/processed/franchise_analysis_all_years.csv"
)

recent_years = pd.read_csv(
    "data/processed/franchise_analysis_2000_onward.csv"
)

# Rename columns so both periods can be compared side by side
all_years = all_years.rename(columns={
    "candidate_films": "films_all_years",
    "total_revenue": "revenue_all_years",
    "aggregate_ratio": "ratio_all_years"
})

recent_years = recent_years.rename(columns={
    "candidate_films": "films_2000_onward",
    "total_revenue": "revenue_2000_onward",
    "aggregate_ratio": "ratio_2000_onward"
})

# Add rankings based on total revenue
all_years["rank_all_years"] = (
    all_years["revenue_all_years"]
    .rank(method="min", ascending=False)
)

recent_years["rank_2000_onward"] = (
    recent_years["revenue_2000_onward"]
    .rank(method="min", ascending=False)
)

# Match collections across both periods
comparison = all_years.merge(
    recent_years,
    on=["belongs_to_collection.id", "belongs_to_collection.name"],
    how="left",
    validate="one_to_one"
)

# Calculate differences
comparison["film_count_change"] = (
    comparison["films_2000_onward"] -
    comparison["films_all_years"]
)

comparison["revenue_change"] = (
    comparison["revenue_2000_onward"] -
    comparison["revenue_all_years"]
)

comparison["ratio_change"] = (
    comparison["ratio_2000_onward"] -
    comparison["ratio_all_years"]
)

comparison["rank_change"] = (
    comparison["rank_2000_onward"] -
    comparison["rank_all_years"]
)

# Sort by all-years revenue ranking
comparison = comparison.sort_values("rank_all_years")

# Display comparison
columns = [
    "belongs_to_collection.name",
    "films_all_years",
    "films_2000_onward",
    "rank_all_years",
    "rank_2000_onward",
    "rank_change",
    "revenue_change",
    "ratio_all_years",
    "ratio_2000_onward",
    "ratio_change"
]

print("FRANCHISE COMPARISON")
print("====================")
print(comparison[columns].to_string(index=False))

# Save complete comparison
comparison.to_csv(
    "data/processed/franchise_period_comparison.csv",
    index=False
)

print("\nCOMPARISON CHECKS")
print("=================")
print("Collections compared:", len(comparison))
print(
    "Collections without 2000-onward films:",
    comparison["films_2000_onward"].isna().sum()
)
print(
    "Collections with fewer candidate films:",
    (comparison["film_count_change"] < 0).sum()
)
print(
    "Collections with increased aggregate ratio:",
    (comparison["ratio_change"] > 0).sum()
)
