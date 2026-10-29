from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator


def clean_data():
    print("Removing duplicates and empty rows...")


with DAG(
    dag_id="sales_pipeline",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
) as dag:

    download = BashOperator(task_id="download", bash_command="echo 'downloading sales.csv'")
    clean = PythonOperator(task_id="clean", python_callable=clean_data)
    report = BashOperator(task_id="report", bash_command="echo 'building report'")
    archive = BashOperator(task_id="archive", bash_command="echo 'archiving file'")
    notify = BashOperator(task_id="notify", bash_command="echo 'done!'")

    download >> clean >> [report, archive] >> notify
