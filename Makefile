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

# deploy only function
function-deploy:
	rm -f cloud_function.zip  # Remove old zip file if it exists
	cd cloud_function && zip -FSr ../cloud_function.zip main.py requirements.txt task1_column_mapping.py task1_process_supplier_1.py 
	task1_process_supplier_2.py task3_process_buyer_preferences task3_process_supplier_1.py task3_process_supplier_.py && cd ..
	unzip -l cloud_function.zip  # Verify the contents of the zip file
	gcloud functions deploy data-ingestion-function \
	  --region=europe-west3 \
	  --runtime=python311 \
	  --trigger-resource=vanilla-steel-data \
	  --trigger-event=google.storage.object.finalize \
	  --entry-point=ingest_data \
	  --source=./cloud_function

# Upload Test File to Trigger Cloud Function
upload-task1-supplier1:
	gsutil cp resources/task_1/supplier_data_1.xlsx gs://$(DATA_BUCKET)

upload-task1-supplier2:
	gsutil cp resources/task_1/supplier_data_2.xlsx gs://$(DATA_BUCKET)

upload-task3-buyer:
	gsutil cp resources/task_3/buyer_preferences.xlsx gs://$(DATA_BUCKET)

upload-task3-supplier1:
	gsutil cp resources/task_3/supplier_data1.xlsx gs://$(DATA_BUCKET)

upload-task3-supplier2:
	gsutil cp resources/task_3/supplier_data2.xlsx gs://$(DATA_BUCKET)

upload-deals:
	gsutil cp resources/task_2/deals.csv gs://$(DATA_BUCKET)

upload_all: upload-task1-supplier1 upload-task1-supplier2 upload-task3-buyer upload-task3-supplier1 upload-task3-supplier2


# View Cloud Function Logs
logs:
	gcloud functions logs read --region=$(REGION) --limit=20

# Check if Data is in BigQuery 
query1:
	bq query --use_legacy_sql=false 'SELECT * FROM vanilla_steel.inventory_dataset LIMIT 10'

query2:
	bq query --use_legacy_sql=false 'SELECT * FROM vanilla_steel.buyer_preferences LIMIT 10'

query3:
	bq query --use_legacy_sql=false 'SELECT * FROM vanilla_steel.supplier_data_1 LIMIT 10'

query4:
	bq query --use_legacy_sql=false 'SELECT * FROM vanilla_steel.supplier_data_2 LIMIT 10'

query5:
	bq query --use_legacy_sql=false 'SELECT * FROM vanilla_steel.deals LIMIT 10'

# DELETE Data in BigQuery (Task 1 - First)
delquery1:
	bq query --use_legacy_sql=false 'DELETE FROM `vanilla_steel.inventory_dataset` WHERE TRUE;'

delquery2:
	bq query --use_legacy_sql=false 'DELETE FROM `vanilla_steel.buyer_preferences` WHERE TRUE;'

delquery3:
	bq query --use_legacy_sql=false 'DELETE FROM `vanilla_steel.supplier_data_1` WHERE TRUE;'

delquery4:
	bq query --use_legacy_sql=false 'DELETE FROM `vanilla_steel.supplier_data_2` WHERE TRUE;'

delquery5:
	bq query --use_legacy_sql=false 'DELETE FROM `vanilla_steel.deals` WHERE TRUE;'

delquery_all: delquery1 delquery2 delquery3 delquery4 