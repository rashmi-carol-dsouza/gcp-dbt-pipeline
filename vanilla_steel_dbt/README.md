# **DBT Project - Vanilla Steel**

## **Overview**
This **dbt (Data Build Tool) project** is used to transform and model data for Vanilla Steel on **Google BigQuery**. The project automates data transformation using dbt, providing **cleaned, structured, and optimized** datasets for analytics and reporting.

## **Project Structure**
```
vanilla_steel_dbt/
│── models/                # SQL models (transformation logic)
│   ├── sources.yml
│   ├── suppliers.sql      # Supplier data transformations
│   ├── buyers.sql         # Buyer data transformations
│   ├── recommendations.sql # Final matching model
│── macros/                # Custom macros for dbt
│── tests/                 # Data quality tests
│── snapshots/             # Slowly changing dimension snapshots
│── target/                # dbt compiled and run artifacts (IGNORE THIS IN GIT)
│── logs/                  # Logs for dbt runs (IGNORE THIS IN GIT)
│── profiles.yml           # dbt profile configuration (DO NOT COMMIT)
│── dbt_project.yml        # Main dbt project configuration
│── README.md              # Documentation for the project
```

---

## **Getting Started**
### **1. Prerequisites**
- **Google Cloud Platform (GCP)**
- **BigQuery**
- **Python 3.8+**
- **dbt-core** and **dbt-bigquery**

### **2. Install dbt**
```bash
pip install dbt-core dbt-bigquery
```

### **3. Configure dbt Profiles**
Edit `~/.dbt/profiles.yml` and add:
```yaml
vanilla_steel_dbt:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: your-gcp-project-id
      dataset: vanilla_steel
      threads: 4
      location: europe-west-3
```
👉 **Do not commit `profiles.yml` to Git** because it contains credentials.

---

## **Running dbt**
### **1. Test Connection**
```bash
dbt debug
```

### **2. Run All Models**
```bash
dbt run
```

### **3. Run Specific Model**
```bash
dbt run --select recommendations
```

### **4. Run Tests**
You can add Tests and then run them using the following:
```bash
dbt test
```


### **5. Generate and View Documentation**
```bash
dbt docs generate
dbt docs serve
```



