provider "google" {
  project = "vanillasteel"
  region  = "europe-west3"
}

# Google Cloud Storage (GCS) Bucket
resource "google_storage_bucket" "data_bucket" {
  name     = "vanilla-steel-data"
  location = "EU"
  force_destroy = true  # Allows deletion of bucket without confirmation
}

# BigQuery Dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = "vanilla_steel"
  location   = "EU"
}

# BigQuery Tables
resource "google_bigquery_table" "supplier_data" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "supplier_data"
  schema     = file("schemas/supplier_schema.json")
  deletion_protection=false
}

resource "google_bigquery_table" "buyer_data" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "buyer_data"
  schema     = file("schemas/buyer_schema.json")
  deletion_protection=false
}

resource "google_bigquery_table" "recommendations" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "recommendations"
  schema     = file("schemas/recommendation_schema.json")
  deletion_protection=false
}
