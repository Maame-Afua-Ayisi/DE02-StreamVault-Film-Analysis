
import pandas as pd

# Load the extracted movie details.
movies = pd.read_json("data/raw/movie_details.json")

print("MOVIE DATA PROFILE")
print("==================")

# 1. Dataset dimensions
print(f"\nRows: {len(movies)}")
print(f"Columns: {len(movies.columns)}")
print(f"Unique movie IDs: {movies['id'].nunique()}")

# 2. Missing values in important fields
important_fields = [
    "title",
    "release_date",
    "budget",
    "revenue",
    "runtime",
    "genres",
    "belongs_to_collection"
]

print("\nMISSING VALUES")
print(movies[important_fields].isna().sum())

# 3. Zero financial values
print("\nZERO FINANCIAL VALUES")
print("Budget equals zero:", (movies["budget"] == 0).sum())
print("Revenue equals zero:", (movies["revenue"] == 0).sum())

# 4. Inspect movies with zero budget or revenue
print("\nMOVIES WITH ZERO BUDGET")
print(
    movies.loc[
        movies["budget"] == 0,
        ["id", "title", "release_date", "budget", "revenue"]
    ].to_string(index=False)
)

print("\nMOVIES WITH ZERO REVENUE")
print(
    movies.loc[
        movies["revenue"] == 0,
        ["id", "title", "release_date", "budget", "revenue"]
    ].to_string(index=False)
)

# 5. Inspect collection information
print("\nCOLLECTION MEMBERSHIP")
print(
    movies[
        ["id", "title", "belongs_to_collection.id",
         "belongs_to_collection.name"]
    ].head(15).to_string(index=False)
)

# 6. Check duplicate movie records
print("\nDUPLICATE MOVIE IDs")
print(
    movies[
        movies["id"].duplicated(keep=False)
    ][["id", "title"]]
)


# 7. Identify potential outliers using the IQR method
print("\nPOTENTIAL OUTLIER ANALYSIS")
print("==========================")

outlier_fields = {
    "budget": "Budget",
    "revenue": "Revenue",
    "runtime": "Runtime"
}

outlier_records = []

for column, label in outlier_fields.items():

    # Exclude missing and zero values.
    values = movies.loc[
        movies[column].notna() & (movies[column] > 0),
        column
    ]

    if len(values) < 4:
        print(f"\n{label}: Not enough positive values to assess.")
        continue

    # Calculate quartiles and IQR.
    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    # Identify values outside the IQR boundaries.
    outliers = movies.loc[
        movies[column].notna()
        & (movies[column] > 0)
        & (
            (movies[column] < lower_bound)
            | (movies[column] > upper_bound)
        ),
        ["id", "title", column]
    ]

    print(f"\n{label.upper()}")
    print(f"Records assessed: {len(values)}")
    print(f"First quartile (Q1): {q1:,.2f}")
    print(f"Third quartile (Q3): {q3:,.2f}")
    print(f"IQR: {iqr:,.2f}")
    print(f"Lower boundary: {lower_bound:,.2f}")
    print(f"Upper boundary: {upper_bound:,.2f}")
    print(f"Potential outliers: {len(outliers)}")

    if not outliers.empty:
        print(outliers.to_string(index=False))

    for _, row in outliers.iterrows():
        outlier_records.append({
            "movie_id": row["id"],
            "title": row["title"],
            "field": column,
            "value": row[column],
            "lower_boundary": lower_bound,
            "upper_boundary": upper_bound
        })


# 8. Save potential outliers for further investigation
outlier_report = pd.DataFrame(outlier_records)

import os

os.makedirs("reports", exist_ok=True)

outlier_report.to_csv(
    "reports/potential_outliers.csv",
    index=False
)

print("\nOUTLIER ANALYSIS COMPLETE")
print(f"Potential outlier records saved: {len(outlier_report)}")
print("Report saved to reports/potential_outliers.csv")
