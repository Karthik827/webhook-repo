from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from app.extensions import MONGODB_URI
from dateutil.parser import parse
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


# Setup MongoDB connection (singleton for blueprint)
client = MongoClient(MONGODB_URI)
db = client['webhook_github']
collection = db['events']

@webhook.route('/receiver', methods=["POST"])
def receiver():
    """
    Receive and process GitHub webhook events (push, pull request, merge).
    """
    try:
        data = request.json
        event_type = request.headers.get('X-GitHub-Event')
        event_data = {}

        if event_type == 'push':
            if not data.get('head_commit') or not data['head_commit'].get('id') or not data['head_commit'].get('timestamp') or not data.get('pusher'):
                return jsonify({'message': 'Invalid push payload'}), 400
            try:
                timestamp = parse(data['head_commit']['timestamp'])
            except ValueError:
                return jsonify({'message': 'Invalid timestamp format'}), 400
            event_data = {
                '_id': data['head_commit']['id'],
                'request_id': data['head_commit']['id'],
                'author': data['pusher']['name'],
                'action': 'PUSH',
                'from_branch': None,
                'to_branch': data['ref'].split('/')[-1],
                'timestamp': timestamp
            }
        elif event_type == 'pull_request':
            if not data.get('pull_request') or not data.get('action') or not data['pull_request'].get('user'):
                return jsonify({'message': 'Invalid pull_request payload'}), 400
            pr = data['pull_request']
            if data.get('action') == 'closed' and pr.get('merged'):
                if not pr.get('merged_at'):
                    return jsonify({'message': 'Missing merged_at timestamp'}), 400
                try:
                    timestamp = parse(pr['merged_at'])
                except ValueError:
                    return jsonify({'message': 'Invalid timestamp format'}), 400
                event_data = {
                    '_id': str(pr['id']),
                    'request_id': str(pr['id']),
                    'author': pr['user']['login'],
                    'action': 'MERGE',
                    'from_branch': pr['head']['ref'],
                    'to_branch': pr['base']['ref'],
                    'timestamp': timestamp
                }
            elif data.get('action') in ['opened', 'reopened']:
                if not pr.get('created_at'):
                    return jsonify({'message': 'Missing created_at timestamp'}), 400
                try:
                    timestamp = parse(pr['created_at'])
                except ValueError:
                    return jsonify({'message': 'Invalid timestamp format'}), 400
                event_data = {
                    '_id': str(pr['id']),
                    'request_id': str(pr['id']),
                    'author': pr['user']['login'],
                    'action': 'PULL_REQUEST',
                    'from_branch': pr['head']['ref'],
                    'to_branch': pr['base']['ref'],
                    'timestamp': timestamp
                }
            else:
                return jsonify({'message': 'Event not supported'}), 400

        if event_data:
            collection.insert_one(event_data)
            return jsonify({'message': 'Event received'}), 200
        return jsonify({'message': 'Event not supported'}), 400
    except Exception as e:
        return jsonify({'message': 'Unexpected error', 'error': str(e)}), 500

@webhook.route('/events', methods=['GET'])
def get_events():
    """
    Fetch and format the 10 most recent webhook events from MongoDB.
    """
    try:
        events = list(collection.find().sort("timestamp", -1).limit(10))
        formatted_events = []
        for event in events:
            event['_id'] = str(event['_id'])
            if 'timestamp' in event and event['timestamp'] is not None:
                try:
                    formatted_time = event['timestamp'].strftime("%d %B %Y - %I:%M %p UTC")
                    event['timestamp'] = formatted_time
                    if event.get('action') == 'MERGE':
                        author = event.get('author', '')
                        from_branch = event.get('from_branch', '')
                        to_branch = event.get('to_branch', '')
                        day = int(formatted_time.split(' ')[0])
                        if 4 <= day <= 20 or 24 <= day <= 30:
                            suffix = 'th'
                        else:
                            suffix = ['st', 'nd', 'rd'][day % 10 - 1]
                        day_str = f"{day}{suffix}"
                        formatted_time_with_suffix = formatted_time.replace(f"{day:02d}", day_str, 1)
                        event['message'] = f'{author} merged branch {from_branch} to {to_branch} on {formatted_time_with_suffix}'
                    formatted_events.append(event)
                except AttributeError:
                    pass
            else:
                pass
        return jsonify(formatted_events), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching events', 'error': str(e)}), 500
