import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import glob
import os


def plot_gaps(file_path):
    # Extract contract code from filename for plot title
    contract_code = file_path.replace("results/price_gaps_", "").replace(".csv", "")

    # Determine if this is an AU or GC file
    is_gc = "GC" in contract_code

    # Read the data
    df = pd.read_csv(file_path)
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
    market_type = "COMEX Gold" if is_gc else "Shanghai Gold"
    plt.title(
        f"Price Gaps Over Time - {market_type} {contract_code}", fontsize=14, pad=15
    )
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Gap Value", fontsize=12)

    # Adjust x-axis
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))

    # Format x-axis
    plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)

    # Add grid
    plt.grid(True, linestyle="--", alpha=0.7)

    # Customize legend
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Create figs directory if it doesn't exist
    os.makedirs("figs", exist_ok=True)

    # Save the plot with contract-specific filename
    plt.savefig(
        f"figs/price_gaps_plot_{contract_code}.png", dpi=450, bbox_inches="tight"
    )

    # Close the figure to free memory
    plt.close()


if __name__ == "__main__":
    # Create figs directory if it doesn't exist
    os.makedirs("figs", exist_ok=True)

    # Get all price_gaps CSV files from results folder (both AU and GC)
    gap_files = glob.glob("results/price_gaps_*.csv")

    for file_path in gap_files:
        plot_gaps(file_path)
        print(f"Plot created for {file_path}")
