
import pandas as pd

# Load the original input file.
df = pd.read_csv("id_list.csv", dtype={"tmdb_id": "string"})

# Remove accidental surrounding whitespace for inspection only.
ids = df["tmdb_id"].str.strip()

# Identify blank entries.
blank_ids = ids.isna() | (ids == "")

# Identify values that cannot be interpreted as numbers.
numeric_ids = pd.to_numeric(ids, errors="coerce")
non_numeric_ids = ids.notna() & (ids != "") & numeric_ids.isna()

# Identify numeric IDs that are zero or negative.
non_positive_ids = numeric_ids.notna() & (numeric_ids <= 0)

# Identify repeated IDs.
duplicate_mask = ids.notna() & ids.duplicated(keep=False)

print("INITIAL INPUT DATA AUDIT")
print("-----------------------")
print(f"Total rows: {len(df)}")
print(f"Populated IDs: {(~blank_ids).sum()}")
print(f"Blank IDs: {blank_ids.sum()}")
print(f"Distinct populated IDs: {ids[~blank_ids].nunique()}")
print(f"Rows belonging to duplicate groups: {duplicate_mask.sum()}")
print(f"Non-numeric IDs: {non_numeric_ids.sum()}")
print(f"Zero or negative IDs: {non_positive_ids.sum()}")

print("\nDuplicate values:")
print(ids[duplicate_mask].value_counts())

print("\nNon-numeric values:")
print(ids[non_numeric_ids])

print("\nZero or negative values:")
print(ids[non_positive_ids])
