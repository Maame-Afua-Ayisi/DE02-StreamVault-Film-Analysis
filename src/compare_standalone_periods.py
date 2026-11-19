
import pandas as pd

movies = pd.read_csv("data/processed/movie_analysis.csv")

# Select films without recorded collection membership
films = movies.loc[
    movies["belongs_to_collection.id"].isna()
].copy()

# Separate films by release period
recent_films = films.loc[
    films["release_year"] >= 2000
].copy()

def summarise_period(data):
    return {
        "film_count": len(data),
        "total_budget": data["budget"].sum(),
        "total_revenue": data["revenue"].sum(),
        "average_revenue": data["revenue"].mean(),
        "average_ratio": data["revenue_budget_ratio"].mean(),
        "aggregate_ratio": (
            data["revenue"].sum() / data["budget"].sum()
            if data["budget"].sum() != 0 else None
        )
    }

all_years_summary = summarise_period(films)
recent_summary = summarise_period(recent_films)

comparison = pd.DataFrame(
    [all_years_summary, recent_summary],
    index=["All years", "2000 onward"]
)

print("FILMS WITHOUT RECORDED COLLECTION MEMBERSHIP")
print("=============================================")
print(comparison.to_string())

print("\nFILM COUNTS BY PERIOD")
print("=====================")
print("All years:", len(films))
print("2000 onward:", len(recent_films))
print("Before 2000:", len(films) - len(recent_films))

print("\nTOP FILMS BY REVENUE: ALL YEARS")
print("================================")
print(
    films.sort_values("revenue", ascending=False)[
        ["title", "release_year", "budget", "revenue",
         "revenue_budget_ratio"]
    ].head(10).to_string(index=False)
)

print("\nTOP FILMS BY REVENUE: 2000 ONWARD")
print("==================================")
print(
    recent_films.sort_values("revenue", ascending=False)[
        ["title", "release_year", "budget", "revenue",
         "revenue_budget_ratio"]
    ].head(10).to_string(index=False)
)

comparison.to_csv(
    "data/processed/films_without_collection_period_comparison.csv"
)

print("\nComparison saved successfully.")
