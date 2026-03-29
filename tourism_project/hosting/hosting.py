"""hosting.py
Uploads the deployment folder (Dockerfile, app.py, requirements.txt) to a
Hugging Face Space running Streamlit.
Triggered as the fourth job (deploy) in the GitHub Actions pipeline.
"""
from huggingface_hub import HfApi, create_repo
from huggingface_hub.utils import RepositoryNotFoundError
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
HF_USERNAME = os.getenv("HF_USERNAME", "sabyasachighosh")
SPACE_REPO  = f"{HF_USERNAME}/tourism-wellness-app"
HF_TOKEN    = os.getenv("HF_TOKEN")

api = HfApi(token=HF_TOKEN)

# ── CREATE SPACE IF NEEDED ────────────────────────────────────────────────────
try:
    api.repo_info(repo_id=SPACE_REPO, repo_type="space")
    print(f"Space '{SPACE_REPO}' already exists.")
except RepositoryNotFoundError:
    create_repo(
        repo_id=SPACE_REPO,
        repo_type="space",
        space_sdk="docker",   # HF no longer accepts "streamlit"; Streamlit apps use "docker" SDK
        private=False,
        token=HF_TOKEN,
    )
    print(f"Created Hugging Face Space: {SPACE_REPO}")

# ── UPLOAD DEPLOYMENT FOLDER ──────────────────────────────────────────────────
api.upload_folder(
    folder_path="tourism_project/deployment",
    repo_id=SPACE_REPO,
    repo_type="space",
)
print(f"\nDeployment files uploaded to Space: {SPACE_REPO}")
print(f"Your app will be live at: https://huggingface.co/spaces/{SPACE_REPO}")
