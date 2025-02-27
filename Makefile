# Define variables
PROJECT_ID=vanillasteel
REGION=europe-west3
BUCKET=vanilla-steel-function
DATA_BUCKET=vanilla-steel-data

# Authenticate with Google Cloud
auth:
	gcloud auth login
	gcloud auth application-default login
	gcloud config set project $(PROJECT_ID)
	gcloud config set compute/region $(REGION)
	gcloud config set compute/zone $(REGION)-a

# Terraform initialization
init:
	terraform init

# Format Terraform files
fmt:
	terraform fmt

# Validate Terraform syntax
validate:
	terraform validate

# Run Terraform plan
plan:
	terraform plan

# Apply Terraform changes
apply:
	terraform apply --auto-approve

# Destroy Terraform resources
destroy:
	terraform destroy --auto-approve

# Full deployment (auth + terraform apply)
deploy: destroy init plan apply

# Task 1 specific
# Upload Test File to Trigger Cloud Function
upload-file:
	gsutil cp resources/task_1/supplier_data_2.xlsx gs://$(DATA_BUCKET)

# View Cloud Function Logs
logs:
	gcloud functions logs read --region=$(REGION) --limit=20

# Check if Data is in BigQuery
query:
	bq query --use_legacy_sql=false 'SELECT * FROM vanilla_steel.inventory_dataset LIMIT 10'

# DELETE data in Bigquery
delquery:
	bq query --use_legacy_sql=false 'DELETE FROM `vanilla_steel.inventory_dataset` WHERE TRUE;'

# deploy only function
function-deploy:
	rm -f cloud_function.zip  # Remove old zip file if it exists
	cd cloud_function && zip -FSr ../cloud_function.zip main.py requirements.txt column_mapping.py process_supplier_1.py process_supplier_2.py && cd ..
	unzip -l cloud_function.zip  # Verify the contents of the zip file
	gcloud functions deploy data-ingestion-function \
	  --region=europe-west3 \
	  --runtime=python311 \
	  --trigger-resource=vanilla-steel-data \
	  --trigger-event=google.storage.object.finalize \
	  --entry-point=ingest_data \
	  --source=./cloud_function

