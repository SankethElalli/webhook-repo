from flask import Flask, request, jsonify
from db import events_collection
from flask_cors import CORS
from models import format_push, format_pull_request, format_merge

app = Flask(__name__)
CORS(app)

@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event_type == "Push":
        data = format_push(payload)

    elif event_type == "Pull_request":
        action = payload["action"]

        if action == "Opened":
            data = format_pull_request(payload)

        elif action == "Closed" and payload["Pull_request"]["Merged"]:
            data = format_merge(payload)

        else:
            return jsonify({"ignored": True}), 200
    else:
        return jsonify({"ignored": True}), 200

    events_collection.insert_one(data)
    return jsonify({"stored": True}), 200


@app.route("/events", methods=["GET"])
def get_events():
    events = list(
        events_collection
        .find({}, {"_id": 0})
        .sort("timestamp", -1)   # LATEST FIRST
        .limit(20)
    )
    return jsonify(events)


if __name__ == "__main__":
    app.run(port=5000)
