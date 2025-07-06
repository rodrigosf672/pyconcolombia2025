import pandas as pd
import matplotlib.pyplot as plt
import json

# Load JSON
with open("q1a-bts-pw.json", "r") as f:
    data = json.load(f)

# Create a DataFrame
df = pd.DataFrame(data)

# Summary statistics
print(df.describe())

# Correlation between total books and load time?
print("\nCorrelation matrix:")
print(df[["Books Total", "Load Time (ms)"]].corr())

# Scatter Plot: Total Books vs. Load Time
plt.figure(figsize=(10, 6))
plt.scatter(df["Books Total"], df["Load Time (ms)"], alpha=0.7)
plt.title("Total Books vs. Load Time")
plt.xlabel("Total Books in Category")
plt.ylabel("Load Time (ms)")
plt.grid(True)
# plt.show()

# Bar Chart: Top 10 Slowest Categories
slowest = df.sort_values(by="Load Time (ms)", ascending=False).head(10)

plt.figure(figsize=(12, 6))
plt.barh(slowest["Category"], slowest["Load Time (ms)"], color="coral")
plt.xlabel("Load Time (ms)")
plt.title("Top 10 Slowest Categories to Load")
plt.gca().invert_yaxis()
plt.tight_layout()
# plt.show()