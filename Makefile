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

# Create ZIP File for Cloud Function (Only `main.py` and `requirements.txt`)
zip-function:
	cd cloud_function && zip -r ../cloud_function.zip main.py requirements.txt

# Upload ZIP File to Google Cloud Storage
upload-function:
	gsutil cp cloud_function.zip gs://$(BUCKET)

# Redeploy Cloud Function
deploy-function: zip-function upload-function apply

# Upload Test File to Trigger Cloud Function
upload-file:
	gsutil cp resources/task_1/supplier_data_1.xlsx gs://$(DATA_BUCKET)

# View Cloud Function Logs
logs:
	gcloud functions logs read --region=$(REGION) --limit=10

# Check if Data is in BigQuery
query:
	bq query --use_legacy_sql=false 'SELECT * FROM vanilla_steel.supplier_data LIMIT 10'


