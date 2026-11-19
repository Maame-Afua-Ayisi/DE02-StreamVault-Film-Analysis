
import pandas as pd

# Load the movie and cast datasets
movies = pd.read_csv("data/processed/movie_analysis.csv")
cast = pd.read_json("data/raw/movie_cast.json")

# Keep the cast columns needed for the analysis
cast = cast[["movie_id", "id", "name", "character", "order"]]

# Attach movie financial information to each cast member's film
cast_films = cast.merge(
    movies[["id", "title", "release_year", "budget",
            "revenue", "revenue_budget_ratio"]],
    left_on="movie_id",
    right_on="id",
    how="inner",
    validate="many_to_one"
)

# Summarise performance for each actor
cast_summary = (
    cast_films.groupby(["id_x", "name"])
    .agg(
        candidate_films=("movie_id", "nunique"),
        total_budget=("budget", "sum"),
        total_revenue=("revenue", "sum"),
        average_revenue=("revenue", "mean"),
        average_ratio=("revenue_budget_ratio", "mean")
    )
    .reset_index()
)
cast_summary = cast_summary.rename(
    columns={"id_x": "actor_id"}
)
# Calculate aggregate revenue-to-budget ratio
cast_summary["aggregate_ratio"] = (
    cast_summary["total_revenue"] /
    cast_summary["total_budget"]
)

# Rank actors by number of candidate films
cast_summary = cast_summary.sort_values(
    ["candidate_films", "total_revenue"],
    ascending=[False, False]
)

print("CAST MEMBER PERFORMANCE")
print("=======================")
print(cast_summary.head(20).to_string(index=False))

# Save the complete results
cast_summary.to_csv(
    "data/processed/cast_analysis.csv",
    index=False
)

print("\nCast analysis saved successfully.")
