# Candidate ID Reconciliation

## Overview

The supplied `id_list.csv` contains 126 rows, whereas the StreamVault case brief refers to 127 candidate titles. The original file was preserved, and identifiers were checked before movie-detail extraction.

## Reconciliation results

| Measure | Count |
|---|---:|
| Original CSV rows | 126 |
| Blank rows | 1 |
| Positive numeric ID rows | 123 |
| Negative or zero IDs | 1 |
| Non-numeric identifiers | 1 |
| Duplicate numeric occurrences | 6 |
| Unique positive numeric IDs requested | 117 |
| Successfully retrieved movies | 112 |
| Failed movie requests | 5 |

## Identifier issues

- Six excess occurrences were identified across six duplicate numeric IDs.
- The negative identifier `-1` returned HTTP 404.
- The IMDb identifier `tt0468569` was resolved to TMDb ID `155`, corresponding to *The Dark Knight*. This film was already represented by numeric ID 155 and was not counted as an additional title.
- Five unique numeric IDs returned HTTP 404: `7733901`, `8471293`, `8471294`, `9412887` and `9412888`.

## Limitations and actions

The five failed identifiers could not be verified against the original source records because the supporting tracker, predecessor spreadsheet and studio list were not supplied.

The difference between the 127 candidates stated in the case brief and the 126 supplied CSV rows remains unresolved. The missing candidate should be requested from the data owner.

The analysis therefore uses the 112 successfully retrieved films. Failed and excluded identifiers remain documented for traceability and should not be silently discarded or treated as confirmed standalone titles.