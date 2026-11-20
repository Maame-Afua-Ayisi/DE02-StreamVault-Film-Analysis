
# StreamVault Data Diagnosis and Candidate Reconciliation

## 1. Executive summary

The StreamVault case brief refers to 127 candidate titles, but the supplied `id_list.csv` contains only 126 rows.

After checking the identifiers, removing duplicate API requests, resolving one IMDb identifier and investigating failed requests, 112 movies were successfully retrieved and included in the final analysis.

The analysis is usable for comparing the retrieved candidates, but it does not represent a fully verified list of all 127 titles.

The most important limitations are:

1. Five movie requests failed, and their identities could not be verified against the original source records.
2. The supplied candidate list contains one fewer row than the brief specifies.
3. The 16 movies without recorded collection membership cannot automatically be treated as confirmed standalone films.
4. Historical theatrical revenue and budget figures do not establish licensing profitability.
5. Cast and director performance measures are indicators of historical association, not proof that an individual caused a film's commercial success.

These limitations should be considered before committing the $14 million licensing budget.

## 2. Candidate ID reconciliation

### 2.1 Reconciliation results

The original `id_list.csv` was preserved. Identifiers were checked before movie-detail extraction.

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
| Movies included in final analysis | 112 |

The 123 positive numeric rows contained six excess duplicate occurrences across six IDs. This left 117 unique positive numeric IDs for extraction.

Of these 117 requests, 112 succeeded and five failed.

### 2.2 Identifier issues

- Six excess occurrences were identified across six duplicate numeric IDs.
- The negative identifier `-1` returned HTTP 404 and was excluded from numeric extraction.
- The IMDb identifier `tt0468569` was resolved to TMDb ID `155`, corresponding to *The Dark Knight*. This film was already represented by numeric ID 155, so it was not counted as another title.
- Five unique numeric IDs returned HTTP 404: `7733901`, `8471293`, `8471294`, `9412887` and `9412888`.

The five failed identifiers could not be verified against the original source records because the supporting tracker, predecessor spreadsheet and studio list were not supplied.

### 2.3 Missing candidate

The case brief refers to 127 candidate titles, while the supplied file contains 126 rows.

The missing entry cannot be identified from the available file. It would be unsafe to invent a candidate or assume that one of the failed IDs represents the missing entry.

The data owner should provide the original candidate list and confirm the missing entry.

## 3. Ranked data risks

The risks below are ranked by their potential effect on the licensing recommendation.

### Risk 1 — Incomplete candidate coverage

**Severity: Critical**

**Problem:** The case brief specifies 127 candidates, but the supplied file contains 126 rows. In addition, five unique numeric IDs could not be retrieved.

**Detection:** Compared the row count in `id_list.csv` with the case brief, checked duplicates and invalid identifiers, and recorded failed API requests.

**Effect on Kwame's decision:** The analysis covers 112 successfully retrieved films, not a verified complete set of 127 candidates. Some potentially valuable franchise or standalone opportunities may therefore be absent from the rankings.

**Recommended action:** Obtain the missing candidate and original source records. Verify the five failed identifiers with the data owner before making final acquisition decisions.

**Cost if unresolved:** Kwame risks making a decision using an incomplete opportunity set. The financial value of the omitted opportunities cannot be calculated from the available data.

### Risk 2 — Historical financial figures are not licensing economics

**Severity: Critical**

**Problem:** The analysis uses TMDb theatrical budgets and revenues. These figures do not represent StreamVault's acquisition costs, licensing fees, streaming revenue or expected profit.

**Detection:** Inspected the financial fields retrieved from the movie API and reviewed the calculations used in the analysis.

**Effect on Kwame's decision:** A film or franchise with high historical theatrical revenue may still be expensive to license or perform poorly on StreamVault. Revenue-to-budget ratios must not be interpreted as licensing returns or guaranteed profitability.

**Recommended action:** Obtain actual studio asking prices, proposed licensing terms and StreamVault audience or viewing-performance estimates before approving deals.

**Cost if unresolved:** Kwame could overpay for a commercially attractive film or reject a less expensive opportunity with stronger potential value.

### Risk 3 — Pre-2000 financial comparisons may be misleading

**Severity: High**

**Problem:** Historical financial values are nominal figures. The analysis does not adjust them for inflation or independently verify currency consistency across release periods.

**Detection:** Compared the all-years results with the 2000-onward results and reviewed the financial fields used in the calculations.

**Effect on Kwame's decision:** Older films may appear less commercially significant because their historical revenues are not adjusted for changes in prices and currency values. This is particularly relevant to Yaw's concern about pre-2000 figures.

**Recommended action:** Keep the two reporting periods visible and obtain verified inflation-adjusted and currency-consistent figures before using historical comparisons for financial valuation.

**Cost if unresolved:** Older franchises or films may be unfairly ranked against newer releases.

### Risk 4 — Missing collection membership does not prove a film is standalone

**Severity: High**

**Problem:** Sixteen retrieved films have no recorded TMDb collection membership.

**Detection:** Checked the `belongs_to_collection.id` field in the retrieved movie details.

**Effect on Kwame's decision:** These films may be incorrectly treated as standalone opportunities. Missing collection information does not establish that a film has no sequel, franchise relationship or bundle requirement.

**Recommended action:** Verify franchise and sequel relationships against studio catalogues before negotiating standalone licences.

**Cost if unresolved:** Kwame may overlook bundle requirements or negotiate for an individual title that is commercially available only as part of a larger package.

### Risk 5 — Collection records may not represent complete licensing bundles

**Severity: High**

**Problem:** TMDb collection membership describes recorded film relationships. It does not establish that every film in a franchise is included in the candidate list or available for licensing as a bundle.

**Detection:** Compared the retrieved collection membership and candidate film counts across franchises.

**Effect on Kwame's decision:** Historical franchise performance may be based on only some films in a collection. It cannot establish the performance or cost of acquiring the complete studio bundle.

**Recommended action:** Obtain the complete studio catalogue and confirm which titles are available together, their rights and their individual licensing costs.

**Cost if unresolved:** A franchise may appear attractive in the analysis but require additional titles or costs that change the acquisition decision.

### Risk 6 — Cast and director performance figures are associations, not causal measures

**Severity: Medium**

**Problem:** Full movie revenue is attributed to credited directors and actors. A film with multiple directors or several leading actors therefore contributes its full revenue to more than one person.

**Detection:** Inspected cast and crew relationships and compared movie-level records with director and actor summary calculations.

**Effect on Kwame's decision:** A high-ranking actor or director may appear to be a reliable commercial signal partly because they worked on the same successful films. The results do not prove that their involvement caused the revenue.

**Recommended action:** Treat the rankings as indicators for further investigation, not guaranteed predictors of future licensing performance.

**Cost if unresolved:** Kwame may overvalue a person based on overlapping revenue attribution rather than independent evidence of commercial performance.

### Risk 7 — Lead actor identification uses billing order as a proxy

**Severity: Medium**

**Problem:** The lead actor analysis uses the first five cast billing positions (`order <= 4`) as a practical proxy for leading actors.

**Detection:** Inspected the cast API's billing-order field and used it to select the first five credited performers per film.

**Effect on Kwame's decision:** Billing order does not always identify the most commercially influential performer or the actual lead role.

**Recommended action:** Validate important actor signals against film credits and other reliable information before using them in acquisition decisions.

**Cost if unresolved:** Kwame may place too much confidence in an actor whose billing position does not reflect their commercial importance.

### Risk 8 — Source accuracy and provenance remain unverified

**Severity: Medium**

**Problem:** The original Adjoa tracker, predecessor spreadsheet and studio email batch were not provided. The retrieved API records have not been independently checked against studio records.

**Detection:** Compared the available project inputs with the source materials described in the case brief.

**Effect on Kwame's decision:** The analysis cannot establish why the original identifiers were included, whether all studio candidates were represented, or whether API financial and collection information matches the rights holders' records.

**Recommended action:** Request the original source files and reconcile the candidate list against verified studio catalogues.

**Cost if unresolved:** Incorrect or incomplete source information may remain undetected and affect the shortlist.

## 4. Data completeness and relationship validation

### 4.1 Movie financial completeness

The 112 successfully retrieved movies were checked for missing values in the principal analytical fields.

| Field | Missing values |
|---|---:|
| Budget | 0 |
| Revenue | 0 |
| Runtime | 0 |
| Release date | 0 |

All 112 retrieved movies had values in these fields.

However, completeness does not guarantee accuracy. The values still require independent verification before being used for financial decisions.

### 4.2 Cast and crew completeness

The credits extraction returned:

| Measure | Count |
|---|---:|
| Cast records | 7,827 |
| Unique cast members | 6,190 |
| Crew records | 24,932 |
| Unique crew members | 16,161 |

All 112 retrieved movies were represented in both cast and crew data.

### 4.3 Relationship validation

The relationship checks found:

| Validation | Result |
|---|---:|
| Cast movie IDs missing from movie details | 0 |
| Crew movie IDs missing from movie details | 0 |
| Movies without cast records | 0 |
| Movies without crew records | 0 |
| Movie-director relationship records | 122 |
| Movies in final movie analysis | 112 |

The director relationship table contains more rows than the movie table because nine movies have multiple directors.

The final movie analysis preserves one row per movie. This prevents multiple director records from unintentionally multiplying movie-level financial figures in the main dataset.

These checks confirm that the retrieved relationships are structurally connected. They do not prove that the source information is factually correct.

## 5. Candidate disposition

The original source file contains 126 rows, including blank, duplicate and invalid entries.

The extraction process produced 117 unique positive numeric IDs. Of these, 112 were successfully retrieved and five failed.

The IMDb identifier was mapped to an already represented TMDb movie and was not counted as a separate film. The negative ID and blank row were excluded from numeric extraction.

The final analytical dataset contains 112 unique movies.

The difference between the 127 candidates stated in the brief and the 112 successfully analysed movies must not be interpreted as 15 confirmed missing titles. The difference includes duplicate entries, invalid or blank entries, failed requests and the unresolved difference between the brief and supplied file.

The five failed identifiers and the missing source entry remain unresolved. They should be investigated before the shortlist is treated as complete.

## 6. Recommendation implications

The analysis can support an initial comparison of franchise and non-collection candidates within the retrieved sample.

However:

- Franchise rankings should be treated as rankings of the represented candidate films, not necessarily complete licensing bundles.
- Films without collection metadata should be described as films without recorded collection membership, not confirmed standalone titles.
- The top actor and director rankings are historical associations, not guaranteed predictors of future success.
- The all-years and 2000-onward comparisons should both be considered because historical nominal financial figures may distort comparisons.
- The financial analysis should not be used to determine licensing prices without actual studio deal information.

Kwame should use the results to prioritise further investigation and negotiation, not as sufficient evidence to approve the entire $14 million budget.

## 7. What could not be verified

The available data did not allow verification of:

- The missing candidate implied by the difference between 127 and 126 rows.
- The original source and intended meaning of the five failed identifiers.
- Whether all candidate films are available for licensing.
- Whether collection membership represents a complete studio bundle.
- Actual licensing prices and contractual terms.
- StreamVault-specific audience demand or expected streaming revenue.
- The accuracy of historical financial figures against studio records.
- Whether the first five cast billing positions consistently identify the commercially relevant lead actors.

These gaps require source-owner or studio confirmation. They cannot be resolved by further calculations on the current dataset alone.

## 8. Implications for future quarterly runs

The extraction and analysis workflow is organised into repeatable scripts and separates raw API responses from processed analytical outputs.

When Adjoa reruns the workflow against approximately 500 candidates:

- The same identifier checks can identify blanks, duplicates and invalid IDs.
- The extraction process can retrieve movie details and credits for the expanded list.
- Relationship validation can identify missing movie, cast and crew links.
- The analysis can be rebuilt for both reporting periods.
- The automated data quality report can consolidate the latest checks.

The process will still depend on valid API access, source-list completeness and human verification of unresolved records and licensing information.

The workflow makes the analysis repeatable; it does not automatically resolve source-data or commercial-rights uncertainty.
