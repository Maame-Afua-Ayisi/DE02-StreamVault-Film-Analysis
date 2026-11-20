# StreamVault Quarterly Data Quality Report

Generated: 2026-11-20 07:53 UTC

## 1. Executive summary

- Candidate rows in source file: 126
- Successfully retrieved movies: 112
- Failed movie requests: 5
- Cast records: 7827
- Crew records: 24932
- Movies in final analysis: 112

## 2. Candidate ID reconciliation

- Blank IDs: 1
- Duplicate positive numeric occurrences: 6
- Non-numeric identifiers: 1
- Non-positive numeric IDs: 1
- Unique positive numeric IDs: 117

Note: Non-numeric identifiers require a separate identifier-resolution step. A successfully mapped identifier should be documented in the reconciliation record.

## 3. API extraction

- Movie records retrieved: 112
- Failed movie requests: 5
- Cast records retrieved: 7827
- Crew records retrieved: 24932
- Failed credit requests: 0

## 4. Data completeness

- Missing budget: 0
- Missing revenue: 0
- Missing runtime: 0
- Missing release_date: 0
- Movies without recorded collection membership: 16

## 5. Relationship validation

- Cast movie IDs not found in movie details: 0
- Crew movie IDs not found in movie details: 0
- Movies without cast records: 0
- Movies without crew records: 0
- Movie-director relationship records: 122

## 6. Analysis coverage

- Rows in movie analysis: 112
- Unique movies in movie analysis: 112
- Franchise reporting periods: All years, 2000 onward
- Director reporting periods: 2000 onward, All years
- Cast reporting periods: 2000 onward, All years
- Lead actor reporting periods: 2000 onward, All years

## 7. Items requiring attention

- Review 1 blank candidate ID row(s).
- Review 6 duplicate candidate ID occurrence(s).
- Review 1 non-numeric identifier(s) and verify their TMDb mappings.
- Investigate 1 non-positive numeric ID(s).
- Investigate 5 failed movie request(s).
- 16 movies have no recorded collection membership; do not automatically classify them as standalone.

## 8. Limitations

- A successful API response does not guarantee that every source value is correct.
- Missing collection membership does not prove that a film is standalone.
- Financial values are theatrical budget and revenue, not licensing costs or streaming performance.
- Non-numeric source identifiers require separate verification and documented mapping.
- This report checks available files; it does not independently verify studio rights or source ownership.
- The report covers the candidate list supplied for this run; it cannot identify missing candidates without an independently maintained expected list.

Report generation time: 0.39 seconds
