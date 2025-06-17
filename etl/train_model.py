import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import os
import config


def train(input_path, model_path=None):
    df = pd.read_csv(input_path)
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    if model_path is None:
        model_path = os.path.join(config.RESULTS_DIR, config.MODEL_FILE)
    joblib.dump(model, model_path)
    return model_path, X_test, y_test

if __name__ == '__main__':
    input_path = os.path.join(config.RESULTS_DIR, config.DATA_FILE)
    train(input_path)
