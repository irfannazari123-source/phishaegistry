import React from 'react';
import './Login.css';

const Login = ({ onLogin }) => {
  const handleDemoLogin = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/auth/demo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      const data = await response.json();
      onLogin(data.user, data.access_token);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-section">
          <div className="logo">
            <i className="fas fa-shield-alt"></i>
            <h1>PhishGuard AI</h1>
          </div>
          <p>AI-Powered Phishing Email Detection System</p>
        </div>

        <div className="login-content">
          <h2>Welcome to PhishGuard AI</h2>
          <p>Demo Version - FYP Project</p>

          <button className="demo-login-btn" onClick={handleDemoLogin}>
            <i className="fas fa-play-circle"></i>
            Start Demo
          </button>

          <div className="demo-info">
            <h3>Demo Features:</h3>
            <ul>
              <li>Real-time email monitoring simulation</li>
              <li>AI-powered phishing detection</li>
              <li>Professional dashboard</li>
              <li>Team information</li>
              <li>Project details</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;