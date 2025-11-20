import React from 'react';
import './About.css';

const About = () => {
  return (
    <div className="about-page">
      <div className="about-header">
        <h1>About PhishGuard AI</h1>
        <p>Advanced AI-powered phishing detection for modern organizations</p>
      </div>

      <div className="about-content">
        <section className="mission-section">
          <h2>Our Mission</h2>
          <p>
            PhishGuard AI was developed to address the growing threat of phishing attacks that target
            organizations and individuals worldwide. Our system leverages cutting-edge artificial
            intelligence and machine learning techniques to identify and neutralize phishing attempts
            before they can cause harm.
          </p>
        </section>

        <section className="technology-section">
          <h2>Technology</h2>
          <div className="tech-grid">
            <div className="tech-card">
              <i className="fas fa-robot"></i>
              <h3>Machine Learning</h3>
              <p>Advanced ML models trained on thousands of phishing and legitimate emails</p>
            </div>
            <div className="tech-card">
              <i className="fas fa-language"></i>
              <h3>Natural Language Processing</h3>
              <p>NLP techniques to understand email content and context</p>
            </div>
            <div className="tech-card">
              <i className="fas fa-bolt"></i>
              <h3>Real-time Processing</h3>
              <p>Instant analysis of incoming emails with minimal latency</p>
            </div>
            <div className="tech-card">
              <i className="fas fa-shield-alt"></i>
              <h3>Security Protocols</h3>
              <p>Integration with SPF, DKIM, and DMARC for enhanced security</p>
            </div>
          </div>
        </section>

        <section className="features-section">
          <h2>How It Works</h2>
          <div className="workflow">
            <div className="workflow-step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Email Collection</h3>
                <p>Connect to your email account via secure IMAP protocol</p>
              </div>
            </div>
            <div className="workflow-step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Content Analysis</h3>
                <p>Extract and process email content, headers, and metadata</p>
              </div>
            </div>
            <div className="workflow-step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>AI Classification</h3>
                <p>ML model analyzes features and classifies emails as phishing or legitimate</p>
              </div>
            </div>
            <div className="workflow-step">
              <div className="step-number">4</div>
              <div className="step-content">
                <h3>Instant Alerts</h3>
                <p>Immediate notifications for suspicious emails with detailed analysis</p>
              </div>
            </div>
          </div>
        </section>

        <section className="project-info">
          <h2>Final Year Project</h2>
          <p>
            This system was developed as a Final Year Project by computer science students
            specializing in cybersecurity and artificial intelligence. The project demonstrates
            the practical application of machine learning in solving real-world security challenges.
          </p>
          <div className="project-details">
            <div className="detail-item">
              <strong>Project Duration:</strong> 6 Months
            </div>
            <div className="detail-item">
              <strong>Technology Stack:</strong> React, Flask, MongoDB, Scikit-learn
            </div>
            <div className="detail-item">
              <strong>Supervisor:</strong> Dr. Sarah Williams
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default About;