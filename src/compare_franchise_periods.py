import pandas as pd

movies = pd.read_csv("data/processed/movie_analysis.csv")

def summarise_franchises(data):
    franchise_movies = data.loc[
        data["belongs_to_collection.id"].notna()
    ].copy()

    summary = (
        franchise_movies.groupby(
            ["belongs_to_collection.id", "belongs_to_collection.name"]
        )
        .agg(
            candidate_films=("id", "nunique"),
            total_budget=("budget", "sum"),
            total_revenue=("revenue", "sum"),
            average_revenue=("revenue", "mean"),
            average_ratio=("revenue_budget_ratio", "mean")
        )
        .reset_index()
    )

    summary["aggregate_ratio"] = (
        summary["total_revenue"] / summary["total_budget"]
    )

    return summary.sort_values("total_revenue", ascending=False)


# Analyse all candidate films
all_years = summarise_franchises(movies)

# Analyse films released from 2000 onward
movies_2000_onward = movies.loc[
    movies["release_year"] >= 2000
].copy()

recent_years = summarise_franchises(movies_2000_onward)


print("ALL YEARS: TOP 15 FRANCHISES")
print("============================")
print(all_years[[
    "belongs_to_collection.name",
    "candidate_films",
    "total_revenue",
    "aggregate_ratio"
]].head(15).to_string(index=False))


print("\n2000 ONWARD: TOP 15 FRANCHISES")
print("==============================")
print(recent_years[[
    "belongs_to_collection.name",
    "candidate_films",
    "total_revenue",
    "aggregate_ratio"
]].head(15).to_string(index=False))


# Save both analyses
all_years.to_csv(
    "data/processed/franchise_analysis_all_years.csv",
    index=False
)

recent_years.to_csv(
    "data/processed/franchise_analysis_2000_onward.csv",
    index=False
)

print("\nCOMPARISON SUMMARY")
print("==================")
print("All-years candidate films:", len(movies))
print("Films released from 2000 onward:", len(movies_2000_onward))
print("All-years collections:", len(all_years))
print("Collections from 2000 onward:", len(recent_years))
