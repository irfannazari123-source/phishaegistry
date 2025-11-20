from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
import os
from pymongo import MongoClient
from email_monitor import email_monitor

app = Flask(__name__)
# Add these routes to your existing app.py:

@app.route('/api/emails/start-monitoring', methods=['POST'])
@jwt_required()
def start_email_monitoring():
    current_user = get_jwt_identity()

    # For demo, we don't need real credentials
    demo_credentials = {
        'email': 'demo@phishguard.ai',
        'password': 'demo',
        'demo': True
    }

    email_monitor.start_monitoring(current_user, demo_credentials)
    return jsonify({'message': 'Email monitoring started', 'mode': 'demo'})


@app.route('/api/emails/stop-monitoring', methods=['POST'])
@jwt_required()
def stop_email_monitoring():
    email_monitor.stop_monitoring()
    return jsonify({'message': 'Email monitoring stopped'})


@app.route('/api/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    current_user = get_jwt_identity()

    # Mock alerts for demo
    alerts = [
        {
            '_id': '1',
            'subject': 'High probability phishing detected',
            'probability': 0.95,
            'triggered_at': datetime.now().isoformat(),
            'is_read': False
        }
    ]

    return jsonify(alerts)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

CORS(app)
jwt = JWTManager(app)

# MongoDB setup
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client.phishguard

# Mock user data for demo
users_db = {
    'demo@phishguard.ai': {
        'email': 'demo@phishguard.ai',
        'name': 'Demo User',
        'picture': 'https://via.placeholder.com/150/1a73e8/ffffff?text=DU'
    }
}


@app.route('/api/auth/demo', methods=['POST'])
def demo_auth():
    """Demo authentication endpoint (replace with Google OAuth in production)"""
    user_data = users_db['demo@phishguard.ai']
    access_token = create_access_token(identity=user_data['email'])

    return jsonify({
        'access_token': access_token,
        'user': user_data
    })


@app.route('/api/stats', methods=['GET'])
@jwt_required()
def get_stats():
    current_user = get_jwt_identity()

    # Mock statistics for demo
    return jsonify({
        'total_emails': 1247,
        'phishing_emails': 24,
        'today_emails': 89,
        'detection_rate': 98.7
    })


@app.route('/api/emails', methods=['GET'])
@jwt_required()
def get_emails():
    # Mock email data for demo
    mock_emails = [
        {
            '_id': '1',
            'subject': 'Urgent: Verify Your Bank Account',
            'body_preview': 'Please verify your bank account immediately by clicking the link below...',
            'received_at': '2023-12-01T10:30:00',
            'is_phishing': True,
            'probability': 0.95
        },
        {
            '_id': '2',
            'subject': 'Meeting Scheduled for Tomorrow',
            'body_preview': 'Hi team, we have a meeting scheduled for tomorrow at 10 AM...',
            'received_at': '2023-12-01T09:15:00',
            'is_phishing': False,
            'probability': 0.12
        }
    ]

    return jsonify(mock_emails)


@app.route('/api/emails/start-monitoring', methods=['POST'])
@jwt_required()
def start_monitoring():
    return jsonify({'message': 'Email monitoring started (demo mode)'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)