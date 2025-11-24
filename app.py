from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "scores.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"scores": {}, "players": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"scores": {}, "players": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


@app.route("/scores", methods=["GET"])
def get_scores():
    data = load_data()
    return jsonify(data)


@app.route("/scores", methods=["POST"])
def save_scores():
    body = request.get_json(force=True, silent=True) or {}
    scores = body.get("scores", {})
    players = body.get("players", [])

    data = {
        "scores": scores if isinstance(scores, dict) else {},
        "players": players if isinstance(players, list) else [],
    }
    save_data(data)
    return jsonify({"status": "ok"})


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
