# Vanilla Steel Data Pipeline - Terraform Setup

This project automates **data ingestion, transformation, and reporting** using **Google Cloud Storage, BigQuery, dbt, and Looker**. The infrastructure is managed using **Terraform** and **Cloud Functions**, ensuring seamless data processing.

---

## **System Overview**
This project is structured into **three tasks**:

### **Task 1: Supplier Inventory Processing**
- Users upload **supplier_data_1.xlsx** or **supplier_data_2.xlsx** to **Google Cloud Storage** (`vanilla-steel-data` bucket).
- **Cloud Function** (`data-ingestion-function`) is triggered.
- The function applies **data cleaning**:
  - `task1_process_supplier_1.py` → Cleans Supplier 1 data.
  - `task1_process_supplier_2.py` → Cleans Supplier 2 data.
- Processed data is **stored in BigQuery** (`vanilla_steel.inventory_dataset` table).

### **Task 2: Deals Data Processing & Transformation**
- Users upload **deals.csv** to **Google Cloud Storage** (`vanilla-steel-data` bucket).
- **Cloud Function** processes and loads data into **BigQuery** (`vanilla_steel.deals` table).
- A **dbt job runs once a day** to:
  - Create **aggregated revenue tables**.
  - Generate **account manager performance tables**.
  - Optimize data for **Looker dashboards**.

### **Task 3: Supplier Recommendation System**
- Users upload **supplier_data_1.xlsx** and **supplier_data_2.xlsx** to **Google Cloud Storage**.
- **Cloud Function** processes and stores cleaned data into **BigQuery** as:
  - `vanilla_steel.supplier_data_1`
  - `vanilla_steel.supplier_data_2`
- The **dbt transformation runs daily**, aggregating supplier data and **creating a recommendation table**.
- Looker dashboards automatically refresh with updated data.

---

# 🚀 Deployment Instructions

## 1. Prerequisites
Ensure the following are installed:

- **Terraform** (≥ 1.0)
- **Google Cloud SDK** (`gcloud`)
- **dbt CLI** (`pip install dbt-bigquery`)
- **Make** (`sudo apt install make`)

---

## 2. Authenticate & Enable APIs
Run the following commands to authenticate and enable necessary Google Cloud services:

```sh
gcloud auth application-default login
gcloud services enable storage.googleapis.com \
    cloudfunctions.googleapis.com \
    bigquery.googleapis.com \
    cloudscheduler.googleapis.com \
    iam.googleapis.com
```

---

## 3️. Deploy Infrastructure
Initialize and apply Terraform to set up the infrastructure:

```sh
terraform init
terraform plan
terraform apply -auto-approve
```

---

## 4. Upload Data
Upload required data files to Google Cloud Storage:

```sh
gsutil cp supplier_data_1.xlsx gs://vanilla-steel-data/
gsutil cp supplier_data_2.xlsx gs://vanilla-steel-data/
gsutil cp deals.xlsx gs://vanilla-steel-data/
```

---

## 5️. Check Logs
View logs for Cloud Functions to monitor the pipeline:

```sh
gcloud functions logs read data-ingestion-function --region=europe-west3
gcloud functions logs read dbt-runner-function --region=europe-west3
```

---

## Makefile Commands
Here are some example commands that are available for managing the deployment(Check the Makefile for further commands):

```sh
make apply            # Deploy infrastructure
make destroy          # Remove infrastructure
make upload-suppliers # Upload supplier data - data must be stored in appropiate directory
make upload-deals     # Upload deals data - data must be stored in appropiate directory
make logs             # View Cloud Function logs
```

---

## 📊 Looker Dashboards
Dashboards are connected to **BigQuery** and auto-refresh daily.

### **Data Sources:**
- **Revenue Performance**
- **Account Manager Insights**

---

## Next Steps
- Plan to limit duplication in BigQuery tables.
- Expand pipeline for other sellers and buyers
- Automate failure notifications for data ingestion.
- Expand dbt transformations for deeper analytics.


