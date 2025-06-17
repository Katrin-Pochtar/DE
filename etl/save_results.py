import shutil
import os
import config


def save_to_storage(source_paths, dest_dir=None):
    if dest_dir is None:
        dest_dir = config.RESULTS_DIR
    os.makedirs(dest_dir, exist_ok=True)
    for p in source_paths:
        shutil.copy(p, dest_dir)

if __name__ == '__main__':
    paths = [
        os.path.join(config.RESULTS_DIR, config.MODEL_FILE),
        os.path.join(config.RESULTS_DIR, config.METRICS_FILE)
    ]
    save_to_storage(paths)
    print('Results saved')
