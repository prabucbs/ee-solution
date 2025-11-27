
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GITHUB_URL = "https://api.github.com/users/{user}/gists"

@app.route("/<user>", methods=["GET"])
def get_public_gists(user):
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=30, type=int)

    url = GITHUB_URL.format(user=user)
    params = {"page": page, "per_page": per_page}

    r = requests.get(url, params=params, timeout=10)

    if r.status_code == 404:
        return jsonify({"detail": "GitHub user not found"}), 404
    if r.status_code != 200:
        return jsonify({"detail": r.text}), r.status_code

    raw = r.json()

    gists = []
    for g in raw:
        gists.append({
            "id": g.get("id"),
            "description": g.get("description"),
            "html_url": g.get("html_url"),
            "files": list(g.get("files", {}).keys())
        })

    return jsonify({
        "user": user,
        "page": page,
        "per_page": per_page,
        "count": len(gists),
        "gists": gists
    })

@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
