import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path

# ---------------- Load Data ----------------
def load_json(file):
    with open(file) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["Source"] = file.stem
    return df

files = [
    Path("q1a-bts-pw.json"),
    Path("q1b-bts-pw.json"),
    Path("q2a-bts-pw.json"),
    Path("q2b-bts-pw.json"),
]

df = pd.concat([load_json(f) for f in files], ignore_index=True)
df["Caching"] = df["Source"].apply(lambda x: "No Caching" if "q1" in x else "Caching")
df["Navigation"] = df["Source"].apply(lambda x: "Clicking" if "a" in x else "Direct Link")
sns.set(style="whitegrid")

# Barplot: Average Load Time by Category + Caching/Navigation
plt.figure(figsize=(12, 6))
df["Group"] = df["Caching"] + " / " + df["Navigation"]
sns.barplot(data=df, x="Category", y="Load Time (ms)", hue="Group", ci=None)
plt.title("Average Load Time by Category and Method")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("barplot_avg_loadtime.png")
plt.show()

# Boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Category", y="Load Time (ms)")
plt.title("Boxplot of Load Time by Category")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("boxplot_loadtime.png")
plt.show()

# Violin Plot
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x="Category", y="Load Time (ms)")
plt.title("Violin Plot of Load Time by Category")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("violinplot_loadtime.png")
plt.show()

# Summary statistics
summary = df.groupby("Category")["Load Time (ms)"].agg(["mean", "median", "count"]).sort_values("mean", ascending=False)
summary.to_csv("loadtime_summary.csv")
print(summary)
