from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python import PythonOperator
from app.test import start
import pandas as pd
import sqlalchemy

path_temp_csv = "/tmp/dataset.csv"
email_failed = "felipesf05@gmail.com"

dag = DAG(
    dag_id="elt-pipeline1",
    description="TESTE de descricao",
    start_date=days_ago(2),
    schedule_interval=None,
)

extract_task = PythonOperator(
    task_id="Extract_Dataset", 
    python_callable=start,
    email_on_failure=True,
    email=email_failed, 
    dag=dag
)

email_task = EmailOperator(
    task_id="Notify",
    email_on_failure=True,
    email=email_failed, 
    to='felipesf05@gmail.com',
    subject='Pipeline Finalizado',
    html_content='<p> O Pipeline para atualizacao de dados entre os ambientes OLTP e OLAP foi finalizado com sucesso. <p>',
    dag=dag)

extract_task >> email_task
