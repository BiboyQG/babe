import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Read the data
df = pd.read_csv("price_gaps.csv")
df["DateTime"] = pd.to_datetime(df["DateTime"])

# Create the figure and axis
plt.figure(figsize=(12, 6))

# Plot all four lines
plt.plot(
    df["DateTime"],
    df["gap_open"],
    label="Open",
    marker="o",
    linewidth=1,
    markersize=0.5,
    alpha=0.1,
)
plt.plot(
    df["DateTime"],
    df["gap_high"],
    label="High",
    marker="^",
    linewidth=1,
    markersize=0.5,
    alpha=0.1,
)
plt.plot(
    df["DateTime"],
    df["gap_low"],
    label="Low",
    marker="v",
    linewidth=1,
    markersize=0.5,
    alpha=0.1,
)
plt.plot(
    df["DateTime"],
    df["gap_close"],
    label="Close",
    marker="s",
    linewidth=1,
    markersize=0.5,
    alpha=0.1,
)

# Customize the plot
plt.title("Price Gaps Over Time", fontsize=14, pad=15)
plt.xlabel("Time", fontsize=12)
plt.ylabel("Gap Value", fontsize=12)

# Format x-axis
plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
plt.xticks(rotation=45)

# Add grid
plt.grid(True, linestyle="--", alpha=0.7)

# Customize legend
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))

# Adjust layout to prevent label cutoff
plt.tight_layout()

plt.savefig("price_gaps_plot.png", dpi=450, bbox_inches="tight")

# Show the plot
plt.show()