from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "kacper",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="market_data_pipeline",
    default_args=default_args,
    description="Run market data ETL pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["market-data", "etl"],
) as dag:
    run_etl = BashOperator(
        task_id="run_etl_pipeline",
        bash_command="cd /opt/airflow/project && python -m app.main",
    )