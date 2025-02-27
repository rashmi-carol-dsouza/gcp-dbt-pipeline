import functions_framework
from google.cloud import storage, bigquery
import pandas as pd
import io
from task1_process_supplier_1 import process_supplier_1
from task1_process_supplier_2 import process_supplier_2
from task3_process_buyer_preferences import process_buyer_preferences
from task3_process_supplier_1 import process_task3_supplier_1
from task3_process_supplier_2 import process_task3_supplier_2

# Set up Google Cloud clients
storage_client = storage.Client()
bq_client = bigquery.Client()

# GCS Bucket & BigQuery Dataset Info
BUCKET_NAME = "vanilla-steel-data"
BQ_DATASET = "vanilla_steel"


@functions_framework.cloud_event
def ingest_data(cloud_event):
    """Triggered when a file is uploaded to GCS. Reads, merges, and loads data into BigQuery."""

    file_name = cloud_event.data["name"]
    bucket_name = cloud_event.data["bucket"]

    print(f"Processing file: {file_name} from bucket: {bucket_name}")

    # Load file from GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_bytes()

    # Read the file (CSV or Excel)
    if file_name.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content), dtype=str)
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(content), engine="openpyxl", dtype=str)
    else:
        print(f"Unsupported file format: {file_name}. Skipping.")
        return

    # Determine which processing logic to use and target table

    if "supplier_data_1" in file_name.lower():
        df = process_supplier_1(df)
        target_table = "inventory_dataset"
    elif "supplier_data_2" in file_name.lower():
        df = process_supplier_2(df)
        target_table = "inventory_dataset"
    elif "buyer_preferences" in file_name.lower():
        df = process_buyer_preferences(df)
        target_table = "buyer_preferences"
    elif "supplier_data1" in file_name.lower():
        df = process_task3_supplier_1(df)
        target_table = "supplier_data_1"
    elif "supplier_data2" in file_name.lower():
        df = process_task3_supplier_2(df)
        target_table = "supplier_data_2"
    else:
        print(f"No processing logic found for file: {file_name}. Skipping.")
        return

    # Load data into BigQuery
    table_id = f"{BQ_DATASET}.{target_table}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    job = bq_client.load_table_from_dataframe(
        df, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"Successfully loaded {file_name} into {table_id}")
