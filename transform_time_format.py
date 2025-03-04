import os
import pandas as pd
from datetime import datetime


def transform_datetime_format(input_file, output_file):
    """
    Transform the DateTime format in CSV files from 'YYYY/MM/DD HH:MM' to 'YYYY-MM-DD HH:MM:SS'

    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to the output CSV file
    """
    print(f"Processing {input_file}...")

    # Read the CSV file
    df = pd.read_csv(input_file)

    # Convert DateTime column to the new format
    df["DateTime"] = df["DateTime"].apply(
        lambda x: datetime.strptime(x, "%Y/%m/%d %H:%M").strftime("%Y-%m-%d %H:%M:00")
    )

    # Save the transformed data to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Transformed data saved to {output_file}")


def main():
    # Input files
    input_files = ["data/GCM24E.CMX.csv", "data/GCZ23E.CMX.csv"]

    output_dir = "data"

    # Process each input file
    for input_file in input_files:
        # Generate output file name
        file_name = os.path.basename(input_file).replace(".csv", "_transformed.csv")
        output_file = os.path.join(output_dir, file_name)

        # Transform the file
        transform_datetime_format(input_file, output_file)


if __name__ == "__main__":
    main()
