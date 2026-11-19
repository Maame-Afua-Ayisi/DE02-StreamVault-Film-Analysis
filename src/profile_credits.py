
import pandas as pd

# Load extracted credits
cast = pd.read_json("data/raw/movie_cast.json")
crew = pd.read_json("data/raw/movie_crew.json")

print("CAST PROFILE")
print("============")
print("Rows:", len(cast))
print("Columns:", len(cast.columns))
print("Unique movies:", cast["movie_id"].nunique())
print("Unique people:", cast["id"].nunique())

print("\nMissing cast values:")
print(cast[["movie_id", "id", "name", "character"]].isna().sum())

print("\nCREW PROFILE")
print("============")
print("Rows:", len(crew))
print("Columns:", len(crew.columns))
print("Unique movies:", crew["movie_id"].nunique())
print("Unique people:", crew["id"].nunique())

print("\nMissing crew values:")
print(crew[["movie_id", "id", "name", "department", "job"]].isna().sum())

print("\nTOP FIVE CAST MEMBERS BY NUMBER OF MOVIES")
print(
    cast.groupby(["id", "name"])["movie_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTOP FIVE DIRECTORS BY NUMBER OF MOVIES")
directors = crew[crew["job"] == "Director"]

print(
    directors.groupby(["id", "name"])["movie_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(5)
)
