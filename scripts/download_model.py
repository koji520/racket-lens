import os
from huggingface_hub import hf_hub_download

REPO_ID = "koji520/racket_classifier"
FILENAME = "racket_classifier_model.onnx"
LOCAL_DIR = "app/prediction/models"

os.makedirs(LOCAL_DIR, exist_ok=True)

downloaded_path = hf_hub_download(
    repo_id=REPO_ID,
    filename=FILENAME,
    local_dir=LOCAL_DIR,
)
print(f"Downloaded model to: {downloaded_path}")
