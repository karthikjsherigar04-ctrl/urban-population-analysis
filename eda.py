import pandas as pd

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# ── 1. Load cleaned dataset ──────────────────────────────────
df = pd.read_csv("data/cleaned_population.csv")

print("Dataset loaded successfully")
print("Shape:", df.shape)

# ── 2. Overall statistics ────────────────────────────────────
print("\n── Overall Population Statistics ───────────────────")

print("Total countries:        ", len(df))
print("Continents covered:     ", df["continent"].nunique())

print("World population 2022: ",
      f"{df['pop_2022'].sum():,}")

print("World population 1970: ",
      f"{df['pop_1970'].sum():,}")

print("Total growth 1970→2022:",
      f"{df['pop_change'].sum():,}")

# ── 3. Top 10 most populated countries ──────────────────────
print("\n── Top 10 Most Populated Countries (2022) ──────────")

top10_pop = df.nlargest(10, "pop_2022")[
    ["country", "continent", "pop_2022"]
]

print(top10_pop.to_string(index=False))

# ── 4. Population by continent ──────────────────────────────
print("\n── Population by Continent (2022) ─────────────────")

continent_pop = (
    df.groupby("continent")["pop_2022"]
    .sum()
    .sort_values(ascending=False)
)

print(continent_pop)

# ── 5. Fastest growing countries ────────────────────────────
print("\n── Top 10 Fastest Growing Countries ────────────────")

top_growth = df.nlargest(10, "growth_rate_pct")[
    ["country", "continent", "growth_rate_pct"]
]

print(top_growth.to_string(index=False))

# ── 6. Slowest growing / declining countries ────────────────
print("\n── Top 10 Slowest Growing Countries ────────────────")

slow_growth = df.nsmallest(10, "growth_rate_pct")[
    ["country", "continent", "growth_rate_pct"]
]

print(slow_growth.to_string(index=False))

# ── 7. Population change from 1970 to 2022 ──────────────────
print("\n── Top 10 Countries by Population Change ───────────")

top_change = df.nlargest(10, "pop_change")[
    [
        "country",
        "pop_1970",
        "pop_2022",
        "pop_change",
        "pop_change_pct"
    ]
]

print(top_change.to_string(index=False))

# ── 8. Most densely populated countries ─────────────────────
print("\n── Top 10 Most Densely Populated Countries ─────────")

top_density = df.nlargest(10, "density")[
    ["country", "continent", "density", "pop_2022"]
]

print(top_density.to_string(index=False))

# ── 9. World population trend by decade ─────────────────────
print("\n── World Population Trend by Decade ────────────────")

years = [
    "pop_1970",
    "pop_1980",
    "pop_1990",
    "pop_2000",
    "pop_2010",
    "pop_2015",
    "pop_2020",
    "pop_2022"
]

for col in years:
    year = col.replace("pop_", "")
    total = df[col].sum()

    print(f"{year}: {total:,.0f}")

# ── 10. Average growth rate by continent ────────────────────
print("\n── Average Growth Rate by Continent ───────────────")

continent_growth = (
    df.groupby("continent")["growth_rate_pct"]
    .mean()
    .sort_values(ascending=False)
)

print(continent_growth)

# ── 11. Top countries by world population share ─────────────
print("\n── Top 10 Countries by World Population Share ─────")

top_share = df.nlargest(10, "world_pop_percentage")[
    ["country", "world_pop_percentage"]
]

print(top_share.to_string(index=False))

# ── 12. Additional insights ─────────────────────────────────
print("\n── Additional Insights ─────────────────────────────")

# Highest density country
highest_density = df.loc[df["density"].idxmax()]

print("\nMost densely populated country:")
print(
    f"{highest_density['country']} "
    f"({highest_density['density']:,.2f} people/km²)"
)

# Largest area country
largest_area = df.loc[df["area_km2"].idxmax()]

print("\nLargest country by area:")
print(
    f"{largest_area['country']} "
    f"({largest_area['area_km2']:,.0f} km²)"
)

# Lowest population country
lowest_pop = df.loc[df["pop_2022"].idxmin()]

print("\nLowest population country:")
print(
    f"{lowest_pop['country']} "
    f"({lowest_pop['pop_2022']:,.0f})"
)

print("\n✅ EDA completed successfully")