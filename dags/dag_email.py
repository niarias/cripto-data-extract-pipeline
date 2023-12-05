from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from scripts.email import send_email


with DAG(
    dag_id="email_dag",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    schedule_interval="0 0 * * *",
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    }
) as dag:

    dummy_start_task = DummyOperator(
        task_id="dummy_start"
    )

    dummy_email_task = PythonOperator(
        task_id="dummy_email",
        python_callable=send_email
    )

    dummy_end_task = DummyOperator(
        task_id="dummy_end"
    )

    dummy_start_task >> dummy_email_task >> dummy_end_task
