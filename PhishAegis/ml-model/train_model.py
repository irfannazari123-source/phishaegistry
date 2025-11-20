import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import re


def clean_text(text):
    """Clean and preprocess text"""
    if pd.isna(text):
        return ""
    text = re.sub(r'[^\w\s]', ' ', str(text))
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()


def create_training_data():
    """Create comprehensive training data for phishing detection"""

    # Phishing email examples
    phishing_emails = [
        "urgent verify your bank account now click here http://fake-bank.com",
        "your account has been compromised reset password immediately",
        "win free prize claim now limited time offer http://bit.ly/fakelink",
        "security alert suspicious login detected on your account",
        "confirm your email address to receive special offers",
        "your account will be suspended verify now http://secure-login.com",
        "paypal security update required click to verify",
        "you have won a lottery claim your prize now",
        "amazon order problem verify your payment information",
        "microsoft account security verify your identity",
        "bank of america security update required immediately",
        "netflix payment issue update your billing information",
        "facebook security alert confirm your login details",
        "apple id verification required account on hold",
        "irs tax refund claim your money now",
        "google drive storage exceeded verify your account",
        "linkedin security alert unusual login activity",
        "twitter account verification required immediately",
        "instagram suspicious activity verify your account",
        "whatsapp security update required click here"
    ]

    # Legitimate email examples
    legitimate_emails = [
        "meeting scheduled for tomorrow at 10 am conference room",
        "project update attached please review the document",
        "hi john just checking in about the project timeline",
        "invoice attached for your recent purchase",
        "your subscription will renew automatically next week",
        "team lunch this friday at 12 pm",
        "weekly report attached for your review",
        "holiday schedule for the upcoming season",
        "office closed on monday for maintenance",
        "new software update available for download",
        "welcome to the team orientation session tomorrow",
        "performance review scheduled for next week",
        "company picnic this saturday at central park",
        "it maintenance scheduled for tonight at 10 pm",
        "new benefits package information available",
        "training session for new software next monday",
        "department meeting agenda for this week",
        "reminder about the deadline for project submission",
        "thanks for your help with the client presentation",
        "happy birthday enjoy your special day"
    ]

    # Create DataFrame
    emails = phishing_emails + legitimate_emails
    labels = [1] * len(phishing_emails) + [0] * len(legitimate_emails)

    df = pd.DataFrame({
        'text': emails,
        'label': labels
    })

    return df


def train_phishing_model():
    """Train and save the phishing detection model"""
    print("🔄 Creating training data...")
    df = create_training_data()

    print("🔄 Cleaning and preprocessing text...")
    df['cleaned_text'] = df['text'].apply(clean_text)

    # Feature extraction
    print("🔄 Extracting features...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8
    )

    X = vectorizer.fit_transform(df['cleaned_text'])
    y = df['label']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train model
    print("🔄 Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )

    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"✅ Model training completed!")
    print(f"📊 Accuracy: {accuracy:.4f}")
    print(f"📊 Training set size: {len(X_train)}")
    print(f"📊 Test set size: {len(X_test)}")
    print("\n📈 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))

    # Feature importance
    feature_names = vectorizer.get_feature_names_out()
    importances = model.feature_importances_
    top_features = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:10]

    print("\n🔍 Top 10 Important Features:")
    for feature, importance in top_features:
        print(f"  {feature}: {importance:.4f}")

    # Save model and vectorizer
    print("💾 Saving model and vectorizer...")
    with open('phishing_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)

    print("✅ Model and vectorizer saved successfully!")
    print("📁 Files created:")
    print("   - phishing_model.pkl")
    print("   - vectorizer.pkl")

    return model, vectorizer


def test_model(model, vectorizer):
    """Test the trained model with sample emails"""
    test_emails = [
        "verify your bank account now urgent security alert",
        "meeting tomorrow at 10 am bring your reports",
        "claim your free prize money now limited offer",
        "project update attached for your review",
        "your account will be suspended click to verify"
    ]

    print("\n🧪 Model Testing:")
    for i, email in enumerate(test_emails, 1):
        cleaned_text = clean_text(email)
        features = vectorizer.transform([cleaned_text])
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        status = "PHISHING" if prediction == 1 else "LEGITIMATE"
        print(f"Email {i}: {status} (Confidence: {probability:.2%})")
        print(f"   Text: {email}")


if __name__ == '__main__':
    print("🤖 Phishing Detection Model Training")
    print("=" * 50)

    model, vectorizer = train_phishing_model()
    test_model(model, vectorizer)

    print("\n🎉 Training completed! Model is ready for use.")