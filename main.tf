provider "google" {
  project = "vanillasteel"
  region  = "europe-west3"
}

# Google Cloud Storage (GCS) Bucket
resource "google_storage_bucket" "data_bucket" {
  name     = "vanilla-steel-data"
  location = "europe-west3"
  force_destroy = true  
}

# BigQuery Dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = "vanilla_steel"
  location   = "europe-west3"
  labels = {
    environment = "production"
  }

  delete_contents_on_destroy = true  
}

# BigQuery Table Schema for Merged Inventory Data(Task 1)
resource "google_bigquery_table" "inventory_dataset" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "inventory_dataset"
  schema     = file("schemas/inventory_schema.json")
  deletion_protection = false
}

# BigQuery Table for Buyer Preferences(Task 3)
resource "google_bigquery_table" "buyer_preferences" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "buyer_preferences"
  schema              = file("schemas/buyer_preferences.json")
  deletion_protection = false
}

# BigQuery Table for Supplier Data 1(Task 3)
resource "google_bigquery_table" "supplier_data_1" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "supplier_data_1"
  schema              = file("schemas/supplier_data1.json")
  deletion_protection = false
}

# BigQuery Table for Supplier Data 2(Task 3)
resource "google_bigquery_table" "supplier_data_2" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "supplier_data_2"
  schema              = file("schemas/supplier_data2.json")
  deletion_protection = false

    lifecycle {
    ignore_changes = [schema, deletion_protection]
  }
}

# BigQuery Table Schema for Deals (Task 2) - Native Table
resource "google_bigquery_table" "deals_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "deals"

  schema     = file("schemas/deals_schema.json")
  deletion_protection = false
}

# Cloud Storage Bucket for Cloud Function Code
resource "google_storage_bucket" "function_bucket" {
  name     = "vanilla-steel-function"
  location = "europe-west3"
  force_destroy = true
}

# Upload Cloud Function Source Code as a ZIP
data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "cloud_function"
  output_path = "cloud_function.zip"
}

# Upload the ZIP file to the function bucket
resource "google_storage_bucket_object" "function_archive" {
  name   = "cloud_function.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_zip.output_path
}

# Deploy Cloud Function
resource "google_cloudfunctions_function" "data_ingestion" {
  name        = "data-ingestion-function"
  region      = "europe-west3"
  runtime     = "python311"
  entry_point = "ingest_data"
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_archive.name

  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = google_storage_bucket.data_bucket.name
  }

  available_memory_mb = 256
  timeout            = 120
}

# Upload Cloud Function Source Code for dbt Runner
data "archive_file" "dbt_function_zip" {
  type        = "zip"
  source_dir  = "cloud_function"
  output_path = "dbt_function.zip"
}

resource "google_storage_bucket_object" "dbt_function_archive" {
  name   = "dbt_function.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.dbt_function_zip.output_path
}

# Deploy Cloud Function for dbt Runner
resource "google_cloudfunctions_function" "dbt_runner" {
  name        = "dbt-runner-function"
  region      = "europe-west3"
  runtime     = "python311"
  entry_point = "run_dbt"
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.dbt_function_archive.name
  trigger_http = true
  available_memory_mb = 512
  timeout = 300

  environment_variables = {
    DBT_PROFILES_DIR = "/workspace"
  }
}

# Cloud Scheduler Job to Trigger Cloud Function Daily
resource "google_cloud_scheduler_job" "dbt_scheduler" {
  name     = "dbt-daily-run"
  region   = "europe-west3"
  schedule = "0 0 * * *"  # Runs at midnight daily

  http_target {
    uri = google_cloudfunctions_function.dbt_runner.https_trigger_url
    http_method = "POST"
  }
}

