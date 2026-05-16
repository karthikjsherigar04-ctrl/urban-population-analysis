import pandas as pd
import os

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# ── 1. Load dataset ──────────────────────────────────────────
df = pd.read_csv("C:\\Users\\test\\Desktop\\urban_population_analysis\\world_population.csv")
print("Original shape:", df.shape)

# ── 2. Check basic info ──────────────────────────────────────
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

# ── 3. Rename columns for easier use ────────────────────────
df = df.rename(columns={
    "Country/Territory": "country",
    "CCA3": "code",
    "Capital": "capital",
    "Continent": "continent",
    "Area (km²)": "area_km2",
    "Density (per km²)": "density",
    "Growth Rate": "growth_rate",
    "World Population Percentage": "world_pop_percentage",
    "2022 Population": "pop_2022",
    "2020 Population": "pop_2020",
    "2015 Population": "pop_2015",
    "2010 Population": "pop_2010",
    "2000 Population": "pop_2000",
    "1990 Population": "pop_1990",
    "1980 Population": "pop_1980",
    "1970 Population": "pop_1970"
})

# ── 4. Check null values ─────────────────────────────────────
print("\nNull values:")
print(df.isnull().sum())

# ── 5. Convert growth rate to percentage ────────────────────
df["growth_rate_pct"] = (df["growth_rate"] - 1) * 100
df["growth_rate_pct"] = df["growth_rate_pct"].round(2)

# ── 6. Calculate population change 1970 to 2022 ─────────────
df["pop_change"] = df["pop_2022"] - df["pop_1970"]

df["pop_change_pct"] = (
    (df["pop_2022"] - df["pop_1970"]) /
    df["pop_1970"] * 100
).round(2)

# ── 7. Create data folder if not exists ─────────────────────
os.makedirs("data", exist_ok=True)

# ── 8. Save cleaned data ─────────────────────────────────────
df.to_csv("data/cleaned_population.csv", index=False)

print("\n✅ Cleaned data saved to data/cleaned_population.csv")

# ── 9. Summary ───────────────────────────────────────────────
print("\n── Summary ──────────────────────────────────────────")

print("Total countries:     ", len(df))
print("Continents covered:  ", df["continent"].nunique())

print("\nFastest growing country:")
print(df.loc[df["growth_rate_pct"].idxmax(),
             ["country", "growth_rate_pct"]])

print("\nTop 5 most populated countries (2022):")
print(df.nlargest(5, "pop_2022")[["country", "pop_2022"]])