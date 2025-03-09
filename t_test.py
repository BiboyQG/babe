import pandas as pd
import numpy as np
import glob
import os
from scipy import stats
import tabulate


def perform_t_test(file_path):
    """
    Perform t-test for gap = 0 for all price types in the given file.

    Args:
        file_path: Path to the price gaps CSV file

    Returns:
        Dictionary containing t-test results for each price type
    """
    # Extract contract name from file path
    contract_name = (
        os.path.basename(file_path).replace("price_gaps_", "").replace(".csv", "")
    )

    # Read the gap data
    df = pd.read_csv(file_path)

    # Dictionary to store results
    results = {"Contract": contract_name}

    # Perform t-test for each price type
    for price_type in ["open", "high", "low", "close"]:
        gap_column = f"gap_{price_type}"

        # Calculate statistics
        mean = df[gap_column].mean()
        std_dev = df[gap_column].std()
        n = len(df[gap_column])
        std_err = std_dev / np.sqrt(n)

        # Calculate t-statistic manually for large sample sizes
        t_stat = mean / std_err if std_err != 0 else np.nan

        # Calculate p-value (two-tailed test)
        # For large sample sizes, we can use normal distribution approximation
        if not np.isnan(t_stat):
            p_value = 2 * (1 - stats.norm.cdf(abs(t_stat)))
        else:
            p_value = np.nan

        # Store results
        results[f"{price_type}_mean"] = mean
        results[f"{price_type}_std_dev"] = std_dev
        results[f"{price_type}_std_err"] = std_err
        results[f"{price_type}_t_stat"] = t_stat
        results[f"{price_type}_p_value"] = p_value

    return results


def main():
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)

    # Get all price gap files
    gap_files = glob.glob("results/price_gaps_*.csv")

    # Separate AU and GC files
    au_files = [f for f in gap_files if "AU" in f]
    gc_files = [f for f in gap_files if "GC" in f]

    # Lists to store results
    au_results = []
    gc_results = []

    # Process AU files
    print("Processing AU contracts...")
    for file_path in au_files:
        results = perform_t_test(file_path)
        au_results.append(results)
        print(f"Processed {results['Contract']}")

    # Process GC files
    print("\nProcessing GC contracts...")
    for file_path in gc_files:
        results = perform_t_test(file_path)
        gc_results.append(results)
        print(f"Processed {results['Contract']}")

    # Create DataFrames from results
    au_df = pd.DataFrame(au_results)
    gc_df = pd.DataFrame(gc_results)

    # Print results in a nice format
    print("\n=== AU Contracts T-Test Results ===")
    print_results_table(au_df)

    print("\n=== GC Contracts T-Test Results ===")
    print_results_table(gc_df)

    # Save results to CSV
    au_df.to_csv("results/au_t_test_results.csv", index=False)
    gc_df.to_csv("results/gc_t_test_results.csv", index=False)

    print(
        "\nResults saved to 'results/au_t_test_results.csv' and 'results/gc_t_test_results.csv'"
    )


def print_results_table(df):
    """Print results in a formatted table"""
    # Create a more readable format for the results
    table_data = []

    for _, row in df.iterrows():
        contract = row["Contract"]

        for price_type in ["open", "high", "low", "close"]:
            mean = row[f"{price_type}_mean"]
            std_dev = row[f"{price_type}_std_dev"]
            std_err = row[f"{price_type}_std_err"]
            t_stat = row[f"{price_type}_t_stat"]
            p_value = row[f"{price_type}_p_value"]

            # Add significance stars
            sig = ""
            if not np.isnan(p_value):
                if p_value < 0.01:
                    sig = "***"
                elif p_value < 0.05:
                    sig = "**"
                elif p_value < 0.1:
                    sig = "*"

            table_data.append(
                [
                    contract,
                    price_type.capitalize(),
                    f"{mean:.6f}",
                    f"{std_dev:.6f}",
                    f"{std_err:.6f}",
                    f"{t_stat:.4f}" if not np.isnan(t_stat) else "nan",
                    f"{p_value:.6f}{sig}" if not np.isnan(p_value) else "nan",
                ]
            )

    # Print the table
    headers = [
        "Contract",
        "Price Type",
        "Mean",
        "Std Dev",
        "Std Err",
        "t-stat",
        "p-value",
    ]
    print(tabulate.tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
