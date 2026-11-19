# ADR-004: Handling Missing Collection Membership

**Status:** Accepted  
**Date:** 19 November 2026

## Context

StreamVault needs to compare franchise candidates with standalone titles.

The TMDb movie details response includes collection information through the `belongs_to_collection` field. However, 16 of the 112 successfully retrieved films had no recorded collection ID.

The absence of a collection record does not prove that a film was released or licensed as a standalone title.

## Decision

Classify films with a recorded TMDb collection ID as collection-associated films.

Classify films without a recorded collection ID as films without recorded collection membership.

Do not automatically describe the latter group as confirmed standalone films. Retain them in a separate analysis to provide a useful comparison while making the classification limitation explicit.

## Alternatives Considered

- **Treat every film without a collection ID as standalone:** Rejected because missing collection metadata does not establish the commercial licensing category.
- **Exclude films without collection information:** Rejected because this would remove 16 successfully retrieved candidates from the analysis and could hide potentially valuable titles.
- **Manually assign missing collection memberships:** Rejected because there was no authoritative source available to verify those assignments.

## Consequences

- 96 films have recorded collection membership.
- 16 films have no recorded collection membership.
- The analysis can compare the two groups without claiming that the groups exactly represent the studio's licensing categories.
- The final client recommendation must distinguish TMDb collection associations from actual licensing arrangements.

## Risks and Limitations

Some films without recorded collection membership may belong to commercially packaged franchises or other licensing arrangements.

Consequently, the comparison is a useful indication of candidate performance, not proof that every film in the second group can be licensed individually.