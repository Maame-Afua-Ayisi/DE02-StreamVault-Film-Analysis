
import os
import requests

API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise EnvironmentError("TMDB_API_KEY is not configured.")

failed_ids = [
    8471293,
    9412887,
    8471294,
    9412888,
    7733901
]

base_url = "https://api.themoviedb.org/3"

for movie_id in failed_ids:
    response = requests.get(
        f"{base_url}/movie/{movie_id}",
        params={"api_key": API_KEY},
        timeout=30
    )

    print(f"\nTMDb ID: {movie_id}")
    print(f"HTTP status: {response.status_code}")

    try:
        print("API response:", response.json())
    except ValueError:
        print("Response:", response.text[:300])
