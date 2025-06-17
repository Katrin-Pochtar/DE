import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import joblib
import json
import os
import config


def evaluate(data_path, model_path=None, metrics_path=None):
    df = pd.read_csv(data_path)
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    if model_path is None:
        model_path = os.path.join(config.RESULTS_DIR, config.MODEL_FILE)
    model = joblib.load(model_path)
    preds = model.predict(X_test)
    metrics = {
        'accuracy': accuracy_score(y_test, preds),
        'precision': precision_score(y_test, preds),
        'recall': recall_score(y_test, preds),
        'f1': f1_score(y_test, preds)
    }
    if metrics_path is None:
        metrics_path = os.path.join(config.RESULTS_DIR, config.METRICS_FILE)
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    return metrics_path

if __name__ == '__main__':
    data_path = os.path.join(config.RESULTS_DIR, config.DATA_FILE)
    evaluate(data_path)
