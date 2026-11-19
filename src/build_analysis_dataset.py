
import os
import time
import pandas as pd

start_time = time.perf_counter()

# 1. Load source datasets
movies = pd.read_json("data/raw/movie_details.json")
crew = pd.read_json("data/raw/movie_crew.json")

# 2. Extract director credits
directors = crew.loc[
    crew["job"] == "Director",
    ["movie_id", "id", "name"]
].copy()

directors = directors.rename(columns={
    "id": "director_id",
    "name": "director_name"
})

# 3. Build a separate movie-director table
movie_directors = directors.drop_duplicates(
    subset=["movie_id", "director_id"]
)

# 4. Summarise director information at movie level
director_summary = (
    movie_directors.groupby("movie_id")
    .agg(
        director_count=("director_id", "nunique"),
        director_names=("director_name", lambda x: "; ".join(x))
    )
    .reset_index()
)

# 5. Add director information to movie details
analysis = movies.merge(
    director_summary,
    left_on="id",
    right_on="movie_id",
    how="left",
    validate="one_to_one"
)

# 6. Create release year
analysis["release_date"] = pd.to_datetime(
    analysis["release_date"]
)

analysis["release_year"] = analysis["release_date"].dt.year

# 7. Calculate financial measures
analysis["revenue_minus_budget"] = (
    analysis["revenue"] - analysis["budget"]
)

analysis["revenue_budget_ratio"] = (
    analysis["revenue"] / analysis["budget"]
)

# 8. Save outputs
os.makedirs("data/processed", exist_ok=True)

analysis.to_csv(
    "data/processed/movie_analysis.csv",
    index=False
)

movie_directors.to_csv(
    "data/processed/movie_directors.csv",
    index=False
)

# 9. Validate output grain
print("DATASET VALIDATION")
print("==================")
print("Movie analysis rows:", len(analysis))
print("Unique movie IDs:", analysis["id"].nunique())
print("Movie-director rows:", len(movie_directors))
print("Movies with multiple directors:",
      (analysis["director_count"] > 1).sum())

print("\nFIRST TEN MOVIES")
print(
    analysis[
        ["title", "release_year", "director_names",
         "budget", "revenue", "revenue_budget_ratio"]
    ].head(10).to_string(index=False)
)

elapsed_time = time.perf_counter() - start_time

print(f"\nExecution time: {elapsed_time:.2f} seconds")
