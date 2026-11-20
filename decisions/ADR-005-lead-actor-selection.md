# ADR-005: Selection of Lead-Billed Actors

**Status:** Accepted  
**Date:** 20 November 2026

## Context

The project needs a consistent way to identify actors who appear in leading roles across the candidate films.

The available cast information includes a billing order for each actor. This indicates the order in which actors are listed in the film credits.

## Decision

Use the first five billing positions (`order <= 4`) as a consistent way to identify lead-billed actors.

Compare the results across all years and films released from 2000 onward.

## Alternatives Considered

1. **Use every cast member:** This includes supporting actors and very small roles, making it harder to identify leading actors.
2. **Use only the first-billed actor:** This may overlook other important leading actors.
3. **Manually select lead actors:** This would require subjective decisions and make the process harder to repeat.

The first five billing positions provide a consistent and repeatable approach.

## Evidence

The analysis covered:

- 112 successfully retrieved films.
- 560 cast records from the first five billing positions.
- Results across all years and from 2000 onward.

## Consequences and Limitations

This approach makes the analysis repeatable, including when the candidate list grows to approximately 500 films.

However:

- Billing order does not always identify the actual lead actor.
- Revenue is associated with each selected actor's films, so the same film's revenue may be counted for several actors.
- The results show historical associations, not proof that an actor caused a film to perform well.

These limitations should be considered when interpreting the actor rankings.