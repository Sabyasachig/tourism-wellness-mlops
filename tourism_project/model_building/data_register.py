"""data_register.py
Creates a Hugging Face dataset repository and uploads tourism.csv to it.
Triggered as the first job in the GitHub Actions CI/CD pipeline.
"""
from huggingface_hub.utils import RepositoryNotFoundError
from huggingface_hub import HfApi, create_repo
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
HF_USERNAME = os.getenv("HF_USERNAME", "sabyasachighosh")
DATASET_REPO_ID = f"{HF_USERNAME}/tourism-wellness-data"
REPO_TYPE = "dataset"
DATA_FILE = "tourism.csv"

# ── INITIALISE API ─────────────────────────────────────────────────────────────
api = HfApi(token=os.getenv("HF_TOKEN"))

# ── CREATE REPO IF NEEDED ─────────────────────────────────────────────────────
try:
    api.repo_info(repo_id=DATASET_REPO_ID, repo_type=REPO_TYPE)
    print(f"Dataset repo '{DATASET_REPO_ID}' already exists.")
except RepositoryNotFoundError:
    create_repo(repo_id=DATASET_REPO_ID, repo_type=REPO_TYPE,
                private=False, token=os.getenv("HF_TOKEN"))
    print(f"Created dataset repo: {DATASET_REPO_ID}")

# ── UPLOAD DATA ───────────────────────────────────────────────────────────────
api.upload_file(
    path_or_fileobj=DATA_FILE,
    path_in_repo="tourism.csv",
    repo_id=DATASET_REPO_ID,
    repo_type=REPO_TYPE,
)
print(f"Uploaded '{DATA_FILE}' to '{DATASET_REPO_ID}'.")
