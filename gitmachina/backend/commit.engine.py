import time
import uuid

def make_commit(repo, repos, message):
    commit = {
        "id": uuid.uuid4().hex[:8],
        "message": message,
        "time": int(time.time()),
        "files": repos[repo]["files"].copy()
    }

    repos[repo].setdefault("commits", []).append(commit)
    return commit
