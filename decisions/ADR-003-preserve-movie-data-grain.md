# ADR-003: Preserve Movie-Level Data Grain

**Status:** Accepted  
**Date:** 19 November 2026

## Context

The movie details dataset contains one record per movie, while the director credits dataset can contain multiple records for a single movie.

An initial direct join between movie details and director records increased the dataset from 112 to 122 rows because nine movies had multiple director records.

This repeated movie-level financial information in the joined dataset and created a risk of overstating budgets and revenues during aggregation.

## Decision

Maintain two separate analytical datasets:

- `movie_analysis.csv`: one row per movie, containing movie details, financial measures and aggregated director names.
- `movie_directors.csv`: one row per movie-director relationship, preserving individual director associations.

Aggregate director information by movie before joining it to the movie-level dataset. Validate the final join as one-to-one.

Use the separate movie-director dataset when analysing director performance.

## Alternatives Considered

- **Join all director records directly to movie details:** Rejected because movies with multiple directors would appear more than once, potentially inflating financial totals.
- **Keep only one director per movie:** Rejected because it would discard valid director relationships and misrepresent co-directed films.

## Consequences

- The final movie analysis contains 112 rows for 112 unique movies.
- The separate movie-director dataset contains 122 movie-director relationships.
- All nine movies with multiple director records retain their director associations.
- Movie-level financial totals are not duplicated by the director join.
- Director analysis can still be performed using the separate relationship dataset.

## Risks and Limitations

Aggregating director names does not establish that a director caused a film's financial performance.

A film's revenue is associated with every credited director in the analysis, so director-level revenue totals overlap and must not be added together as though they represent separate revenue.