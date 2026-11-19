
import pandas as pd

# Load the extracted movie details.
movies = pd.read_json("data/raw/movie_details.json")

print("MOVIE DATA PROFILE")
print("==================")

# 1. Dataset dimensions
print(f"\nRows: {len(movies)}")
print(f"Columns: {len(movies.columns)}")
print(f"Unique movie IDs: {movies['id'].nunique()}")

# 2. Missing values in important fields
important_fields = [
    "title",
    "release_date",
    "budget",
    "revenue",
    "runtime",
    "genres",
    "belongs_to_collection"
]

print("\nMISSING VALUES")
print(movies[important_fields].isna().sum())

# 3. Zero financial values
print("\nZERO FINANCIAL VALUES")
print("Budget equals zero:", (movies["budget"] == 0).sum())
print("Revenue equals zero:", (movies["revenue"] == 0).sum())

# 4. Inspect movies with zero budget or revenue
print("\nMOVIES WITH ZERO BUDGET")
print(
    movies.loc[
        movies["budget"] == 0,
        ["id", "title", "release_date", "budget", "revenue"]
    ].to_string(index=False)
)

print("\nMOVIES WITH ZERO REVENUE")
print(
    movies.loc[
        movies["revenue"] == 0,
        ["id", "title", "release_date", "budget", "revenue"]
    ].to_string(index=False)
)

# 5. Inspect collection information
print("\nCOLLECTION MEMBERSHIP")
print(
    movies[
        ["id", "title", "belongs_to_collection.id",
         "belongs_to_collection.name"]
    ].head(15).to_string(index=False)
)

# 6. Check duplicate movie records
print("\nDUPLICATE MOVIE IDs")
print(movies[movies["id"].duplicated(keep=False)][["id", "title"]])
