from flask import Flask, request, jsonify, send_from_directory
import pprint
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
mongo = PyMongo(app)

def format_event(event):
    action = event.get('action')
    author = event.get('author')
    from_branch = event.get('from_branch')
    to_branch = event.get('to_branch')
    timestamp = event.get('timestamp')
    if action == 'PUSH':
        return f'"{author}" Pushed to "{to_branch}" on {timestamp}'
    elif action == 'PULL_REQUEST':
        return f'"{author}" Submitted a Pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
    elif action == 'MERGE':
        return f'"{author}" Merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
    return ''

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("\n--- Incoming GitHub Webhook Payload ---", flush=True)
    pprint.pprint(data, stream=None)
    event = None
    github_event = request.headers.get('X-GitHub-Event')
    # Handle push event
    if github_event == 'push' or (data.get('ref') and data.get('commits')):
        event = {
            'request_id': data.get('after'),
            'author': data.get('pusher', {}).get('name') or data.get('pusher', {}).get('email'),
            'action': 'PUSH',
            'from_branch': None,
            'to_branch': data.get('ref', '').split('/')[-1],
            'timestamp': datetime.utcnow().strftime('%d %b %Y - %I:%M %p UTC')
        }
    # Handle pull request event
    elif github_event == 'pull_request' or data.get('pull_request'):
        pr = data.get('pull_request', {})
        event = {
            'request_id': str(pr.get('id') or data.get('number')),
            'author': pr.get('user', {}).get('login'),
            'action': 'PULL_REQUEST',
            'from_branch': pr.get('head', {}).get('ref'),
            'to_branch': pr.get('base', {}).get('ref'),
            'timestamp': datetime.utcnow().strftime('%d %b %Y - %I:%M %p UTC')
        }
        if pr.get('merged'):
            event['action'] = 'MERGE'
    else:
        event = {
            'request_id': data.get('request_id'),
            'author': data.get('author'),
            'action': data.get('action'),
            'from_branch': data.get('from_branch'),
            'to_branch': data.get('to_branch'),
            'timestamp': data.get('timestamp') or datetime.utcnow().strftime('%d %b %Y - %I:%M %p UTC')
        }
    print("--- Parsed Event to Store ---", flush=True)
    pprint.pprint(event, stream=None)
    if event:
        mongo.db.events.insert_one(event)
        return jsonify({'status': 'success'}), 201
    else:
        return jsonify({'status': 'ignored', 'reason': 'Unrecognized event'}), 400

@app.route('/events', methods=['GET'])
def get_events():
    events = list(mongo.db.events.find().sort('timestamp', -1).limit(20))
    for e in events:
        e['_id'] = str(e['_id'])
        e['display'] = format_event(e)
    return jsonify(events)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)