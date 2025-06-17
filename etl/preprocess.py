import pandas as pd
import os
import config


def preprocess(input_path, output_path=None):
    df = pd.read_csv(input_path)
    # simple preprocessing: lowercase column names
    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
    if output_path is None:
        output_path = input_path  # overwrite
    df.to_csv(output_path, index=False)
    return output_path

if __name__ == '__main__':
    input_path = os.path.join(config.RESULTS_DIR, config.DATA_FILE)
    preprocess(input_path)
    print(f"Preprocessed data saved to {input_path}")
