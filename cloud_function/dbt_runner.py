import functions_framework
import subprocess
import logging

@functions_framework.http
def run_dbt(request):
    """Runs dbt inside a Cloud Run container and logs the output."""
    try:
        # Run dbt command
        result = subprocess.run(
            ["dbt", "run"],
            text=True,
            capture_output=True,
            check=True
        )
        
        logging.info(f"dbt run output: {result.stdout}")
        return f"dbt run executed successfully.", 200

    except subprocess.CalledProcessError as e:
        logging.error(f"dbt run failed: {e.stderr}")
        return f"dbt run failed: {e.stderr}", 500
