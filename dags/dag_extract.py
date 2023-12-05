from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.binance import get_binance_pairs, get_24hr_ticker
# Importar DummyOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG(
    dag_id="extract_dag",
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

    create_tables_task = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id="redshift_conn_1",
        sql="sql/creates.sql",
        hook_params={
            "options": "-c search_path=nicolas_ezequiel_arias300_coderhouse"
        }
    )

    # Task 1: Get binance pairs
    get_binance_pairs = PythonOperator(
        task_id="get_binance_pairs",
        python_callable=get_binance_pairs,
        op_kwargs={
            "whitelist": ["BTC", "USDT"]
        }
    )

    dummy_end_task = DummyOperator(
        task_id="dummy_end_task"
    )

    dummy_start_task >> create_tables_task >> get_binance_pairs >> dummy_end_task
