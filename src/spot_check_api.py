
import os
import time
import requests
import pandas as pd

# 1. Configuration
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

if not API_KEY:
    raise EnvironmentError("TMDB_API_KEY is not configured.")

# 2. Load locally saved data
movies = pd.read_json("data/raw/movie_details.json")
cast = pd.read_json("data/raw/movie_cast.json")
crew = pd.read_json("data/raw/movie_crew.json")

# Select five reproducible sample movies
sample = movies.sample(
    n=min(5, len(movies)),
    random_state=42
)

# Fields to compare against TMDb
fields = [
    "title",
    "release_date",
    "budget",
    "revenue",
    "runtime"
]

numeric_fields = {"budget", "revenue", "runtime"}

session = requests.Session()
session.params = {"api_key": API_KEY}

results = []
start_time = time.perf_counter()


# 3. Normalise values before comparing
def normalise(value, field):
    if pd.isna(value):
        return None

    if field in numeric_fields:
        return int(value)

    return str(value)


# 4. Check each sampled movie
for _, local_movie in sample.iterrows():
    movie_id = int(local_movie["id"])

    print(f"Checking movie ID: {movie_id}")

    try:
        # Retrieve fresh movie details
        movie_response = session.get(
            f"{BASE_URL}/movie/{movie_id}",
            timeout=30
        )
        movie_response.raise_for_status()
        api_movie = movie_response.json()

        # Retrieve fresh credits
        credits_response = session.get(
            f"{BASE_URL}/movie/{movie_id}/credits",
            timeout=30
        )
        credits_response.raise_for_status()
        api_credits = credits_response.json()

        # Compare movie details
        for field in fields:
            local_value = normalise(
                local_movie[field],
                field
            )
            api_value = normalise(
                api_movie.get(field),
                field
            )

            results.append({
                "movie_id": movie_id,
                "check": field,
                "result": (
                    "PASS"
                    if local_value == api_value
                    else "MISMATCH"
                ),
                "local_value": local_value,
                "api_value": api_value
            })

        # Compare cast credit IDs
        local_cast = cast.loc[
            cast["movie_id"] == movie_id,
            "credit_id"
        ].dropna().astype(str)

        api_cast = {
            str(person["credit_id"])
            for person in api_credits.get("cast", [])
            if person.get("credit_id")
        }

        local_cast_ids = set(local_cast)

        results.append({
            "movie_id": movie_id,
            "check": "cast_credit_ids",
            "result": (
                "PASS"
                if local_cast_ids == api_cast
                else "MISMATCH"
            ),
            "local_value": len(local_cast_ids),
            "api_value": len(api_cast)
        })

        # Compare crew credit IDs
        local_crew = crew.loc[
            crew["movie_id"] == movie_id,
            "credit_id"
        ].dropna().astype(str)

        api_crew = {
            str(person["credit_id"])
            for person in api_credits.get("crew", [])
            if person.get("credit_id")
        }

        local_crew_ids = set(local_crew)

        results.append({
            "movie_id": movie_id,
            "check": "crew_credit_ids",
            "result": (
                "PASS"
                if local_crew_ids == api_crew
                else "MISMATCH"
            ),
            "local_value": len(local_crew_ids),
            "api_value": len(api_crew)
        })

    except requests.RequestException as error:
        results.append({
            "movie_id": movie_id,
            "check": "API request",
            "result": "ERROR",
            "local_value": None,
            "api_value": str(error)
        })


# 5. Produce the spot-check report
report = pd.DataFrame(results)

os.makedirs("reports", exist_ok=True)

elapsed_time = time.perf_counter() - start_time

passed = (report["result"] == "PASS").sum()
mismatches = (report["result"] == "MISMATCH").sum()
errors = (report["result"] == "ERROR").sum()

with open(
    "reports/api_spot_check.md",
    "w",
    encoding="utf-8"
) as file:
    file.write("# TMDb API Spot-Check Report\n\n")
    file.write(f"- Movies sampled: {len(sample)}\n")
    file.write(f"- Checks passed: {passed}\n")
    file.write(f"- Mismatches: {mismatches}\n")
    file.write(f"- API errors: {errors}\n")
    file.write(f"- Execution time: {elapsed_time:.2f} seconds\n\n")

    file.write("## Detailed results\n\n")
    file.write("```text\n")
    file.write(report.to_string(index=False))
    file.write("\n```\n")


# 6. Display summary
print("\nAPI SPOT-CHECK REPORT")
print("=====================")
print(f"Movies sampled: {len(sample)}")
print(f"Checks passed: {passed}")
print(f"Mismatches: {mismatches}")
print(f"API errors: {errors}")
print(f"Execution time: {elapsed_time:.2f} seconds")

print("\nDetailed report saved to reports/api_spot_check.md")

session.close()
