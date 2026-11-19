import pandas as pd
import time

start_time = time.perf_counter()

# Load the movie and cast datasets
movies = pd.read_csv("data/processed/movie_analysis.csv")
cast = pd.read_json("data/raw/movie_cast.json")

# Keep the cast columns needed for the analysis
cast = cast[["movie_id", "id", "name"]]

# Attach movie information to each cast member
cast_films = cast.merge(
    movies[["id", "title", "release_year", "budget",
            "revenue", "revenue_budget_ratio"]],
    left_on="movie_id",
    right_on="id",
    how="inner",
    validate="many_to_one"
)

# Keep one record per actor per movie
cast_films = cast_films.drop_duplicates(
    subset=["id_x", "movie_id"]
)

# Function to summarise cast performance
def summarise_cast(data):
    cast_summary = (
        data.groupby(["id_x", "name"])
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
    cast_summary["aggregate_ratio"] = (
        cast_summary["total_revenue"] /
        cast_summary["total_budget"]
    )

    # Rename actor ID column
    cast_summary = cast_summary.rename(
        columns={"id_x": "actor_id"}
    )

    # Rank actors by number of candidate films
    cast_summary = cast_summary.sort_values(
        ["candidate_films", "total_revenue"],
        ascending=[False, False]
    )

    return cast_summary


# Analyse all candidate films
all_years = summarise_cast(cast_films)

# Analyse films released from 2000 onward
recent_movies = cast_films.loc[
    cast_films["release_year"] >= 2000
].copy()

recent_years = summarise_cast(recent_movies)

# Add period labels
all_years["period"] = "All years"
recent_years["period"] = "2000 onward"

# Combine both analyses
comparison = pd.concat(
    [all_years, recent_years],
    ignore_index=True
)

# Display the top 20 actors in each period
print("CAST PERFORMANCE: ALL YEARS")
print("============================")
print(
    all_years.head(20).to_string(index=False)
)

print("\nCAST PERFORMANCE: 2000 ONWARD")
print("==============================")
print(
    recent_years.head(20).to_string(index=False)
)

# Display dataset summary
print("\nPERIOD SUMMARY")
print("==============")
print("All-years candidate films:", cast_films["movie_id"].nunique())
print("2000-onward candidate films:", recent_movies["movie_id"].nunique())
print("All-years cast members:", all_years["actor_id"].nunique())
print("2000-onward cast members:", recent_years["actor_id"].nunique())

# Save complete results
all_years.to_csv(
    "data/processed/cast_analysis_all_years.csv",
    index=False
)

recent_years.to_csv(
    "data/processed/cast_analysis_2000_onward.csv",
    index=False
)

comparison.to_csv(
    "data/processed/cast_period_comparison.csv",
    index=False
)

# Measure execution time
end_time = time.perf_counter()

print("\nExecution time:", round(end_time - start_time, 2), "seconds")
print("Cast period comparison saved successfully.")
