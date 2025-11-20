import pickle
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


class PhishingDetector:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.load_model()

    def load_model(self):
        try:
            with open('ml-model/phishing_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            with open('ml-model/vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
            print("ML model loaded successfully")
        except FileNotFoundError:
            print("No pre-trained model found. Using rule-based fallback.")
            self.model = None
            self.vectorizer = None

    def extract_features(self, text):
        features = {}

        if not text:
            text = ""

        # Text-based features
        features['length'] = len(text)
        features['num_links'] = len(
            re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
        features['num_attachments'] = text.count('Content-Disposition: attachment')
        features['suspicious_words'] = len(
            re.findall(r'urgent|verify|password|security|update|account|login|confirm|bank|paypal', text, re.I))
        features['has_html'] = 1 if '<html' in text.lower() else 0
        features['special_chars'] = len(re.findall(r'[^\w\s]', text))

        return features

    def predict(self, subject, body):
        text = f"{subject} {body}"

        if self.model and self.vectorizer:
            # Use ML model
            features_vector = self.vectorizer.transform([text])
            prediction = self.model.predict(features_vector)[0]
            probability = self.model.predict_proba(features_vector)[0][1]
        else:
            # Rule-based fallback
            features = self.extract_features(text)
            probability = min(
                features['suspicious_words'] * 0.15 +
                features['num_links'] * 0.2 +
                (1 if features['has_html'] else 0) * 0.1,
                0.95
            )
            prediction = 1 if probability > 0.5 else 0

        return bool(prediction), float(probability)


# Global instance
phishing_detector = PhishingDetector()