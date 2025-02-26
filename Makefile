# Define variables
PROJECT_ID=vanillasteel
REGION=europe-west3

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
deploy: auth init fmt validate plan apply

# Cleanup (destroy infrastructure)
cleanup: destroy
