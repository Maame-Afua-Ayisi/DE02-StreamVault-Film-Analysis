# StreamVault Film Licensing Analysis

## 1. Project Overview

This project analyses films that StreamVault, a streaming service, is considering for licensing.

The aim is to help the company decide which films and franchises deserve further attention before committing its $14 million licensing budget.

The analysis examines:

- Historical financial performance across film franchises.
- Films with no recorded franchise membership.
- Directors and actors appearing across the candidate films.
- Differences in results when older films are excluded.
- Data quality issues that could affect the reliability of the analysis.

Film information is retrieved from The Movie Database (TMDb).

The project is designed to support repeatable analysis when StreamVault receives larger candidate lists.

## 2. Project Structure

```text
DE02-StreamVault-Film-Analysis/
│
├── data/
│   ├── raw/             Original information retrieved from TMDb
│   └── processed/       Prepared information used for analysis
│
├── decisions/           Architecture Decision Records (ADRs)
├── docs/                Data reconciliation and quality documentation
├── reports/             Generated reports and analysis evidence
├── src/                 Python scripts
├── tests/               Performance testing
│
├── id_list.csv
├── client_memo.md
├── deal_notes.md
├── improvement.md
├── requirements.txt
└── README.md
```

## 3. Tools and Technologies

- **Python:** Used for data extraction, preparation, validation and analysis.
- **Pandas:** Used to organise, clean and analyse tabular data.
- **Requests:** Used to retrieve information from the TMDb API.
- **TMDb API:** Provides movie, cast and crew information.
- **Git and GitHub:** Used for version control and project management.

## 4. Project Setup

### 4.1 Clone the repository

Open Git Bash and run:

```bash
git clone https://github.com/Maame-Afua-Ayisi/DE02-StreamVault-Film-Analysis.git
cd DE02-StreamVault-Film-Analysis
```

### 4.2 Create and activate a virtual environment

```bash
python -m venv venv
source venv/Scripts/activate
```

### 4.3 Install the required packages

```bash
pip install -r requirements.txt
```

### 4.4 Configure the TMDb API key

A TMDb API key is required to retrieve movie information.

In Git Bash, run:

```bash
export TMDB_API_KEY="your_api_key_here"
```

Replace the example with your own API key.

**Never upload your API key to GitHub or share it publicly.**

## 5. Running the Project

Run the scripts from the main project directory, in the order shown below.

### Step 1: Inspect and reconcile the candidate list

```bash
python src/inspect_input.py
python src/extract_movies.py
python src/investigate_failed_ids.py
python src/reconcile_candidate_ids.py
```

These scripts examine the original candidate list, retrieve available movie information and investigate problems such as blank, repeated, invalid or unsuccessful IDs.

The extraction script includes retry and backoff handling for temporary API failures.

### Step 2: Retrieve cast and crew information

```bash
python src/extract_credits.py
```

This retrieves cast and crew information for the successfully retrieved movies.

### Step 3: Profile, validate and prepare the data

```bash
python src/profile_movies.py
python src/profile_credits.py
python src/build_analysis_dataset.py
python src/validate_relationships.py
```

These scripts examine data completeness, identify potential outliers, prepare the analysis dataset and check relationships between movie, cast and crew records.

The movie profiling script also creates:

```text
reports/potential_outliers.csv
```

This contains values flagged by the Interquartile Range (IQR) method. These are potential outliers for investigation, not automatically confirmed errors.

### Step 4: Spot-check the extracted information

```bash
python src/spot_check_api.py
```

This script retrieves a reproducible sample of five movies again from TMDb and compares selected movie details and cast and crew identifiers with the previously extracted information.

The results are saved in:

```text
reports/api_spot_check.md
```

The spot-check provides evidence for the sampled records; it does not independently verify every extracted record.

### Step 5: Analyse the films

```bash
python src/analyse_franchises.py
python src/analyse_standalone_films.py
python src/analyse_directors.py
python src/analyse_cast.py
python src/analyse_lead_actors.py
```

These scripts examine franchise performance, films without recorded collection membership, directors, cast members and lead-billed actors.

### Step 6: Compare the results

```bash
python src/compare_franchise_periods.py
python src/compare_director_periods.py
python src/compare_standalone_periods.py
python src/compare_cast_periods.py
python src/compare_franchise_results.py
```

The comparisons examine results across all years and for films released from 2000 onward.

### Step 7: Generate the data quality report

```bash
python src/generate_data_quality_report.py
```

This generates:

```text
reports/data_quality_report.md
```

The report summarises extraction results, candidate reconciliation, data completeness and relationship validation.

The separate outlier and API spot-check reports provide additional evidence.

## 6. Important Findings and Limitations

The analysis established that:

- The supplied candidate list contains 126 rows, although the original brief refers to 127 films.
- Information was successfully retrieved for 112 films.
- Five movie requests failed.
- The candidate list contained blank, repeated, non-numeric and non-positive identifiers.
- Six duplicate positive numeric occurrences were identified.
- Sixteen films have no recorded collection membership. This does not automatically mean they are standalone films.
- The extracted movie details contain no duplicate movie IDs.
- Relationship validation found no cast or crew movie IDs missing from the movie details dataset.
- The API spot-check completed 35 checks across five sampled movies, with no mismatches or API errors.
- The outlier analysis identified seven potential outlier records across budget, revenue and runtime.

The analysis also has important limitations:

- Financial values represent historical theatrical budgets and revenues, not licensing costs or streaming performance.
- Financial values have not been adjusted for inflation.
- Historical theatrical performance does not guarantee future streaming demand.
- Missing collection information does not prove that a film is standalone.
- The analysis does not independently verify studio ownership, licensing rights or availability.
- Failed movie requests and unresolved candidate records may affect the completeness of the assessment.

The detailed findings are available in `docs/data_reconciliation.md` and `reports/data_quality_report.md`.

## 7. Project Decisions

The `decisions/` folder contains Architecture Decision Records (ADRs).

These explain important technical and analytical decisions, including data handling, the organisation of the analysis and the selection of lead-billed actors.

Each record documents the reasoning behind a decision, alternatives considered and relevant consequences.

## 8. Additional Improvement

The project includes an additional data quality reporting improvement to help Adjoa assess future candidate lists.

The improvement brings important data checks together in a report, making it easier to identify missing information, repeated IDs and other data quality problems.

A performance test was also conducted using 500 sample candidate films.

Across five measured runs, the report generation process had a median execution time of approximately 1.58 seconds.

The benchmark used synthetic test data. It did not involve retrieving 500 additional films from TMDb.

Further details are available in `improvement.md` and `reports/benchmark_500_candidates.md`.

## 9. Commercial Deliverables

The project includes two documents supporting the licensing decision:

- **`client_memo.md`:** Communicates the main findings and recommendation to Kwame Boateng.
- **`deal_notes.md`:** Provides practical negotiation priorities, questions for studios and commercial risks to investigate before agreeing to licensing terms.

These documents distinguish historical analytical evidence from commercial information that still needs to be obtained.

## 10. Final Deliverables

The repository contains:

1. An examination and reconciliation of the original candidate list.
2. Python scripts for retrieving, preparing, validating and analysing movie information.
3. API retry handling and spot-checking.
4. Data quality profiling and outlier analysis.
5. Written Architecture Decision Records.
6. A licensing recommendation memo for Kwame.
7. Commercial deal notes to support studio negotiations.
8. An additional data quality reporting improvement.
9. A performance benchmark using 500 synthetic candidate records.

## 11. Conclusion

The analysis helps StreamVault identify promising franchises and individual film candidates for further consideration.

The findings provide a basis for prioritising licensing discussions, but they do not establish which deal will generate the highest return.

Before committing the $14 million budget, StreamVault should verify film availability, licensing rights, acquisition prices, contractual terms and expected streaming audience demand.

The final licensing decision should combine the historical evidence in this project with commercial due diligence.