
import pandas as pd

# Load the corrected one-row-per-film dataset
movies = pd.read_csv("data/processed/movie_analysis.csv")

# Identify films without recorded collection membership
standalone_films = movies.loc[
    movies["belongs_to_collection.id"].isna()
].copy()

# Select useful columns for analysis
standalone_summary = standalone_films[[
    "id",
    "title",
    "release_year",
    "budget",
    "revenue",
    "revenue_budget_ratio",
    "director_names"
]].copy()

# Rank films by reported theatrical revenue
standalone_summary = standalone_summary.sort_values(
    "revenue",
    ascending=False
)

print("FILMS WITHOUT RECORDED COLLECTION MEMBERSHIP")
print("=============================================")
print(
    standalone_summary.to_string(index=False)
)

print("\nSUMMARY")
print("=======")
print("Films without recorded collection membership:",
      len(standalone_summary))
print("Average revenue:",
      standalone_summary["revenue"].mean())
print("Average revenue-to-budget ratio:",
      standalone_summary["revenue_budget_ratio"].mean())
print("Total reported revenue:",
      standalone_summary["revenue"].sum())

# Save results
standalone_summary.to_csv(
    "data/processed/standalone_film_analysis.csv",
    index=False
)
