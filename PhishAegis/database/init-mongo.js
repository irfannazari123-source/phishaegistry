db = db.getSiblingDB('phishguard');

// Create collections
db.createCollection('users');
db.createCollection('emails');
db.createCollection('alerts');

// Create indexes
db.users.createIndex({ "email": 1 }, { unique: true });
db.emails.createIndex({ "user_id": 1, "received_at": -1 });
db.alerts.createIndex({ "user_id": 1, "triggered_at": -1 });

print("PhishGuard AI database initialized successfully");