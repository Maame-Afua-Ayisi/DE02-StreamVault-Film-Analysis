
import os
import time
import requests
import pandas as pd

# 1. Configuration
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

if not API_KEY:
    raise EnvironmentError("TMDB_API_KEY is not configured.")

# 2. Load the original candidate list
df = pd.read_csv("id_list.csv", dtype={"tmdb_id": "string"})

# 3. Prepare the identifiers
ids = df["tmdb_id"].str.strip()
numeric_ids = pd.to_numeric(ids, errors="coerce")

# Keep only positive, whole-number TMDb IDs.
valid_mask = (
    numeric_ids.notna()
    & (numeric_ids > 0)
    & (numeric_ids % 1 == 0)
)

valid_ids = numeric_ids.loc[valid_mask].astype("int64")

# 4. Remove exact duplicate IDs for API extraction.
# The original CSV remains unchanged.
unique_ids = valid_ids.drop_duplicates()

# 5. Prepare the API request
session = requests.Session()
session.params = {"api_key": API_KEY}

movie_records = []
failed_records = []

start_time = time.perf_counter()

# 6. Retrieve each movie's details
for movie_id in unique_ids:
    url = f"{BASE_URL}/movie/{movie_id}"

    try:
        response = session.get(url, timeout=30)

        if response.status_code == 404:
            failed_records.append({
                "tmdb_id": movie_id,
                "status": "not_found",
                "http_status": 404
            })
            continue

        response.raise_for_status()

        movie = response.json()
        movie_records.append(movie)

    except requests.RequestException as error:
        failed_records.append({
            "tmdb_id": movie_id,
            "status": str(error),
            "http_status": getattr(
                getattr(error, "response", None),
                "status_code",
                None
            )
        })

end_time = time.perf_counter()

# 7. Save the retrieved data
movies = pd.json_normalize(movie_records)

os.makedirs("data/raw", exist_ok=True)

movies.to_json(
    "data/raw/movie_details.json",
    orient="records",
    indent=2
)

pd.DataFrame(failed_records).to_csv(
    "data/raw/failed_movie_requests.csv",
    index=False
)

# 8. Report the extraction results
print("\nMOVIE EXTRACTION REPORT")
print("-----------------------")
print(f"Original CSV rows: {len(df)}")
print(f"Valid numeric ID rows: {len(valid_ids)}")
print(f"Unique IDs requested: {len(unique_ids)}")
print(f"Movies successfully retrieved: {len(movies)}")
print(f"Failed requests: {len(failed_records)}")
print(f"Execution time: {end_time - start_time:.2f} seconds")
