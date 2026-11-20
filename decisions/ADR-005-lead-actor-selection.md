

\# ADR-005: Lead Actor Selection Using Cast Billing Order



\*\*Status:\*\* Accepted  

\*\*Date:\*\* 20 November 2026



\## Context



The StreamVault analysis needs to identify actors who appear consistently in commercially successful candidate films.



The TMDb credits response provides a cast billing order through the `order` field. However, the brief does not specify how many cast members should count as lead actors.



Including every credited cast member would make it difficult to distinguish principal performers from supporting and minor roles.



\## Decision



Use the first five cast billing positions in each film as a practical proxy for lead actors.



The analysis filters cast records using:



`order <= 4`



The selected cast records are then joined to movie-level financial information to compare actor appearances and associated film performance across:



\- All years.

\- 2000 onward.



\## Alternatives Considered



\- \*\*Include every credited cast member:\*\* Rejected because minor and supporting roles would be treated equally with principal performers.

\- \*\*Use only the first billed actor:\*\* Rejected because this could exclude other important leading performers in ensemble films.

\- \*\*Manually identify lead actors for every film:\*\* Rejected because this would require subjective research and would be difficult to repeat consistently across approximately 500 candidates.



\## Consequences



\- The analysis uses a consistent selection rule across all retrieved films.

\- The first five billing positions produce 560 cast records across 112 movies.

\- Actor appearances can be compared across the two reporting periods.

\- The method is repeatable when Adjoa processes a larger candidate list.



\## Risks and Limitations



Cast billing order is only a proxy for lead roles. It does not always identify the most commercially influential performer or accurately represent ensemble films.



Full movie revenue is attributed to each selected actor. Therefore, revenue totals overlap when multiple actors appear in the same film.



The results show historical associations within the candidate sample. They do not prove that an actor caused a film's financial performance or guarantee future commercial success.



If the first five billing positions do not accurately represent the principal performers, some relevant actors may be excluded and some supporting performers may be included.



The selection rule should therefore be treated as a consistent analytical assumption, not a definitive classification of lead actors.



