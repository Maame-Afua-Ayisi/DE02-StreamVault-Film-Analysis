# 500-Candidate Data Quality Report Benchmark

Generated: 2026-11-20 10:06 UTC

## Test purpose

Measure the time required to run the project's actual data-quality report generator against a synthetic dataset representing 500 movies.

## Test dataset

| Measure | Records |
|---|---:|
| Candidate rows | 500 |
| Movie detail records | 500 |
| Cast records | 35,215 |
| Crew records | 111,781 |
| Movie analysis rows | 500 |
| Movie-director relationships | 545 |

## Results

- Warm-up runs (excluded): 1
- Measured runs: 5
- Run times: 1.408s, 1.631s, 1.645s, 1.468s, 1.575s
- Fastest run: 1.408s
- Slowest run: 1.645s
- Median run time: 1.575s

## Test environment

- Python: 3.15.2
- Pandas: 3.1.1
- Operating system: Windows-11-10.0.26300-SP0

## Method and limitations

- The benchmark runs `src/generate_data_quality_report.py` itself.
- The test creates 500 synthetic movie records by cycling through the project's existing movie records and assigning synthetic IDs.
- Cast, crew and movie-director relationships are copied with the synthetic movie IDs so the report processes a larger related dataset.
- The test uses a temporary copy of the required project files. It does not modify the original data files or generated report.
- No TMDb API requests are made; this measures local report generation, not API extraction or the complete analysis pipeline.
- Synthetic records demonstrate processing capacity, not the accuracy or completeness of 500 independently sourced films.
- Timings depend on the computer and its current workload. Re-run this script on the target laptop to obtain that machine's measurement.
