
import pandas as pd

# 1. Load the analysis dataset
movies = pd.read_csv("data/processed/movie_analysis.csv")

# 2. Keep films with recorded collection membership
franchise_movies = movies.loc[
    movies["belongs_to_collection.id"].notna()
].copy()

# 3. Group by collection
franchise_summary = (
    franchise_movies.groupby(
        ["belongs_to_collection.id", "belongs_to_collection.name"]
    )
    .agg(
        candidate_films=("id", "nunique"),
        total_budget=("budget", "sum"),
        total_revenue=("revenue", "sum"),
        average_revenue=("revenue", "mean"),
        average_ratio=("revenue_budget_ratio", "mean")
    )
    .reset_index()
)

# 4. Calculate aggregate revenue-to-budget ratio
franchise_summary["aggregate_ratio"] = (
    franchise_summary["total_revenue"] /
    franchise_summary["total_budget"]
)

# 5. Sort by total revenue
franchise_summary = franchise_summary.sort_values(
    "total_revenue",
    ascending=False
)

# 6. Display results
print("FRANCHISE PERFORMANCE")
print("======================")

print(franchise_summary[[
    "belongs_to_collection.name",
    "candidate_films",
    "total_budget",
    "total_revenue",
    "average_revenue",
    "average_ratio",
    "aggregate_ratio"
]].head(15).to_string(index=False))

print("\nCOLLECTION SUMMARY")
print("==================")
print("Movies with collection membership:", len(franchise_movies))
print("Distinct collections:", franchise_summary.shape[0])

# 7. Save results
franchise_summary.to_csv(
    "data/processed/franchise_analysis.csv",
    index=False
)
