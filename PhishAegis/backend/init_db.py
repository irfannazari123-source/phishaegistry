from pymongo import MongoClient
import os


def init_database():
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
    db = client.phishguard

    # Create indexes
    db.emails.create_index([('user_id', 1), ('received_at', -1)])
    db.alerts.create_index([('user_id', 1), ('triggered_at', -1)])
    db.users.create_index('email', unique=True)

    print("Database initialized with indexes")


if __name__ == '__main__':
    init_database()