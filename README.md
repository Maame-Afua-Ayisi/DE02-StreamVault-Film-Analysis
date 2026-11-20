# StreamVault Film Licensing Analysis

## Project Overview

This project analyses films that StreamVault, a streaming service, is considering for licensing.

The aim is to help the company decide which films and franchises deserve further attention before spending its $14 million licensing budget.

The analysis looks at:
- How well different film franchises performed.
- Films that have no recorded franchise membership.
- Directors and actors who appear across the films.
- How the results compare when older films are excluded.

The project uses film information from The Movie Database (TMDb).

It is designed so the analysis can be repeated when StreamVault receives a larger list of films.

## Project Structure

```text
DE02-StreamVault-Film-Analysis/
│
├── data/
│   ├── raw/          Original information retrieved
│   └── processed/    Cleaned information used for analysis
│
├── decisions/        Important project decisions
├── docs/             Data-quality findings
├── reports/          Generated reports
├── src/              Python scripts
├── tests/            Performance test
│
├── id_list.csv
├── client_memo.md
├── improvement.md
├── requirements.txt
└── README.md
```

## Tools Used

- **Python:** Used to carry out the analysis.
- **Pandas and NumPy:** Used to organise and work with the information.
- **Requests:** Used to retrieve information from TMDb.
- **TMDb:** Provides film, cast and crew information.
- **Git and GitHub:** Used to manage and store the project.

## How to Set Up the Project

### 1. Download the project

Open Git Bash and run:

```bash
git clone https://github.com/Maame-Afua-Ayisi/DE02-StreamVault-Film-Analysis.git
cd DE02-StreamVault-Film-Analysis
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Add your TMDb API key

A TMDb API key is needed to retrieve film information.

In Git Bash, run:

```bash
export TMDB_API_KEY="your_api_key_here"
```

Replace the example with your own key.

**Do not upload your API key to GitHub or share it publicly.**

## How to Run the Project

Run the following commands from the main project folder.

### Step 1: Check the film list and retrieve film information

```bash
python src/inspect_input.py
python src/extract_movies.py
python src/investigate_failed_ids.py
python src/reconcile_candidate_ids.py
```

These scripts check the original film list, retrieve available film information and identify problems such as missing or repeated IDs.

### Step 2: Retrieve actors and crew information

```bash
python src/extract_credits.py
```

This retrieves information about the actors and crew members involved in the films.

### Step 3: Check and prepare the information

```bash
python src/profile_movies.py
python src/profile_credits.py
python src/build_analysis_dataset.py
python src/validate_relationships.py
```

These scripts check the information, prepare it for analysis and make sure the film, actor and crew records match correctly.

### Step 4: Analyse the films

```bash
python src/analyse_franchises.py
python src/analyse_standalone_films.py
python src/analyse_directors.py
python src/analyse_cast.py
python src/analyse_lead_actors.py
```

These scripts examine franchise performance, individual-title candidates, directors and actors.

### Step 5: Compare the results

```bash
python src/compare_franchise_periods.py
python src/compare_director_periods.py
python src/compare_standalone_periods.py
python src/compare_cast_periods.py
python src/compare_franchise_results.py
```

The results are compared across all years and for films released from 2000 onward.

### Step 6: Create the data-quality report

```bash
python src/generate_data_quality_report.py
```

This creates an updated report at:

```text
reports/data_quality_report.md
```

The report summarises the number of films retrieved, missing information and other issues found during the checks.

## Important Findings and Limitations

The analysis found that:

- The supplied film list contains 126 rows, although the brief refers to 127 films.
- Information was successfully retrieved for 112 films.
- Five film IDs could not be found.
- Some IDs were repeated, blank or in an unexpected format.
- Some films have no recorded franchise membership. This does not automatically mean they are standalone films.
- Older films have not been adjusted for inflation.

Most importantly, cinema earnings and production costs do not tell us how much StreamVault should pay to license a film.

The full findings are available in `docs/data_reconciliation.md`.

## Project Decisions

The `decisions/` folder explains the important choices made during the project, including how the original film list was handled, how the information was organised and how lead-billed actors were selected.

## Additional Improvement

The project includes an automated report to help Adjoa check the quality of future film lists.

The report brings important checks together in one place, making it easier to spot missing films, repeated IDs and other problems.

A performance test was also carried out using 500 sample films. The report took a median of approximately 1.36 seconds to generate in that test. The sample was created for testing and does not represent 500 additional films retrieved from TMDb.

More details are available in `improvement.md`.

## Final Deliverables

This project includes:

1. An examination of the original film list and its problems.
2. Python scripts for retrieving and analysing film information.
3. Written explanations of important project decisions.
4. A recommendation memo for Kwame in `client_memo.md`.
5. An additional reporting improvement for future film lists in `improvement.md`.

## Conclusion

The analysis helps StreamVault identify promising franchises and individual films for further discussion.

However, the results are based on historical cinema performance. StreamVault should confirm film availability, licensing rights, prices and expected viewer interest before making its final decision.