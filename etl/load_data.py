import pandas as pd
from sklearn.datasets import load_breast_cancer
import os
import config

def load_data(output_path=None):
    data = load_breast_cancer(as_frame=True)
    df = data.frame
    if output_path is None:
        output_path = os.path.join(config.RESULTS_DIR, config.DATA_FILE)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path

if __name__ == '__main__':
    path = load_data()
    print(f"Data saved to {path}")
