import functions_framework
from google.cloud import storage, bigquery
import pandas as pd
import io
import re

# Set up Google Cloud clients
storage_client = storage.Client()
bq_client = bigquery.Client()

# GCS Bucket & BigQuery Dataset Info
BUCKET_NAME = "vanilla-steel-data"
BQ_DATASET = "vanilla_steel"

def clean_column_names(df):
    """Standardize column names to match BigQuery schema."""
    column_mapping = {
        "Werksgüte": "grade",
        "Bestellgütentext": "finish",
        "Nenndicke NNN.NN mm mit Dezimalpunkt": "thickness_mm",
        "Breite": "width_mm",
        "Länge": "length_mm",
        "Gewicht (kg)": "weight_kg",
        "Cluster": "quantity"
    }

    df = df.rename(columns=column_mapping)

    # Standardize column names
    df.columns = (
        df.columns.str.lower()
        .str.replace(r"[^a-z0-9_]", "_", regex=True)  # Remove special chars
        .str.strip("_")  # Remove leading/trailing underscores
    )

    return df

def clean_numeric_columns(df, columns):
    """Remove commas from numeric columns and convert them to float."""
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "").astype(float)
    return df

@functions_framework.cloud_event
def ingest_data(cloud_event):
    """Triggered when a file is uploaded to GCS. Reads, cleans, and loads data into BigQuery."""
    
    file_name = cloud_event.data["name"]
    bucket_name = cloud_event.data["bucket"]
    
    print(f"Processing file: {file_name} from bucket: {bucket_name}")

    # Load file from GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_bytes()

    # Determine file type (CSV or Excel)
    if file_name.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
    else:
        print("Unsupported file format. Skipping.")
        return
    
    # Define expected columns
    EXPECTED_SUPPLIER_COLUMNS = [
        "grade", "finish", "thickness_mm", "width_mm", "weight_kg", "quantity"
    ]

    # Clean column names
    df = clean_column_names(df)

    # Keep only expected columns if they exist
    available_columns = [col for col in EXPECTED_SUPPLIER_COLUMNS if col in df.columns]
    df = df[available_columns]

    # Remove commas and convert to numbers
    df = clean_numeric_columns(df, ["thickness_mm", "width_mm", "weight_kg"])

    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)

    # Drop rows with missing key values
    df = df.dropna()

    # Determine the target BigQuery table
    if "buyer" in file_name.lower():
        table_id = f"{BQ_DATASET}.buyer_data"
    elif "supplier" in file_name.lower():
        table_id = f"{BQ_DATASET}.supplier_data"
    else:
        print("Unknown file type. Skipping.")
        return

    # Load data into BigQuery
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"✅ Successfully loaded {file_name} into {table_id}")
