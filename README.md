# ML Pipeline Demo

This project demonstrates a simple machine learning pipeline orchestrated with **Apache Airflow**. The pipeline trains a logistic regression model on the Breast Cancer Wisconsin dataset and stores the resulting model and metrics in the `results/final/` directory.

## Project Structure

```
.
├── dags/                # Airflow DAG
├── etl/                 # Modular ETL scripts
├── results/             # Saved model and metrics
├── logs/                # Airflow logs
├── config.py            # Paths configuration
└── README.md
```

## Pipeline Steps

1. **Load Data** – fetch the dataset with `sklearn.datasets.load_breast_cancer` and save it as CSV.
2. **Preprocess** – cleanup (column normalization, duplicate removal, scaling).
3. **Train Model** – train `LogisticRegression` and persist the model with `joblib`.
4. **Evaluate** – calculate accuracy, precision, recall and F1; store metrics in JSON.
5. **Save Results** – copy resulting artifacts to `results/final/` (placeholder for cloud upload).

A simplified flow is:

```
load_data -> preprocess -> train_model -> evaluate -> save_results
```

## DAG

The DAG `ml_pipeline` in `dags/pipeline_dag.py` uses `PythonOperator` tasks for each step. The DAG has no schedule by default (manual trigger) and keeps tasks in order via `t1 >> t2 >> t3 >> t4 >> t5` dependencies.

Example manual task test:

```bash
airflow tasks test ml_pipeline load_data 2023-01-01
```

## Running Locally

Install requirements and execute the scripts directly if Airflow is unavailable:

```bash
pip install -r requirements.txt
python etl/load_data.py
python etl/preprocess.py
python etl/train_model.py
python etl/evaluate.py
python etl/save_results.py
```

Artifacts (`model.pkl` and `metrics.json`) will appear in `results/final/`.
The `results/` folder is created automatically when the pipeline runs, even though it is ignored by git.

## Integration

For demonstration, the integration step simply copies artifacts to `results/final/`. In a real environment this function can be extended to upload files to cloud storage (S3, Google Drive, etc.) using credentials stored outside the repository.

## Error Handling & Robustness

Each step can be run independently which allows retries and isolation. Airflow's built‑in retry parameters can be set per task. Logs are stored in `logs/` when running under Airflow. Typical failure points include unavailable data source or corrupted files; these are mitigated by using built‑in dataset and simple CSV operations.

