
import pandas as pd

# Load datasets
movies = pd.read_json("data/raw/movie_details.json")
cast = pd.read_json("data/raw/movie_cast.json")
crew = pd.read_json("data/raw/movie_crew.json")

# Get unique movie IDs
movie_ids = set(movies["id"])
cast_movie_ids = set(cast["movie_id"])
crew_movie_ids = set(crew["movie_id"])

# Check relationships
print("RELATIONSHIP VALIDATION")
print("========================")

print(
    "Cast movie IDs missing from movie details:",
    len(cast_movie_ids - movie_ids)
)

print(
    "Crew movie IDs missing from movie details:",
    len(crew_movie_ids - movie_ids)
)

print(
    "Movies without cast records:",
    len(movie_ids - cast_movie_ids)
)

print(
    "Movies without crew records:",
    len(movie_ids - crew_movie_ids)
)

# Check duplicate movie IDs
print("\nDUPLICATE MOVIE RECORDS")
print("Movies:", movies["id"].duplicated().sum())

# Check duplicate credit records
print("Cast:", cast.duplicated(["movie_id", "id", "credit_id"]).sum())
print("Crew:", crew.duplicated(["movie_id", "id", "credit_id"]).sum())
