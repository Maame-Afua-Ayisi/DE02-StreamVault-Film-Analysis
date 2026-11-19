
import pandas as pd

# Load the two datasets
movies = pd.read_csv("data/processed/movie_analysis.csv")
directors = pd.read_csv("data/processed/movie_directors.csv")

# Attach movie financial information to each director relationship
director_films = directors.merge(
    movies[["id", "title", "release_year", "budget",
            "revenue", "revenue_budget_ratio"]],
    left_on="movie_id",
    right_on="id",
    how="left",
    validate="many_to_one"
)

# Summarise performance for each director
director_summary = (
    director_films.groupby("director_name")
    .agg(
        candidate_films=("movie_id", "nunique"),
        total_budget=("budget", "sum"),
        total_revenue=("revenue", "sum"),
        average_revenue=("revenue", "mean"),
        average_ratio=("revenue_budget_ratio", "mean")
    )
    .reset_index()
)

# Calculate aggregate revenue-to-budget ratio
director_summary["aggregate_ratio"] = (
    director_summary["total_revenue"] /
    director_summary["total_budget"]
)

# Rank directors by number of candidate films
director_summary = director_summary.sort_values(
    ["candidate_films", "total_revenue"],
    ascending=[False, False]
)

print("DIRECTOR PERFORMANCE")
print("====================")
print(director_summary.head(15).to_string(index=False))

# Save the results
director_summary.to_csv(
    "data/processed/director_analysis.csv",
    index=False
)

print("\nDirector analysis saved successfully.")
