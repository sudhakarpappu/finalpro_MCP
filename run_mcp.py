import os
from git import Repo  # type: ignore

GH_PAT = os.getenv("GH_PAT")  # Stored securely in GitHub Secrets
REPO_DIR = "/tmp/finalpro"
REPO_URL = f"https://{GH_PAT}@github.com/sudhakarpappu/finalpro.git"


def commit_code_change(file_path: str, content: str, commit_message: str):
    # Clone repo if not already present
    if not os.path.exists(REPO_DIR):
        repo = Repo.clone_from(REPO_URL, REPO_DIR)
    else:
        repo = Repo(REPO_DIR)
        # Make sure repo is up to date
        origin = repo.remotes.origin
        origin.pull()

    # Write new/updated file content
    file_full_path = os.path.join(REPO_DIR, file_path)
    os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
    with open(file_full_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Stage and commit
    repo.git.add(file_path)
    if repo.is_dirty():
        repo.index.commit(commit_message)
        origin = repo.remote(name="origin")
        origin.push()
        print(f"✅ Changes committed and pushed: {commit_message}")
    else:
        print("⚠️ No changes to commit")
