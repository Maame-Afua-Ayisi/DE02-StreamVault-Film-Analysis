import pandas as pd
import time

start_time = time.time()

# Load the cast and movie datasets
cast = pd.read_json("data/raw/movie_cast.json")
movies = pd.read_csv("data/processed/movie_analysis.csv")

# Select the five highest-billed cast members in each movie
lead_cast = cast[cast["order"] <= 4].copy()

# Keep only the columns needed
lead_cast = lead_cast[
    ["movie_id", "id", "name", "order"]
]

# Attach movie financial information
analysis = lead_cast.merge(
    movies[["id", "title", "release_year", "budget", "revenue",
            "revenue_budget_ratio"]],
    left_on="movie_id",
    right_on="id",
    how="inner",
    validate="many_to_one"
)

def analyse_period(data, period_name):
    result = (
        data.groupby(["id_x", "name"], as_index=False)
        .agg(
            candidate_films=("movie_id", "nunique"),
            total_revenue=("revenue", "sum"),
            average_revenue=("revenue", "mean"),
            average_ratio=("revenue_budget_ratio", "mean"),
            total_budget=("budget", "sum")
        )
    )

    result["aggregate_ratio"] = (
        result["total_revenue"] / result["total_budget"]
    )

    result["period"] = period_name

    return result.sort_values(
        ["candidate_films", "total_revenue"],
        ascending=[False, False]
    )

# Analyse both required time periods
all_years = analyse_period(analysis, "All years")

recent = analysis[
    analysis["release_year"] >= 2000
]
recent_years = analyse_period(recent, "2000 onward")

# Combine and save the results
final = pd.concat(
    [all_years, recent_years],
    ignore_index=True
)

final = final.rename(columns={"id_x": "actor_id"})

final.to_csv(
    "data/processed/lead_actor_period_comparison.csv",
    index=False
)

print("TOP-BILLED ACTOR ANALYSIS")
print("=========================")
print(final.head(20).to_string(index=False))

print("\nMovies analysed:", analysis["movie_id"].nunique())
print("Top-billed cast records:", len(analysis))
print(f"Execution time: {time.time() - start_time:.2f} seconds")
