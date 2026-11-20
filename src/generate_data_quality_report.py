
import json
import os
import time
from datetime import datetime, timezone

import pandas as pd

start_time = time.time()

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def load_json(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def load_csv(path):
    if not os.path.exists(path):
        return None

    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


# 1. Load source data
candidate_ids = pd.read_csv("id_list.csv")

movies = load_json("data/raw/movie_details.json")
cast = load_json("data/raw/movie_cast.json")
crew = load_json("data/raw/movie_crew.json")

movie_df = pd.DataFrame(movies)
cast_df = pd.DataFrame(cast)
crew_df = pd.DataFrame(crew)

failed_movies = load_csv("data/raw/failed_movie_requests.csv")
failed_credits = load_csv("data/raw/failed_credit_requests.csv")

analysis = load_csv("data/processed/movie_analysis.csv")
movie_directors = load_csv("data/processed/movie_directors.csv")


# 2. Candidate ID reconciliation
raw_ids = candidate_ids["tmdb_id"].dropna().astype(str).str.strip()
numeric_ids = pd.to_numeric(raw_ids, errors="coerce")

valid_ids = numeric_ids[numeric_ids > 0]

blank_rows = int(candidate_ids["tmdb_id"].isna().sum())
duplicate_rows = int(valid_ids.duplicated().sum())
non_numeric_rows = int(numeric_ids.isna().sum())
non_positive_rows = int(
    (numeric_ids.notna() & (numeric_ids <= 0)).sum()
)


# 3. API extraction statistics
movie_count = len(movie_df)
cast_count = len(cast_df)
crew_count = len(crew_df)

failed_movie_count = 0 if failed_movies is None else len(failed_movies)
failed_credit_count = 0 if failed_credits is None else len(failed_credits)


# 4. Data completeness
financial_fields = [
    "budget",
    "revenue",
    "runtime",
    "release_date",
]

missing_financial = {
    field: int(movie_df[field].isna().sum())
    for field in financial_fields
}

missing_collection = int(
    movie_df["belongs_to_collection.id"].isna().sum()
)


# 5. Relationship validation
movie_ids = set(movie_df["id"])
cast_movie_ids = set(cast_df["movie_id"])
crew_movie_ids = set(crew_df["movie_id"])

orphan_cast = len(cast_movie_ids - movie_ids)
orphan_crew = len(crew_movie_ids - movie_ids)

movies_without_cast = len(movie_ids - cast_movie_ids)
movies_without_crew = len(movie_ids - crew_movie_ids)


# 6. Analysis coverage
analysis_count = 0 if analysis is None else len(analysis)

unique_analysis_movies = (
    0 if analysis is None else analysis["id"].nunique()
)

director_relationships = (
    0 if movie_directors is None else len(movie_directors)
)


# 7. Reporting period coverage
period_files = {
    "Franchise": "data/processed/franchise_period_comparison.csv",
    "Director": "data/processed/director_period_comparison.csv",
    "Cast": "data/processed/cast_period_comparison.csv",
    "Lead actor": "data/processed/lead_actor_period_comparison.csv",
}

period_results = {}

for name, path in period_files.items():
    df = load_csv(path)

    if df is None:
        period_results[name] = ["Not available"]

    elif "period" in df.columns:
        period_results[name] = sorted(
            df["period"].dropna().unique().tolist()
        )

    elif name == "Franchise" and {
        "rank_all_years",
        "rank_2000_onward",
    }.issubset(df.columns):
        period_results[name] = ["All years", "2000 onward"]

    else:
        period_results[name] = ["Not available"]


# 8. Build the Markdown report
report = [
    "# StreamVault Quarterly Data Quality Report",
    "",
    f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
    "",
    "## 1. Executive summary",
    "",
    f"- Candidate rows in source file: {len(candidate_ids)}",
    f"- Successfully retrieved movies: {movie_count}",
    f"- Failed movie requests: {failed_movie_count}",
    f"- Cast records: {cast_count}",
    f"- Crew records: {crew_count}",
    f"- Movies in final analysis: {unique_analysis_movies}",
    "",
    "## 2. Candidate ID reconciliation",
    "",
    f"- Blank IDs: {blank_rows}",
    f"- Duplicate positive numeric occurrences: {duplicate_rows}",
    f"- Non-numeric identifiers: {non_numeric_rows}",
    f"- Non-positive numeric IDs: {non_positive_rows}",
    f"- Unique positive numeric IDs: {valid_ids.nunique()}",
    "",
    "Note: Non-numeric identifiers require a separate identifier-resolution "
    "step. A successfully mapped identifier should be documented in the "
    "reconciliation record.",
    "",
    "## 3. API extraction",
    "",
    f"- Movie records retrieved: {movie_count}",
    f"- Failed movie requests: {failed_movie_count}",
    f"- Cast records retrieved: {cast_count}",
    f"- Crew records retrieved: {crew_count}",
    f"- Failed credit requests: {failed_credit_count}",
    "",
    "## 4. Data completeness",
    "",
]

for field, missing in missing_financial.items():
    report.append(f"- Missing {field}: {missing}")

report.extend([
    f"- Movies without recorded collection membership: {missing_collection}",
    "",
    "## 5. Relationship validation",
    "",
    f"- Cast movie IDs not found in movie details: {orphan_cast}",
    f"- Crew movie IDs not found in movie details: {orphan_crew}",
    f"- Movies without cast records: {movies_without_cast}",
    f"- Movies without crew records: {movies_without_crew}",
    f"- Movie-director relationship records: {director_relationships}",
    "",
    "## 6. Analysis coverage",
    "",
    f"- Rows in movie analysis: {analysis_count}",
    f"- Unique movies in movie analysis: {unique_analysis_movies}",
])

for name, periods in period_results.items():
    report.append(
        f"- {name} reporting periods: {', '.join(periods)}"
    )

report.extend([
    "",
    "## 7. Items requiring attention",
    "",
])

if blank_rows:
    report.append(
        f"- Review {blank_rows} blank candidate ID row(s)."
    )

if duplicate_rows:
    report.append(
        f"- Review {duplicate_rows} duplicate candidate ID occurrence(s)."
    )

if non_numeric_rows:
    report.append(
        f"- Review {non_numeric_rows} non-numeric identifier(s) "
        "and verify their TMDb mappings."
    )

if non_positive_rows:
    report.append(
        f"- Investigate {non_positive_rows} non-positive numeric ID(s)."
    )

if failed_movie_count:
    report.append(
        f"- Investigate {failed_movie_count} failed movie request(s)."
    )

if failed_credit_count:
    report.append(
        f"- Investigate {failed_credit_count} failed credit request(s)."
    )

if missing_collection:
    report.append(
        f"- {missing_collection} movies have no recorded collection "
        "membership; do not automatically classify them as standalone."
    )

if orphan_cast or orphan_crew or movies_without_cast or movies_without_crew:
    report.append(
        "- Investigate movie, cast and crew relationship gaps."
    )

if not any([
    blank_rows,
    duplicate_rows,
    non_numeric_rows,
    non_positive_rows,
    failed_movie_count,
    failed_credit_count,
    orphan_cast,
    orphan_crew,
    movies_without_cast,
    movies_without_crew,
]):
    report.append(
        "- No issues detected by the checks in this report."
    )


# 9. Report limitations
report.extend([
    "",
    "## 8. Limitations",
    "",
    "- A successful API response does not guarantee that every source value is correct.",
    "- Missing collection membership does not prove that a film is standalone.",
    "- Financial values are theatrical budget and revenue, not licensing costs or streaming performance.",
    "- Non-numeric source identifiers require separate verification and documented mapping.",
    "- This report checks available files; it does not independently verify studio rights or source ownership.",
    "- The report covers the candidate list supplied for this run; it cannot identify missing candidates without an independently maintained expected list.",
    "",
    f"Report generation time: {time.time() - start_time:.2f} seconds",
])


# 10. Save the report
output_path = os.path.join(
    REPORT_DIR,
    "data_quality_report.md"
)

with open(output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(report) + "\n")


# 11. Display execution summary
print("DATA QUALITY REPORT GENERATED")
print("=============================")
print("Output:", output_path)
print("Candidate rows:", len(candidate_ids))
print("Movies:", movie_count)
print("Cast records:", cast_count)
print("Crew records:", crew_count)
print("Failed movie requests:", failed_movie_count)
print("Failed credit requests:", failed_credit_count)
print(
    f"Execution time: {time.time() - start_time:.2f} seconds"
)
