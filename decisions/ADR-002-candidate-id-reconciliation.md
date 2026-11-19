# ADR-002: Candidate ID Reconciliation and Failure Handling

**Status:** Accepted  
**Date:** 19 November 2026

## Context

The supplied candidate list contained 126 CSV rows, although the brief stated that there were 127 candidate titles.

Inspection identified:
- One blank row.
- Six excess occurrences across six duplicated numeric IDs.
- One IMDb-style identifier (`tt0468569`) that required mapping to a TMDb ID.
- One negative ID (`-1`) that returned HTTP 404.
- Five unique positive numeric IDs that also returned HTTP 404.

The original source records were not available to establish why the five failed IDs were included or to recover the missing candidate implied by the brief.

## Decision

Preserve the original candidate CSV unchanged and reconcile every row before extraction.

- Exclude blank, negative and non-numeric identifiers from numeric API requests.
- Map the IMDb-style identifier to its corresponding TMDb ID and document the mapping.
- Deduplicate valid numeric IDs for API requests without deleting duplicate occurrences from the original source.
- Record failed API requests separately rather than silently discarding them.
- Exclude unresolved failed IDs from the financial analysis until their identities can be verified.

## Alternatives Considered

- **Delete duplicates and invalid records from the original CSV:** Rejected because this would destroy source traceability and hide the quality of the supplied list.
- **Retry or replace failed IDs without verification:** Rejected because an assumed replacement could introduce the wrong film into a decision worth $14M.
- **Ignore failed IDs in the final reconciliation:** Rejected because it would make the analysis appear more complete than it is.

## Consequences

- All 126 source rows are accounted for.
- There are 117 unique positive numeric IDs submitted for extraction.
- 112 movies were successfully retrieved and five unique IDs returned HTTP 404.
- The IMDb-style identifier maps to an existing retrieved film, The Dark Knight (TMDb ID 155).
- The original discrepancy between 126 CSV rows and the 127 titles stated in the brief remains unresolved.

## Risks and Limitations

The five failed IDs and the missing candidate may represent films that could affect the shortlist or recommendation. Their identities and potential financial impact cannot be established from the available source data.

The data owner should provide the missing source record and clarify the failed IDs before any final licensing commitment.