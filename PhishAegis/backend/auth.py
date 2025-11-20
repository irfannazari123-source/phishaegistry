from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
import os

# MongoDB setup
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client.phishguard


def setup_auth(app):
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-secret-key')
    jwt = JWTManager(app)
    return jwt


def create_user(user_info):
    user = {
        'email': user_info['email'],
        'name': user_info['name'],
        'picture': user_info['picture'],
        'created_at': datetime.now(),
        'last_login': datetime.now()
    }

    result = db.users.update_one(
        {'email': user_info['email']},
        {'$set': user},
        upsert=True
    )

    return user


def get_user_stats(user_email):
    total_emails = db.emails.count_documents({'user_id': user_email})
    phishing_emails = db.emails.count_documents({'user_id': user_email, 'is_phishing': True})

    return {
        'total_emails': total_emails,
        'phishing_emails': phishing_emails,
        'detection_rate': (phishing_emails / total_emails * 100) if total_emails > 0 else 0
    }