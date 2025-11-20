import imaplib
import email
from email.header import decode_header
import re
import threading
import time
from datetime import datetime
from pymongo import MongoClient
import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class EmailProcessor:
    @staticmethod
    def extract_features(email_text):
        """Extract features from email text for phishing detection"""
        if not email_text:
            email_text = ""

        features = {}

        # Text-based features
        features['length'] = len(email_text)
        features['num_links'] = len(
            re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_text))
        features['num_attachments'] = email_text.count('Content-Disposition: attachment')
        features['suspicious_words'] = len(re.findall(
            r'urgent|verify|password|security|update|account|login|confirm|bank|paypal|suspend|limited|warning',
            email_text, re.I))
        features['has_html'] = 1 if '<html' in email_text.lower() else 0
        features['special_chars'] = len(re.findall(r'[^\w\s]', email_text))
        features['uppercase_ratio'] = sum(1 for c in email_text if c.isupper()) / max(1, len(email_text))

        # Suspicious patterns
        features['suspicious_sender'] = 1 if re.search(r'[\d{5,}]@|support@\w+\.\w+\.\w+', email_text, re.I) else 0
        features['shortened_links'] = len(re.findall(r'bit\.ly|goo\.gl|tinyurl|t\.co', email_text, re.I))

        return features

    @staticmethod
    def preprocess_email(raw_email):
        """Extract and clean email content"""
        try:
            msg = email.message_from_string(raw_email)
            subject = ""
            body = ""

            # Decode subject
            if msg['subject']:
                subject_parts = decode_header(msg['subject'])
                for part, encoding in subject_parts:
                    if isinstance(part, bytes):
                        subject += part.decode(encoding or 'utf-8', errors='ignore')
                    else:
                        subject += str(part)

            # Extract body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True)
                        if body:
                            body = body.decode('utf-8', errors='ignore')
                        break
                    elif content_type == "text/html" and "attachment" not in content_disposition and not body:
                        body = part.get_payload(decode=True)
                        if body:
                            body = body.decode('utf-8', errors='ignore')
            else:
                body = msg.get_payload(decode=True)
                if body:
                    body = body.decode('utf-8', errors='ignore')

            # Clean body
            if body:
                body = re.sub(r'<.*?>', '', body)  # Remove HTML tags
                body = re.sub(r'\s+', ' ', body)  # Remove extra whitespace
                body = body.strip()

            return subject, body or ""

        except Exception as e:
            print(f"Error processing email: {e}")
            return "", ""


class PhishingModel:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.load_model()

    def load_model(self):
        """Load the trained ML model and vectorizer"""
        try:
            model_path = 'ml-model/phishing_model.pkl'
            vectorizer_path = 'ml-model/vectorizer.pkl'

            if os.path.exists(model_path) and os.path.exists(vectorizer_path):
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                print("✅ ML model loaded successfully")
            else:
                print("⚠️  No pre-trained model found. Using rule-based detection.")
                self.model = None
                self.vectorizer = None

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
            self.vectorizer = None

    def predict(self, subject, body):
        """Predict if email is phishing using ML or rule-based fallback"""
        text = f"{subject} {body}"

        if self.model and self.vectorizer:
            # Use ML model for prediction
            try:
                features_vector = self.vectorizer.transform([text])
                prediction = self.model.predict(features_vector)[0]
                probability = self.model.predict_proba(features_vector)[0][1]
                return bool(prediction), float(probability)
            except Exception as e:
                print(f"ML prediction failed, using rule-based: {e}")

        # Rule-based fallback
        processor = EmailProcessor()
        features = processor.extract_features(text)

        # Calculate probability based on features
        probability = min(
            features['suspicious_words'] * 0.15 +
            features['num_links'] * 0.2 +
            features['shortened_links'] * 0.3 +
            features['suspicious_sender'] * 0.2 +
            (features['uppercase_ratio'] > 0.3) * 0.15,
            0.95
        )

        prediction = 1 if probability > 0.5 else 0
        return bool(prediction), float(probability)


class EmailMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.thread = None
        self.model = PhishingModel()
        self.client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
        self.db = self.client.phishguard

    def start_monitoring(self, user_id, email_credentials=None):
        """Start monitoring emails for a user"""
        if self.is_monitoring:
            print("⚠️  Monitoring already active")
            return

        self.is_monitoring = True
        self.thread = threading.Thread(target=self._monitor_emails, args=(user_id, email_credentials))
        self.thread.daemon = True
        self.thread.start()
        print(f"✅ Started email monitoring for user: {user_id}")

    def stop_monitoring(self):
        """Stop email monitoring"""
        self.is_monitoring = False
        if self.thread:
            self.thread.join(timeout=5)
        print("⏹️  Email monitoring stopped")

    def _monitor_emails(self, user_id, email_credentials):
        """Main email monitoring loop"""
        processor = EmailProcessor()

        while self.is_monitoring:
            try:
                # In demo mode, simulate email processing
                if not email_credentials or email_credentials.get('demo', True):
                    self._process_demo_emails(user_id, processor)
                else:
                    # Real email monitoring (commented for demo)
                    # self._process_real_emails(user_id, email_credentials, processor)
                    pass

            except Exception as e:
                print(f"❌ Error in email monitoring: {e}")

            # Check every 30 seconds in demo mode
            time.sleep(30)

    def _process_demo_emails(self, user_id, processor):
        """Process demo emails for testing"""
        demo_emails = [
            {
                'subject': 'Urgent: Verify Your Bank Account',
                'body': 'Dear customer, we detected suspicious activity on your account. Please verify your bank account immediately by clicking here: http://fake-bank-security.com/verify',
                'is_phishing': True
            },
            {
                'subject': 'Meeting Scheduled for Tomorrow',
                'body': 'Hi team, we have a meeting scheduled for tomorrow at 10 AM in the main conference room. Please bring your project updates.',
                'is_phishing': False
            },
            {
                'subject': 'Your Account Will Be Suspended',
                'body': 'IMPORTANT: Your account will be suspended in 24 hours unless you confirm your details. Click here: http://secure-verify-account.com',
                'is_phishing': True
            },
            {
                'subject': 'Project Update Request',
                'body': 'Hello, could you please provide an update on the current project status? We need to prepare for the client meeting next week.',
                'is_phishing': False
            }
        ]

        for demo_email in demo_emails:
            if not self.is_monitoring:
                break

            # Predict using ML model
            is_phishing, probability = self.model.predict(
                demo_email['subject'],
                demo_email['body']
            )

            # Store in database
            email_data = {
                'user_id': user_id,
                'subject': demo_email['subject'],
                'body': demo_email['body'],
                'body_preview': demo_email['body'][:200] + '...' if len(demo_email['body']) > 200 else demo_email[
                    'body'],
                'received_at': datetime.now(),
                'is_phishing': is_phishing,
                'probability': probability,
                'is_demo': True
            }

            # Insert email record
            result = self.db.emails.insert_one(email_data)

            # Create alert if phishing detected
            if is_phishing and probability > 0.7:
                alert_data = {
                    'user_id': user_id,
                    'email_id': str(result.inserted_id),
                    'subject': demo_email['subject'],
                    'probability': probability,
                    'triggered_at': datetime.now(),
                    'is_read': False,
                    'is_demo': True
                }
                self.db.alerts.insert_one(alert_data)
                print(f"🚨 Phishing alert created: {demo_email['subject']} (Probability: {probability:.2f})")

            # Wait between demo emails
            time.sleep(10)

    def _process_real_emails(self, user_id, email_credentials, processor):
        """Process real emails from IMAP server"""
        try:
            # Connect to Gmail
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(email_credentials['email'], email_credentials['password'])
            mail.select('inbox')

            # Search for unseen emails
            status, messages = mail.search(None, 'UNSEEN')
            email_ids = messages[0].split()

            for email_id in email_ids:
                if not self.is_monitoring:
                    break

                status, msg_data = mail.fetch(email_id, '(RFC822)')
                raw_email = msg_data[0][1].decode('utf-8', errors='ignore')

                # Process email
                subject, body = processor.preprocess_email(raw_email)

                # Predict using ML model
                is_phishing, probability = self.model.predict(subject, body)

                # Store result
                email_data = {
                    'user_id': user_id,
                    'subject': subject,
                    'body': body,
                    'body_preview': body[:200] + '...' if len(body) > 200 else body,
                    'received_at': datetime.now(),
                    'is_phishing': is_phishing,
                    'probability': probability,
                    'is_demo': False
                }

                result = self.db.emails.insert_one(email_data)

                # Trigger alert if phishing
                if is_phishing:
                    alert_data = {
                        'user_id': user_id,
                        'email_id': str(result.inserted_id),
                        'subject': subject,
                        'probability': probability,
                        'triggered_at': datetime.now(),
                        'is_read': False,
                        'is_demo': False
                    }
                    self.db.alerts.insert_one(alert_data)

            mail.close()
            mail.logout()

        except Exception as e:
            print(f"❌ Error processing real emails: {e}")


# Global instance
email_monitor = EmailMonitor()