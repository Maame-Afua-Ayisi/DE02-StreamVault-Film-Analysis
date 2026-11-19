# ADR-001: Separate Raw Data from Processed Data

**Status:** Accepted  
**Date:** 19 November 2026

## Context

The StreamVault analysis retrieves movie details, cast and crew information from the TMDb API. These records need cleaning, transformation and joining before they can be used for analysis.

If the original API responses are overwritten during processing, it becomes difficult to trace changes, investigate data-quality issues or reproduce the analysis.

## Decision

Store the original retrieved data separately from the transformed analysis datasets.

- `data/raw/` contains the original retrieved movie details, cast and crew data, and extraction failure records.
- `data/processed/` contains cleaned, joined and aggregated datasets used for analysis.

Processing scripts read from the raw data and write their results to the processed data directory.

## Alternatives Considered

- **Process and overwrite the original data:** Rejected because it would remove the original records and make it harder to investigate errors or reproduce transformations.
- **Keep all data in one directory:** Rejected because it would make it less clear which files are original source data and which have been transformed.

## Consequences

- Original retrieved data remains available for auditing and reprocessing.
- Data transformations can be repeated without retrieving all records again.
- The project has a clearer structure as the number of candidate films grows.
- Additional storage is required because both raw and processed datasets are retained.

## Risks and Limitations

Keeping raw data does not guarantee that the source information is accurate or complete. API failures and missing source records must still be documented and investigated.