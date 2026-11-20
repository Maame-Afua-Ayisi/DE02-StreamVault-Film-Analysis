
import os
import time
import requests
import pandas as pd

# 1. Configuration
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

MAX_ATTEMPTS = 4
BASE_DELAY = 1

if not API_KEY:
    raise EnvironmentError("TMDB_API_KEY is not configured.")


# 2. Reusable request function with retry and backoff
def request_with_retry(session, url):
    for attempt in range(MAX_ATTEMPTS):
        try:
            response = session.get(url, timeout=30)

        except (requests.Timeout, requests.ConnectionError):
            if attempt == MAX_ATTEMPTS - 1:
                raise

            delay = BASE_DELAY * (2 ** attempt)

            print(
                f"Connection problem. "
                f"Retrying in {delay} seconds..."
            )

            time.sleep(delay)
            continue

        # Retry rate-limit and temporary server errors.
        if response.status_code == 429 or 500 <= response.status_code < 600:
            if attempt == MAX_ATTEMPTS - 1:
                return response

            retry_after = response.headers.get("Retry-After")

            if retry_after:
                try:
                    delay = float(retry_after)
                except ValueError:
                    delay = BASE_DELAY * (2 ** attempt)
            else:
                delay = BASE_DELAY * (2 ** attempt)

            print(
                f"HTTP {response.status_code}. "
                f"Retrying in {delay} seconds..."
            )

            response.close()
            time.sleep(delay)
            continue

        # Return successful responses and permanent errors.
        return response

    raise RuntimeError("Request attempts exhausted.")


# 3. Load successfully retrieved movie IDs
movies = pd.read_json("data/raw/movie_details.json")
movie_ids = movies["id"].drop_duplicates().tolist()

print(f"Movies to retrieve credits for: {len(movie_ids)}")


# 4. Prepare API session
session = requests.Session()

# Automatically include the API key in every request.
session.params = {"api_key": API_KEY}

cast_records = []
crew_records = []
failed_records = []

start_time = time.perf_counter()


# 5. Retrieve credits for each movie
for movie_id in movie_ids:
    url = f"{BASE_URL}/movie/{movie_id}/credits"

    try:
        response = request_with_retry(session, url)

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


# 6. Convert records into DataFrames
cast_df = pd.DataFrame(cast_records)
crew_df = pd.DataFrame(crew_records)
failed_df = pd.DataFrame(failed_records)


# 7. Create output directory
os.makedirs("data/raw", exist_ok=True)


# 8. Save extracted data
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


# 9. Measure execution time
elapsed_time = time.perf_counter() - start_time

print("\nCREDITS EXTRACTION REPORT")
print("=========================")
print(f"Movies processed: {len(movie_ids)}")
print(f"Cast records: {len(cast_df)}")
print(f"Crew records: {len(crew_df)}")
print(f"Failed requests: {len(failed_df)}")
print(f"Execution time: {elapsed_time:.2f} seconds")

session.close()
