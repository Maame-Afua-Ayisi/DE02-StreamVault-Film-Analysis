

# Improvement: Automated Quarterly Data Quality Report



## 1. Problem



The original workflow required Adjoa to run multiple scripts and inspect different output files to understand whether the candidate data was reliable.



This made quarterly checks time-consuming and increased the risk of overlooking missing IDs, duplicate records, failed API requests or broken relationships.



## 2. Solution



I developed an automated data quality reporting script:



`src/generate\_data\_quality\_report.py`



The script reads the existing source, raw API and processed analysis files and generates:



`reports/data\_quality\_report.md`



The report consolidates:



\- Candidate ID reconciliation, including blank, duplicate and invalid IDs.

\- Movie API retrieval successes and failures.

\- Cast and crew record counts.

\- Missing financial information.

\- Missing franchise collection membership.

\- Cast, crew and movie relationship validation.

\- Analysis row counts and reporting-period coverage.

\- Issues requiring further investigation.

\- Data limitations that affect interpretation.



The script uses existing project files and does not make additional API requests.



## 3. Business value



The improvement gives Adjoa one report to review after each quarterly run.



It helps her identify data problems before presenting analysis to Kwame, reduces manual checking and makes the process more repeatable.



For Kwame, it provides greater visibility into the reliability and limitations of the evidence supporting licensing decisions.



## 4. Scalability



The report is generated from the available project files rather than manually entered figures.



When the candidate list grows from 127 to approximately 500 titles, the same reporting process can be rerun against the larger dataset.



The checks can also be extended as additional data sources and validation rules are introduced.



## 5. Limitations



The report cannot independently verify studio ownership, licensing rights or the accuracy of financial information supplied by TMDb.



Missing collection membership does not prove that a film is standalone.



Failed movie requests and unresolved identifiers still require investigation against the original source lists.



The current report checks the supplied candidate file; it cannot identify missing candidates without an independently maintained expected list.



## 6. How to run



From the project root:



```bash

python src/generate\_data\_quality\_report.py

```



The generated report is saved to:



`reports/data\_quality\_report.md`



## 7. Measured Performance

The automated report generator was tested using both the original project dataset and a synthetic dataset representing 500 candidate movies.

**Original dataset:**
- 126 candidate rows.
- 112 successfully retrieved movies.
- 7,827 cast records.
- 24,932 crew records.
- Report generation time: approximately 0.39 seconds.

**500-candidate scalability test:**
- 500 candidate rows.
- 500 movie records.
- 35,215 cast records.
- 111,781 crew records.
- 545 movie-director relationship records.
- Five measured runs: 1.353s, 1.353s, 1.377s, 1.364s and 1.359s.
- Median report generation time: 1.359 seconds.

The test used a synthetic dataset scaled from the original project data. It demonstrates that the reporting process can handle a larger dataset quickly without additional API requests.

The benchmark script is available at `tests/benchmark_data_quality_report.py`, and the recorded results are available at `reports/benchmark_500_candidates.md`.

These measurements cover report generation from existing local files. They exclude API retrieval and the other analysis scripts. Performance may vary depending on the computer used.



