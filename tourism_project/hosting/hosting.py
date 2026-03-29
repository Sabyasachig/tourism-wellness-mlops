"""hosting.py
Uploads the deployment folder (Dockerfile, app.py, requirements.txt) to a
Hugging Face Space running Streamlit (docker SDK).
Triggered as the fourth job (deploy) in the GitHub Actions pipeline.
"""
from huggingface_hub import HfApi, create_repo
from huggingface_hub.utils import RepositoryNotFoundError
import os
import time

# ── CONFIG ────────────────────────────────────────────────────────────────────
HF_USERNAME = os.getenv("HF_USERNAME", "sabyasachighosh")
SPACE_REPO  = f"{HF_USERNAME}/tourism-wellness-app"
HF_TOKEN    = os.getenv("HF_TOKEN")

api = HfApi(token=HF_TOKEN)

# ── DELETE SPACE IF IT EXISTS (ensures clean redeploy, avoids 412 conflict) ──
try:
    api.repo_info(repo_id=SPACE_REPO, repo_type="space")
    print(f"Space '{SPACE_REPO}' already exists. Deleting for clean redeploy...")
    api.delete_repo(repo_id=SPACE_REPO, repo_type="space")
    time.sleep(3)  # brief pause to let HF process the deletion
    print("Deleted.")
except RepositoryNotFoundError:
    print("Space does not exist yet. Will create fresh.")

# ── CREATE SPACE ──────────────────────────────────────────────────────────────
create_repo(
    repo_id=SPACE_REPO,
    repo_type="space",
    space_sdk="docker",
    private=False,
    token=HF_TOKEN,
)
print(f"Created Hugging Face Space: {SPACE_REPO}")

# ── UPLOAD DEPLOYMENT FOLDER ──────────────────────────────────────────────────
api.upload_folder(
    folder_path="tourism_project/deployment",
    repo_id=SPACE_REPO,
    repo_type="space",
    commit_message="Deploy tourism wellness app",
)
print(f"\nDeployment files uploaded to Space: {SPACE_REPO}")
print(f"App will be live at: https://huggingface.co/spaces/{SPACE_REPO}")

print(f"Your app will be live at: https://huggingface.co/spaces/{SPACE_REPO}")
