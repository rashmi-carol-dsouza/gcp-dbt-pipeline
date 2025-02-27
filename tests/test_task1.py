"""
This script verifies data consistency between XLSX files and a BigQuery CSV export.

What it does:
1. Reads all XLSX files in the specified directory (`DATA_DIR`).
2. Merges them into a single DataFrame (`df_xlsx`).
3. Reads the exported BigQuery CSV (`df_csv`).
4. Compares both datasets to check for mismatches in row counts and shared columns.

Usage:
Simply run this script to detect inconsistencies in data ingestion.

Author: Rashmi Carol Dsouza
"""

import pandas as pd
import os
import glob

# Define the directory path where all XLSX and CSV files are located
DATA_DIR = "/home/rashmi/Projects/Vanilla Steel/resources/task_1/"
CSV_FILE = os.path.join(DATA_DIR, "bigquery.csv")  # The BigQuery CSV file

def read_xlsx_files(directory):
    """Reads all XLSX files in the given directory and returns a merged DataFrame."""
    xlsx_files = glob.glob(os.path.join(directory, "*.xlsx"))
    all_dfs = []
    
    for file in xlsx_files:
        print(f"Loading {file}...")
        df = pd.read_excel(file, engine="openpyxl", dtype=str)
        df["source_file"] = os.path.basename(file)  # Keep track of source file
        all_dfs.append(df)
    
    if not all_dfs:
        print("⚠️ No XLSX files found.")
        return None

    merged_xlsx_df = pd.concat(all_dfs, ignore_index=True)
    print(f"Merged {len(all_dfs)} XLSX files with {merged_xlsx_df.shape[0]} rows.")
    return merged_xlsx_df

def compare_datasets(df_xlsx, df_csv):
    """Compares two DataFrames and prints mismatches."""
    if df_xlsx.shape[0] != df_csv.shape[0]:
        print(f"⚠️ Row count mismatch: XLSX({df_xlsx.shape[0]}) vs CSV({df_csv.shape[0]})")
    
    common_columns = list(set(df_xlsx.columns) & set(df_csv.columns))
    
    mismatches = df_xlsx[common_columns].compare(df_csv[common_columns])
    
    if mismatches.empty:
        print("✅ Data matches perfectly!")
    else:
        print("❌ Data mismatches found:")
        print(mismatches)

if __name__ == "__main__":
    # Load BigQuery CSV
    print(f"Loading {CSV_FILE}...")
    df_csv = pd.read_csv(CSV_FILE, dtype=str)
    
    # Load all XLSX files
    df_xlsx = read_xlsx_files(DATA_DIR)
    
    if df_xlsx is not None:
        compare_datasets(df_xlsx, df_csv)
