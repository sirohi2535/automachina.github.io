from http.server import BaseHTTPRequestHandler, HTTPServer
from commit_engine import make_commit
import json, urllib.parse, os, datetime

DATA = "data/repos.json"


class API(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path == "/repos":
            self.send_json("data/repos.json")

        elif path.startswith("/file"):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            repo = q["repo"][0]
            file = q["file"][0]
            data = json.load(open("data/repos.json"))
            self.respond(data[repo]["files"][file])

        else:
            self.respond("GitMachina API Running")

    def send_json(self, file):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(open(file).read().encode())

    def respond(self, text):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(text.encode())

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path == "/repos":
            self.send_json(DATA)

        elif path.startswith("/file"):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            repo = q["repo"][0]
            file = q["file"][0]
            data = json.load(open(DATA))
            self.respond(data[repo]["files"][file])

        else:
            self.respond("GitMachina API Running")

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)
        data = urllib.parse.parse_qs(body.decode())

        repos = json.load(open(DATA))

        # 🆕 CREATE REPO
        if self.path == "/create_repo":
            name = data["name"][0]
            repos[name] = {
                "owner": "sirohi2535",
                "files": {}
            }
            json.dump(repos, open(DATA,"w"), indent=2)
            self.respond("REPO CREATED")

        # 🆕 UPLOAD FILE
        if self.path == "/upload":
            repo = data["repo"][0]
            fname = data["filename"][0]
            content = data["content"][0]
            repos[repo]["files"][fname] = content
            json.dump(repos, open(DATA,"w"), indent=2)
            self.respond("FILE UPLOADED")

    def send_json(self, file):
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(open(file).read().encode())

    def respond(self, txt):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(txt.encode())

@app.route("/commit", methods=["POST"])
def commit():
    repo = request.form["repo"]
    msg = request.form["message"]
    c = make_commit(repo, REPOS, msg)
    return {"status":"ok","commit":c}

@app.route("/commits")
def commits():
    repo = request.args.get("repo")
    return REPOS[repo].get("commits", [])

# CREATE BRANCH
@app.route("/branch/create", methods=["POST"])
def create_branch():
    repo = request.form["repo"]
    name = request.form["branch"]

    r = repos[repo]
    base = r["active"]

    if name in r["branches"]:
        return "Branch already exists"

    r["branches"][name] = {
        "files": r["branches"][base]["files"].copy(),
        "commits": []
    }
    return "Branch created"


# SWITCH BRANCH
@app.route("/branch/switch", methods=["POST"])
def switch_branch():
    repo = request.form["repo"]
    name = request.form["branch"]

    if name not in repos[repo]["branches"]:
        return "Branch not found"

    repos[repo]["active"] = name
    return "Switched to " + name


# GET CURRENT BRANCH
@app.route("/branch/current")
def current_branch():
    repo = request.args.get("repo")
    return jsonify({
        "active": repos[repo]["active"],
        "branches": list(repos[repo]["branches"].keys())
    })

HTTPServer(("0.0.0.0",8080),API).serve_forever()

