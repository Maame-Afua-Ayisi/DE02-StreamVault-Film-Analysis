import pandas as pd

# Load the original candidate list and retrieved movie records
source = pd.read_csv(
    "id_list.csv",
    dtype={"tmdb_id": "string"}
)

movies = pd.read_json("data/raw/movie_details.json")

# Clean identifiers for analysis without changing the original file
raw_ids = source["tmdb_id"].str.strip()
numeric_ids = pd.to_numeric(raw_ids, errors="coerce")

blank_count = raw_ids.isna().sum() + raw_ids.eq("").sum()

positive_numeric = numeric_ids[
    numeric_ids.notna()
    & (numeric_ids > 0)
    & (numeric_ids % 1 == 0)
].astype("int64")

negative_or_zero = numeric_ids[
    numeric_ids.notna() & (numeric_ids <= 0)
]

non_numeric = raw_ids[
    raw_ids.notna()
    & raw_ids.ne("")
    & numeric_ids.isna()
]

# Identify duplicate numeric identifiers
duplicate_ids = positive_numeric[
    positive_numeric.duplicated(keep="first")
]

unique_requested_ids = set(positive_numeric.unique())

# Compare requested IDs with successfully retrieved movie IDs
successful_ids = set(movies["id"].astype("int64"))

failed_ids = unique_requested_ids - successful_ids

# The IMDb identifier was independently resolved to TMDb ID 155
imdb_mapping = {"tt0468569": 155}

print("CANDIDATE ID RECONCILIATION")
print("==========================")
print("Rows in original CSV:", len(source))
print("Blank rows:", blank_count)
print("Positive numeric ID rows:", len(positive_numeric))
print("Negative or zero IDs:", len(negative_or_zero))
print("Non-numeric identifiers:", len(non_numeric))
print("Duplicate numeric occurrences:", len(duplicate_ids))
print("Unique positive numeric IDs:", len(unique_requested_ids))
print("Successfully retrieved movies:", len(successful_ids))
print("Failed movie requests:", len(failed_ids))
print("IMDb identifiers mapped to existing TMDb IDs:", len(imdb_mapping))

print("\nFAILED TMDb IDS")
print("===============")
print(sorted(failed_ids))

print("\nNON-NUMERIC IDENTIFIERS")
print("=======================")
print(non_numeric.tolist())

print("\nIMDb MAPPING")
print("============")
print(imdb_mapping)

print("\nSOURCE COUNT CHECK")
print("==================")
print(
    "Rows accounted for:",
    blank_count
    + len(positive_numeric)
    + len(negative_or_zero)
    + len(non_numeric)
)
