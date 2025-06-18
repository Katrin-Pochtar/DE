import shutil
import os
import config


def save_to_storage(source_paths, dest_dir=None):
    """Copy artifacts to the final storage directory."""
    if dest_dir is None:
        dest_dir = config.FINAL_DIR
    os.makedirs(dest_dir, exist_ok=True)
    for p in source_paths:
        dest_path = os.path.join(dest_dir, os.path.basename(p))
        if os.path.abspath(p) == os.path.abspath(dest_path):
            # Avoid SameFileError when source and destination are identical
            continue
        shutil.copy(p, dest_path)

if __name__ == '__main__':
    paths = [
        os.path.join(config.RESULTS_DIR, config.MODEL_FILE),
        os.path.join(config.RESULTS_DIR, config.METRICS_FILE)
    ]
    save_to_storage(paths)
    print('Results saved')
