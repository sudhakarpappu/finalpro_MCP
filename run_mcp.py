from flask import Flask, request, jsonify
import os
from git import Repo

app = Flask(__name__)

GH_PAT = os.getenv("GH_PAT")
REPO_DIR = "/tmp/finalpro"
REPO_URL = f"https://{GH_PAT}@github.com/sudhakarpappu/finalpro.git"

@app.route("/commit", methods=["POST"])
def commit_code_change():
    data = request.json
    file_path = data.get("file_path")
    content = data.get("content")
    commit_message = data.get("commit_message")

    if not file_path or not content or not commit_message:
        return jsonify({"error": "Missing parameters"}), 400

    if not os.path.exists(REPO_DIR):
        repo = Repo.clone_from(REPO_URL, REPO_DIR)
    else:
        repo = Repo(REPO_DIR)
        repo.remotes.origin.pull()

    file_full_path = os.path.join(REPO_DIR, file_path)
    os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
    with open(file_full_path, "w", encoding="utf-8") as f:
        f.write(content)

    repo.git.add(file_path)
    if repo.is_dirty():
        repo.index.commit(commit_message)
        repo.remote(name="origin").push()
        return jsonify({"status": "success", "message": commit_message})
    else:
        return jsonify({"status": "no changes"})

@app.route("/")
def health():
    return jsonify({"status": "MCP server running ✅"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
