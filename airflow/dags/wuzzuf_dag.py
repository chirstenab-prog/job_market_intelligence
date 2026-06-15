from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import sys

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_scraper():
    subprocess.run([sys.executable, 
        r"C:\Users\Admin\job_market_intelligence\scraper\wuzzuf_scraper.py"], 
        check=True)

def run_transform():
    subprocess.run([sys.executable, 
        r"C:\Users\Admin\job_market_intelligence\transformation\transform.py"], 
        check=True)

def run_load():
    subprocess.run([sys.executable, 
        r"C:\Users\Admin\job_market_intelligence\warehouse\load_to_db.py"], 
        check=True)

with DAG(
    dag_id="wuzzuf_pipeline",
    default_args=default_args,
    description="Job Market Intelligence Pipeline",
    schedule="0 9 * * *",  # كل يوم الساعة 9 الصبح
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    scrape = PythonOperator(
        task_id="scrape_wuzzuf",
        python_callable=run_scraper,
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=run_transform,
    )

    load = PythonOperator(
        task_id="load_to_db",
        python_callable=run_load,
    )

    scrape >> transform >> load