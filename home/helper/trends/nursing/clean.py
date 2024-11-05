"""
FILE DESCRIPTION: clean.py

This script contains functions to clean and preprocess the nursing home inspection data.
"""

# sample useage
# python clean.py data/legacy/01_24_modified_data_clip.csv -o data

import pandas as pd
import os
import argparse

def get_args():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Split a large CSV file by month and year.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file.")
    parser.add_argument(
        "-o", "--output_folder", type=str, default="output_files",
        help="Folder to save the split files. Defaults to 'output_files'."
    )

    return parser.parse_args()

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df["inspection_text"] = df["inspection_text"].apply(lambda s: s.replace("NOTE- TERMS IN BRACKETS HAVE BEEN EDITED TO PROTECT CONFIDENTIALITY", ""))
    df["inspection_text"] = df["inspection_text"].apply(lambda s: s.replace("**** ", ""))
    df["inspection_text"] = df["inspection_text"].str.replace(r'^\d{5}', '', regex=True)
    df["inspection_text"] = df["inspection_text"].apply(lambda s: s.replace("<BR/>", ""))
    return df

def split_csv_by_month_year(input_file, output_folder="output_files"):
    """
    Splits a large CSV file by month and year in the 'inspection_date' column, saving
    each subset as a separate CSV file in the format 'monYY.csv' (e.g., 'jan23.csv').

    Parameters:
    - input_file (str): Path to the large CSV file.
    - output_folder (str): Folder to save the split files. Defaults to "output_files".
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Read the CSV into a DataFrame
    df = pd.read_csv(input_file)

    # Convert 'inspection_date' to datetime format for easy grouping by month and year
    df['inspection_date'] = pd.to_datetime(df['inspection_date'], format='%m/%d/%Y')

    # clean data
    df = clean(df)

    # Group by year and month, then save each group as a separate CSV
    for (year, month), group in df.groupby([df['inspection_date'].dt.year, df['inspection_date'].dt.month]):
        # Generate the file name in the required format, e.g., "jan23.csv", "feb23.csv", etc.
        file_name = f"{output_folder}/{pd.to_datetime(f'{year}-{month}-01').strftime('%b').lower()}{str(year)[-2:]}.csv"
        
        # Save the group to a CSV file
        group.to_csv(file_name, index=False)
        print(f"Saved {file_name}")

if __name__ == "__main__":
    # Parse arguments
    args = get_args()

    # Run the split function with parsed arguments
    split_csv_by_month_year(args.input_file, args.output_folder)
