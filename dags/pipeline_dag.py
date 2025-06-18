from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from etl import load_data, preprocess, train_model, evaluate, save_results

def _load():
    return load_data.load_data()

def _preprocess(ti):
    path = ti.xcom_pull(task_ids='load_data')
    preprocess.preprocess(path)
    return path

def _train():
    input_path = os.path.join(config.RESULTS_DIR, config.DATA_FILE)
    train_model.train(input_path)

def _evaluate():
    input_path = os.path.join(config.RESULTS_DIR, config.DATA_FILE)
    evaluate.evaluate(input_path)

def _save_results():
    paths = [
        os.path.join(config.RESULTS_DIR, config.MODEL_FILE),
        os.path.join(config.RESULTS_DIR, config.METRICS_FILE)
    ]
    save_results.save_to_storage(paths)

with DAG(
    dag_id='ml_pipeline',
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id='load_data',
        python_callable=_load
    )

    t2 = PythonOperator(
        task_id='preprocess',
        python_callable=_preprocess
    )

    t3 = PythonOperator(
        task_id='train_model',
        python_callable=_train
    )

    t4 = PythonOperator(
        task_id='evaluate',
        python_callable=_evaluate
    )

    t5 = PythonOperator(
        task_id='save_results',
        python_callable=_save_results
    )

    t1 >> t2 >> t3 >> t4 >> t5

