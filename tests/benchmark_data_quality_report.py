"""Benchmark the data-quality report with a reproducible synthetic 500-movie dataset.

Run from the repository root:
    python tests/benchmark_data_quality_report.py

The test copies the required project inputs into a temporary directory, expands
movie, cast and crew records to 500 synthetic movies, and runs the real report
 generator there. It does not call the TMDb API or modify the project's source
or analysis data files.
"""

from __future__ import annotations

import copy
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TARGET_MOVIES = 500
MEASURED_RUNS = 5
SYNTHETIC_ID_START = 9_000_000
GENERATOR = ROOT / "src" / "generate_data_quality_report.py"

REQUIRED_FILES = [
    "id_list.csv",
    "data/raw/movie_details.json",
    "data/raw/movie_cast.json",
    "data/raw/movie_crew.json",
    "data/raw/failed_movie_requests.csv",
    "data/raw/failed_credit_requests.csv",
    "data/processed/movie_analysis.csv",
    "data/processed/movie_directors.csv",
    "data/processed/franchise_period_comparison.csv",
    "data/processed/director_period_comparison.csv",
    "data/processed/cast_period_comparison.csv",
    "data/processed/lead_actor_period_comparison.csv",
]


def read_json(path: Path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(value, file)


def prepare_synthetic_project(workspace: Path) -> dict[str, int]:
    """Build an isolated project copy containing 500 synthetic movie records."""
    for relative in REQUIRED_FILES:
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(
                f"Required input is missing: {relative}. "
                "Run the project pipeline before benchmarking."
            )
        destination = workspace / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    if not GENERATOR.is_file():
        raise FileNotFoundError(f"Report generator not found: {GENERATOR}")
    generator_copy = workspace / "src" / GENERATOR.name
    generator_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(GENERATOR, generator_copy)

    # The synthetic fixture contains complete records for all 500 generated
    # movies, so its failed-request logs should be empty rather than inheriting
    # failures from the original 112-movie extraction.
    pd.DataFrame(columns=["movie_id", "status_code", "error"]).to_csv(
        workspace / "data/raw/failed_movie_requests.csv", index=False
    )
    pd.DataFrame(columns=["movie_id", "status_code", "error"]).to_csv(
        workspace / "data/raw/failed_credit_requests.csv", index=False
    )

    original_movies = read_json(ROOT / "data/raw/movie_details.json")
    original_cast = read_json(ROOT / "data/raw/movie_cast.json")
    original_crew = read_json(ROOT / "data/raw/movie_crew.json")

    if not original_movies:
        raise ValueError("The source movie-details file contains no movies.")

    cast_by_movie: dict[int, list[dict]] = {}
    for record in original_cast:
        cast_by_movie.setdefault(int(record["movie_id"]), []).append(record)

    crew_by_movie: dict[int, list[dict]] = {}
    for record in original_crew:
        crew_by_movie.setdefault(int(record["movie_id"]), []).append(record)

    directors = pd.read_csv(ROOT / "data/processed/movie_directors.csv")
    directors_by_movie = {
        int(movie_id): group.to_dict("records")
        for movie_id, group in directors.groupby("movie_id")
    }

    synthetic_movies = []
    synthetic_cast = []
    synthetic_crew = []
    synthetic_directors = []
    synthetic_movie_analysis = []

    analysis = pd.read_csv(ROOT / "data/processed/movie_analysis.csv")
    analysis_by_id = {
        int(movie_id): row
        for movie_id, row in analysis.set_index("id").iterrows()
    }

    for index in range(TARGET_MOVIES):
        source_movie = original_movies[index % len(original_movies)]
        source_id = int(source_movie["id"])
        synthetic_id = SYNTHETIC_ID_START + index

        movie_copy = copy.deepcopy(source_movie)
        movie_copy["id"] = synthetic_id
        synthetic_movies.append(movie_copy)

        for record in cast_by_movie.get(source_id, []):
            row = copy.deepcopy(record)
            row["movie_id"] = synthetic_id
            synthetic_cast.append(row)

        for record in crew_by_movie.get(source_id, []):
            row = copy.deepcopy(record)
            row["movie_id"] = synthetic_id
            synthetic_crew.append(row)

        for record in directors_by_movie.get(source_id, []):
            row = dict(record)
            row["movie_id"] = synthetic_id
            synthetic_directors.append(row)

        if source_id in analysis_by_id:
            row = analysis_by_id[source_id].to_dict()
            row["id"] = synthetic_id
            if "movie_id" in row:
                row["movie_id"] = synthetic_id
            synthetic_movie_analysis.append(row)

    write_json(workspace / "data/raw/movie_details.json", synthetic_movies)
    write_json(workspace / "data/raw/movie_cast.json", synthetic_cast)
    write_json(workspace / "data/raw/movie_crew.json", synthetic_crew)

    # One synthetic candidate ID per synthetic movie; no live API calls occur.
    pd.DataFrame({
        "tmdb_id": [SYNTHETIC_ID_START + i for i in range(TARGET_MOVIES)]
    }).to_csv(workspace / "id_list.csv", index=False)

    pd.DataFrame(synthetic_movie_analysis).to_csv(
        workspace / "data/processed/movie_analysis.csv", index=False
    )
    pd.DataFrame(synthetic_directors).to_csv(
        workspace / "data/processed/movie_directors.csv", index=False
    )

    return {
        "candidate_rows": TARGET_MOVIES,
        "movie_records": len(synthetic_movies),
        "cast_records": len(synthetic_cast),
        "crew_records": len(synthetic_crew),
        "movie_analysis_rows": len(synthetic_movie_analysis),
        "movie_director_relationships": len(synthetic_directors),
    }


def run_report(workspace: Path) -> float:
    """Run the actual report generator in the isolated synthetic project."""
    command = [sys.executable, str(workspace / "src" / GENERATOR.name)]
    started = time.perf_counter()
    result = subprocess.run(
        command,
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    elapsed = time.perf_counter() - started

    if result.returncode != 0:
        raise RuntimeError(
            "The report generator failed in the benchmark workspace.\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    generated_report = workspace / "reports" / "data_quality_report.md"
    if not generated_report.is_file():
        raise RuntimeError("The report generator did not create its output file.")

    report_text = generated_report.read_text(encoding="utf-8")
    required_checks = [
        "Candidate rows in source file: 500",
        "Successfully retrieved movies: 500",
        "Movies in final analysis: 500",
    ]
    for expected in required_checks:
        if expected not in report_text:
            raise RuntimeError(
                "Generated report did not contain the expected benchmark result: "
                f"{expected!r}"
            )

    return elapsed


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="streamvault_500_benchmark_") as temp:
        workspace = Path(temp)
        counts = prepare_synthetic_project(workspace)

        # One warm-up run is excluded from the five measured runs.
        run_report(workspace)
        timings = [run_report(workspace) for _ in range(MEASURED_RUNS)]

    median_seconds = float(pd.Series(timings).median())
    minimum_seconds = min(timings)
    maximum_seconds = max(timings)

    lines = [
        "# 500-Candidate Data Quality Report Benchmark",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Test purpose",
        "",
        "Measure the time required to run the project's actual data-quality "
        "report generator against a synthetic dataset representing 500 movies.",
        "",
        "## Test dataset",
        "",
        "| Measure | Records |",
        "|---|---:|",
        f"| Candidate rows | {counts['candidate_rows']:,} |",
        f"| Movie detail records | {counts['movie_records']:,} |",
        f"| Cast records | {counts['cast_records']:,} |",
        f"| Crew records | {counts['crew_records']:,} |",
        f"| Movie analysis rows | {counts['movie_analysis_rows']:,} |",
        f"| Movie-director relationships | {counts['movie_director_relationships']:,} |",
        "",
        "## Results",
        "",
        f"- Warm-up runs (excluded): 1",
        f"- Measured runs: {MEASURED_RUNS}",
        "- Run times: " + ", ".join(f"{value:.3f}s" for value in timings),
        f"- Fastest run: {minimum_seconds:.3f}s",
        f"- Slowest run: {maximum_seconds:.3f}s",
        f"- Median run time: {median_seconds:.3f}s",
        "",
        "## Test environment",
        "",
        f"- Python: {sys.version.split()[0]}",
        f"- Pandas: {pd.__version__}",
        f"- Operating system: {platform.platform()}",
        "",
        "## Method and limitations",
        "",
        "- The benchmark runs `src/generate_data_quality_report.py` itself.",
        "- The test creates 500 synthetic movie records by cycling through "
        "the project's existing movie records and assigning synthetic IDs.",
        "- Cast, crew and movie-director relationships are copied with the "
        "synthetic movie IDs so the report processes a larger related dataset.",
        "- The test uses a temporary copy of the required project files. It "
        "does not modify the original data files or generated report.",
        "- No TMDb API requests are made; this measures local report generation, "
        "not API extraction or the complete analysis pipeline.",
        "- Synthetic records demonstrate processing capacity, not the accuracy "
        "or completeness of 500 independently sourced films.",
        "- Timings depend on the computer and its current workload. Re-run this "
        "script on the target laptop to obtain that machine's measurement.",
        "",
    ]

    output = ROOT / "reports" / "benchmark_500_candidates.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")

    print("500-CANDIDATE BENCHMARK COMPLETED")
    print("=================================")
    for name, value in counts.items():
        print(f"{name.replace('_', ' ').title()}: {value:,}")
    print("Measured runs:", ", ".join(f"{value:.3f}s" for value in timings))
    print(f"Median: {median_seconds:.3f}s")
    print(f"Fastest: {minimum_seconds:.3f}s")
    print(f"Slowest: {maximum_seconds:.3f}s")
    print("Report saved to:", output.relative_to(ROOT))


if __name__ == "__main__":
    main()
