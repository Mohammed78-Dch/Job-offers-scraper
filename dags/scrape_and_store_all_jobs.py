from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sys
sys.path.append('/home/mohammed/airflow/dags/scripts')
# from scraper import scrape_bank_reviews  # Importer la fonction de scraping
from insert_data_to_json_all_jobs import insert_data_to_json


# Configuration du DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 13),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(minutes=30),  # Augmenter le délai d'attente

}

dag = DAG(
    'scrape_and_store_all_jobs',
    default_args=default_args,
    description='DAG pour scraper et insérer les avis bancaires',
    schedule_interval='@weekly',  # Exécution hebdomadaire
    catchup=False,
)

# Tâche pour insérer les données
insert_task_json = PythonOperator(
    task_id='scrape_and_insert_data_to_json',
    python_callable=insert_data_to_json,
    provide_context=True,  # Permet de récupérer les logs d'Airflow
    dag=dag,
)



insert_task_json 
