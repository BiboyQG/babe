import pandas as pd
import numpy as np
from datetime import datetime
import glob

def calculate_gap(au_file_name):
    # Read all CSV files
    spot_usd = pd.read_csv("data/SPTAUUSDOZ.IDC.csv", encoding_errors="replace")
    exchange_rate = pd.read_csv("data/USDCHY.EX.csv", encoding_errors="replace")
    rmb_rate = pd.read_csv("data/OpeningPrice.csv", encoding_errors="replace")
    au_data = pd.read_csv(f"data/{au_file_name}.csv", encoding_errors="replace")

    # Convert DateTime columns to datetime
    spot_usd["DateTime"] = pd.to_datetime(spot_usd["DateTime"])
    exchange_rate["DateTime"] = pd.to_datetime(exchange_rate["DateTime"]).dt.date
    rmb_rate["DateTime"] = pd.to_datetime(rmb_rate["DateTime"]).dt.date
    au_data["DateTime"] = pd.to_datetime(au_data["DateTime"])

    # Calculate S_RMB for each price type (open, high, low, close)
    # First, merge spot_usd with exchange rate based on date
    spot_usd["Date"] = spot_usd["DateTime"].dt.date
    spot_with_rate = pd.merge(
        spot_usd,
        exchange_rate,
        left_on="Date",
        right_on="DateTime",
        suffixes=("", "_rate"),
    )

    # Calculate S_RMB
    for col in ["open", "high", "low", "close"]:
        spot_with_rate[f"S_RMB_{col}"] = (
            spot_with_rate[col] * spot_with_rate["OPEN"] / 31.1035
        )

    # Merge with RMB rate
    spot_with_rates = pd.merge(
        spot_with_rate,
        rmb_rate,
        left_on="Date",
        right_on="DateTime",
        suffixes=("", "_rmb"),
    )

    def parse_expiry_from_filename(filename):
        # Extract year and month from filename (e.g., 'AU2406' -> 2024, 06)
        year = 2000 + int(filename[2:4])  # '24' -> 2024
        month = int(filename[4:6])        # '06' -> 6
        return datetime(year, month, 1, 2, 30)  # Set to 2:30 AM on 1st of the month

    def calc_time_to_expiry(dt, filename):
        expiry = parse_expiry_from_filename(filename)
        diff = (expiry - dt).total_seconds() / (24 * 60 * 60)  # Convert seconds to days
        return diff / 365  # Convert to years

    # Assuming au_file contains the filename
    spot_with_rates["t"] = spot_with_rates["DateTime"].apply(
        lambda x: calc_time_to_expiry(x, au_file_name)
    )

    # Calculate F_RMB for each price type
    for col in ["open", "high", "low", "close"]:
        spot_with_rates[f"F_RMB_{col}"] = spot_with_rates[f"S_RMB_{col}"] * np.exp(
            spot_with_rates["OPEN_rmb"] / 100 * spot_with_rates["t"]
        )

    # Merge with AU data
    final_data = pd.merge(
        spot_with_rates,
        au_data,
        left_on="DateTime",
        right_on="DateTime",
        suffixes=("_spot", ""),
    )

    # Calculate gaps for each price type
    for col in ["open", "high", "low", "close"]:
        final_data[f"gap_{col}"] = final_data[col] - final_data[f"F_RMB_{col}"]

    # Filter out rows where any of the AU2412 prices are NaN
    final_data = final_data.dropna(subset=["open", "high", "low", "close"])

    # Select relevant columns for output
    output_data = final_data[
        ["DateTime", "gap_open", "gap_high", "gap_low", "gap_close"]
    ]

    # Save to CSV with specific filename for each AU contract
    output_filename = f"results/price_gaps_{au_file_name}.csv"
    output_data.to_csv(output_filename, index=False)
    return output_data


if __name__ == "__main__":
    # Use glob to find all AU files in the data directory
    au_files = glob.glob("data/AU*.csv")
    # Extract just the AU code without 'data/' and '.csv'
    au_files = [f.replace("data/", "").replace(".csv", "") for f in au_files]
    
    for au_file in au_files:
        gaps = calculate_gap(au_file)
        print(f"Calculation completed for {au_file}. Results saved to 'price_gaps_{au_file}.csv'")
