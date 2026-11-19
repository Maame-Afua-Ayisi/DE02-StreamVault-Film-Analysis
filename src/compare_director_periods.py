
import pandas as pd

movies = pd.read_csv("data/processed/movie_analysis.csv")
directors = pd.read_csv("data/processed/movie_directors.csv")


def summarise_directors(movie_data):
    # Keep only directors associated with the selected films
    selected_directors = directors.merge(
        movie_data[["id", "release_year", "budget", "revenue",
                    "revenue_budget_ratio"]],
        left_on="movie_id",
        right_on="id",
        how="inner",
        validate="many_to_one"
    )

    summary = (
        selected_directors.groupby("director_name")
        .agg(
            candidate_films=("movie_id", "nunique"),
            total_budget=("budget", "sum"),
            total_revenue=("revenue", "sum"),
            average_revenue=("revenue", "mean"),
            average_ratio=("revenue_budget_ratio", "mean")
        )
        .reset_index()
    )

    summary["aggregate_ratio"] = (
        summary["total_revenue"] / summary["total_budget"]
    )

    return summary.sort_values(
        "total_revenue", ascending=False
    )


# Analyse all release years
all_years = summarise_directors(movies)

# Analyse films released from 2000 onward
recent_movies = movies.loc[
    movies["release_year"] >= 2000
].copy()

recent_years = summarise_directors(recent_movies)

# Add period labels
all_years["period"] = "All years"
recent_years["period"] = "2000 onward"

# Combine both summaries
comparison = pd.concat(
    [all_years, recent_years],
    ignore_index=True
)

# Show the top 15 directors in each period
print("TOP DIRECTORS BY TOTAL REVENUE")
print("==============================")

for period in ["All years", "2000 onward"]:
    print(f"\n{period.upper()}")
    print("-" * len(period))

    print(
        comparison.loc[
            comparison["period"] == period
        ].head(15).to_string(index=False)
    )

# Save results
comparison.to_csv(
    "data/processed/director_period_comparison.csv",
    index=False
)

print("\nDirector period comparison saved successfully.")
