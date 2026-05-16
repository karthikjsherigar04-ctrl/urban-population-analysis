import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ── Pandas display settings ──────────────────────────────────
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# ── Load cleaned dataset ─────────────────────────────────────
df = pd.read_csv("data/cleaned_population.csv")

# ── Create charts folder ─────────────────────────────────────
os.makedirs("charts", exist_ok=True)

# ── Seaborn theme ────────────────────────────────────────────
sns.set_theme(style="whitegrid")

print("Generating charts...")

# ─────────────────────────────────────────────────────────────
# CHART 1 → Top 10 Most Populated Countries
# ─────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 6))

top10 = (
    df.nlargest(10, "pop_2022")[["country", "pop_2022"]]
    .reset_index(drop=True)
)

top10["pop_millions"] = top10["pop_2022"] / 1e6

sns.barplot(
    data=top10,
    x="pop_millions",
    y="country",
    hue="country",
    palette="Blues_r",
    legend=False
)

plt.title("Top 10 Most Populated Countries (2022)", fontsize=14)
plt.xlabel("Population (Millions)")
plt.ylabel("Country")

for i, v in enumerate(top10["pop_millions"]):
    plt.text(v + 5, i, f"{v:.0f}M", va="center")

plt.tight_layout()

plt.savefig("charts/chart1_top10_populated.png")

plt.show()

print("✅ Chart 1 saved")

# ─────────────────────────────────────────────────────────────
# CHART 2 → World Population Trend
# ─────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 6))

years = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]

cols = [
    "pop_1970",
    "pop_1980",
    "pop_1990",
    "pop_2000",
    "pop_2010",
    "pop_2015",
    "pop_2020",
    "pop_2022"
]

world_pop = [df[col].sum() / 1e9 for col in cols]

sns.lineplot(
    x=years,
    y=world_pop,
    marker="o",
    linewidth=2.5
)

plt.fill_between(years, world_pop, alpha=0.2)

for x, y in zip(years, world_pop):
    plt.text(x, y + 0.05, f"{y:.2f}B", ha="center")

plt.title("World Population Growth Trend (1970–2022)", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Population (Billions)")

plt.xticks(years)

plt.tight_layout()

plt.savefig("charts/chart2_world_population_trend.png")

plt.show()

print("✅ Chart 2 saved")

# ─────────────────────────────────────────────────────────────
# CHART 3 → Population Share by Continent
# ─────────────────────────────────────────────────────────────
plt.figure(figsize=(9, 9))

continent_pop = (
    df.groupby("continent")["pop_2022"]
    .sum()
)

plt.pie(
    continent_pop.values,
    labels=continent_pop.index,
    autopct="%1.1f%%",
    startangle=140,
    explode=[0.05] * len(continent_pop)
)

plt.title("World Population Share by Continent (2022)", fontsize=14)

plt.tight_layout()

plt.savefig("charts/chart3_continent_pie.png")

plt.show()

print("✅ Chart 3 saved")

# ─────────────────────────────────────────────────────────────
# CHART 4 → Fastest Growing Countries
# ─────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 6))

top_growth = (
    df.nlargest(10, "growth_rate_pct")
    [["country", "growth_rate_pct"]]
    .reset_index(drop=True)
)

sns.barplot(
    data=top_growth,
    x="growth_rate_pct",
    y="country",
    hue="country",
    palette="Reds_r",
    legend=False
)

plt.title("Top 10 Fastest Growing Countries", fontsize=14)

plt.xlabel("Growth Rate (%)")
plt.ylabel("Country")

for i, v in enumerate(top_growth["growth_rate_pct"]):
    plt.text(v + 0.05, i, f"{v:.2f}%")

plt.tight_layout()

plt.savefig("charts/chart4_fastest_growing.png")

plt.show()

print("✅ Chart 4 saved")

# ─────────────────────────────────────────────────────────────
# CHART 5 → Declining Countries
# ─────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 6))

declining = (
    df.nsmallest(10, "growth_rate_pct")
    [["country", "growth_rate_pct"]]
    .reset_index(drop=True)
)

sns.barplot(
    data=declining,
    x="growth_rate_pct",
    y="country",
    hue="country",
    palette="Blues",
    legend=False
)

plt.title("Top 10 Declining Countries", fontsize=14)

plt.xlabel("Growth Rate (%)")
plt.ylabel("Country")

for i, v in enumerate(declining["growth_rate_pct"]):
    plt.text(v - 0.1, i, f"{v:.2f}%", ha="right")

plt.tight_layout()

plt.savefig("charts/chart5_declining_countries.png")

plt.show()

print("✅ Chart 5 saved")

# ─────────────────────────────────────────────────────────────
# CHART 6 → Continent Population Trend
# ─────────────────────────────────────────────────────────────
plt.figure(figsize=(14, 7))

decade_cols = {
    "1970": "pop_1970",
    "1990": "pop_1990",
    "2000": "pop_2000",
    "2010": "pop_2010",
    "2022": "pop_2022"
}

continent_decade = pd.DataFrame()

for year, col in decade_cols.items():

    temp = (
        df.groupby("continent")[col]
        .sum()
        .reset_index()
    )

    temp.columns = ["continent", "population"]

    temp["year"] = year

    continent_decade = pd.concat(
        [continent_decade, temp],
        ignore_index=True
    )

continent_decade["population"] = (
    continent_decade["population"] / 1e9
)

sns.lineplot(
    data=continent_decade,
    x="year",
    y="population",
    hue="continent",
    marker="o",
    linewidth=2
)

plt.title("Population Growth by Continent", fontsize=14)

plt.xlabel("Year")
plt.ylabel("Population (Billions)")

plt.legend(
    title="Continent",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)

plt.tight_layout()

plt.savefig("charts/chart6_continent_growth.png")

plt.show()

print("✅ Chart 6 saved")

# ─────────────────────────────────────────────────────────────
# CHART 7 → Population Density
# ─────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 6))

top_density = (
    df.nlargest(10, "density")
    [["country", "density"]]
    .reset_index(drop=True)
)

sns.barplot(
    data=top_density,
    x="density",
    y="country",
    hue="country",
    palette="Purples_r",
    legend=False
)

plt.title("Top 10 Most Densely Populated Countries", fontsize=14)

plt.xlabel("Density (people per km²)")
plt.ylabel("Country")

for i, v in enumerate(top_density["density"]):
    plt.text(v + 100, i, f"{v:,.0f}")

plt.tight_layout()

plt.savefig("charts/chart7_density.png")

plt.show()

print("✅ Chart 7 saved")

# ─────────────────────────────────────────────────────────────
# CHART 8 → Population Change
# ─────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 6))

top_change = (
    df.nlargest(10, "pop_change")
    [["country", "pop_change"]]
    .reset_index(drop=True)
)

top_change["change_millions"] = (
    top_change["pop_change"] / 1e6
)

sns.barplot(
    data=top_change,
    x="change_millions",
    y="country",
    hue="country",
    palette="Greens_r",
    legend=False
)

plt.title("Top 10 Population Increase (1970–2022)", fontsize=14)

plt.xlabel("Population Change (Millions)")
plt.ylabel("Country")

for i, v in enumerate(top_change["change_millions"]):
    plt.text(v + 5, i, f"{v:.0f}M")

plt.tight_layout()

plt.savefig("charts/chart8_population_change.png")

plt.show()

print("✅ Chart 8 saved")

# ─────────────────────────────────────────────────────────────
# CHART 9 → Average Growth by Continent
# ─────────────────────────────────────────────────────────────
plt.figure(figsize=(10, 6))

continent_growth = (
    df.groupby("continent")["growth_rate_pct"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

continent_growth.columns = [
    "continent",
    "avg_growth"
]

sns.barplot(
    data=continent_growth,
    x="continent",
    y="avg_growth",
    hue="continent",
    palette="coolwarm",
    legend=False
)

plt.title("Average Growth Rate by Continent", fontsize=14)

plt.xlabel("Continent")
plt.ylabel("Average Growth Rate (%)")

for i, v in enumerate(continent_growth["avg_growth"]):
    plt.text(i, v + 0.03, f"{v:.2f}%", ha="center")

plt.tight_layout()

plt.savefig("charts/chart9_continent_growth_rate.png")

plt.show()

print("✅ Chart 9 saved")

print("\n✅ All charts generated successfully")