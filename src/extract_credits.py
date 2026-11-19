
import os
import json
import time
import requests
import pandas as pd

# 1. Load API key
api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not configured.")

# 2. Load successfully retrieved movie IDs
movies = pd.read_json("data/raw/movie_details.json")

movie_ids = movies["id"].drop_duplicates().tolist()

print(f"Movies to retrieve credits for: {len(movie_ids)}")

# 3. Prepare API session
session = requests.Session()

cast_records = []
crew_records = []
failed_records = []

start_time = time.perf_counter()

# 4. Retrieve credits for each movie
for movie_id in movie_ids:

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

    try:
        response = session.get(
            url,
            params={"api_key": api_key},
            timeout=30
        )

        if response.status_code != 200:
            failed_records.append({
                "movie_id": movie_id,
                "status_code": response.status_code
            })
            continue

        data = response.json()

        # Add movie ID to every cast record
        for person in data.get("cast", []):
            cast_records.append({
                "movie_id": movie_id,
                **person
            })

        # Add movie ID to every crew record
        for person in data.get("crew", []):
            crew_records.append({
                "movie_id": movie_id,
                **person
            })

    except requests.RequestException as error:
        failed_records.append({
            "movie_id": movie_id,
            "error": str(error)
        })

# 5. Convert records into DataFrames
cast_df = pd.DataFrame(cast_records)
crew_df = pd.DataFrame(crew_records)
failed_df = pd.DataFrame(failed_records)

# 6. Create output directory
os.makedirs("data/raw", exist_ok=True)

# 7. Save extracted data
cast_df.to_json(
    "data/raw/movie_cast.json",
    orient="records",
    indent=2
)

crew_df.to_json(
    "data/raw/movie_crew.json",
    orient="records",
    indent=2
)

failed_df.to_csv(
    "data/raw/failed_credit_requests.csv",
    index=False
)

# 8. Measure execution time
elapsed_time = time.perf_counter() - start_time

print("\nCREDITS EXTRACTION REPORT")
print("=========================")
print(f"Movies processed: {len(movie_ids)}")
print(f"Cast records: {len(cast_df)}")
print(f"Crew records: {len(crew_df)}")
print(f"Failed requests: {len(failed_df)}")
print(f"Execution time: {elapsed_time:.2f} seconds")
