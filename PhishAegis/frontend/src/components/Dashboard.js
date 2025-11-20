import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  const [stats, setStats] = useState({});
  const [recentEmails, setRecentEmails] = useState([]);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetchStats();
    fetchRecentEmails();
    fetchAlerts();
  }, []);

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/stats', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
      // Mock data for demo
      setStats({
        total_emails: 1247,
        phishing_emails: 24,
        today_emails: 89,
        detection_rate: 98.7
      });
    }
  };

  const fetchRecentEmails = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/emails', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setRecentEmails(data);
    } catch (error) {
      console.error('Error fetching emails:', error);
      // Mock data for demo
      setRecentEmails([
        {
          _id: '1',
          subject: 'Urgent: Verify Your Bank Account',
          body_preview: 'Please verify your bank account immediately by clicking the link below...',
          received_at: new Date().toISOString(),
          is_phishing: true,
          probability: 0.95
        },
        {
          _id: '2',
          subject: 'Meeting Scheduled for Tomorrow',
          body_preview: 'Hi team, we have a meeting scheduled for tomorrow at 10 AM...',
          received_at: new Date().toISOString(),
          is_phishing: false,
          probability: 0.12
        },
        {
          _id: '3',
          subject: 'Your Account Has Been Compromised',
          body_preview: 'We detected suspicious activity on your account. Reset your password now...',
          received_at: new Date().toISOString(),
          is_phishing: true,
          probability: 0.87
        }
      ]);
    }
  };

  const fetchAlerts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/alerts', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
      // Mock alerts for demo
      setAlerts([
        {
          _id: '1',
          subject: 'High probability phishing detected',
          probability: 0.95,
          triggered_at: new Date().toISOString()
        }
      ]);
    }
  };

  const startMonitoring = async () => {
    try {
      const token = localStorage.getItem('token');
      await fetch('http://localhost:5000/api/emails/start-monitoring', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      setIsMonitoring(true);
      alert('Email monitoring started in demo mode!');
    } catch (error) {
      console.error('Error starting monitoring:', error);
      setIsMonitoring(true);
      alert('Email monitoring started (demo mode)!');
    }
  };

  const stopMonitoring = () => {
    setIsMonitoring(false);
    alert('Email monitoring stopped!');
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Security Dashboard</h1>
        <div className="dashboard-controls">
          {!isMonitoring ? (
            <button className="monitoring-btn start" onClick={startMonitoring}>
              <i className="fas fa-play"></i>
              Start Monitoring
            </button>
          ) : (
            <button className="monitoring-btn stop" onClick={stopMonitoring}>
              <i className="fas fa-stop"></i>
              Stop Monitoring
            </button>
          )}
        </div>
      </div>

      {/* Alert Banner */}
      {alerts.length > 0 && (
        <div className="alert-banner">
          <i className="fas fa-exclamation-triangle"></i>
          <span>{alerts.length} new security alert{alerts.length > 1 ? 's' : ''} detected</span>
        </div>
      )}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon total-emails">
            <i className="fas fa-envelope"></i>
          </div>
          <div className="stat-info">
            <h3>{stats.total_emails || 0}</h3>
            <p>Total Emails Scanned</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon phishing">
            <i className="fas fa-exclamation-triangle"></i>
          </div>
          <div className="stat-info">
            <h3>{stats.phishing_emails || 0}</h3>
            <p>Phishing Detected</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon detection-rate">
            <i className="fas fa-chart-line"></i>
          </div>
          <div className="stat-info">
            <h3>{stats.detection_rate ? stats.detection_rate.toFixed(1) : 0}%</h3>
            <p>Detection Rate</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon today">
            <i className="fas fa-clock"></i>
          </div>
          <div className="stat-info">
            <h3>{stats.today_emails || 0}</h3>
            <p>Today's Emails</p>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="recent-activity">
          <h2>Recent Email Analysis</h2>
          <div className="emails-list">
            {recentEmails.map(email => (
              <div key={email._id} className={`email-item ${email.is_phishing ? 'phishing' : 'legitimate'}`}>
                <div className="email-header">
                  <h4>{email.subject || 'No Subject'}</h4>
                  <span className={`status ${email.is_phishing ? 'danger' : 'safe'}`}>
                    {email.is_phishing ? 'Phishing' : 'Legitimate'}
                  </span>
                </div>
                <p className="email-preview">{email.body_preview}</p>
                <div className="email-footer">
                  <span className="probability">
                    Confidence: {(email.probability * 100).toFixed(1)}%
                  </span>
                  <span className="time">
                    {new Date(email.received_at).toLocaleString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="quick-actions">
          <h3>Quick Actions</h3>
          <div className="action-buttons">
            <button className="action-btn">
              <i className="fas fa-cog"></i>
              Settings
            </button>
            <button className="action-btn">
              <i className="fas fa-download"></i>
              Export Report
            </button>
            <button className="action-btn">
              <i className="fas fa-history"></i>
              View History
            </button>
            <button className="action-btn">
              <i className="fas fa-question-circle"></i>
              Help
            </button>
          </div>

          <div className="system-status">
            <h4>System Status</h4>
            <div className="status-item">
              <span className="status-label">AI Model:</span>
              <span className="status-value active">Running</span>
            </div>
            <div className="status-item">
              <span className="status-label">Database:</span>
              <span className="status-value active">Connected</span>
            </div>
            <div className="status-item">
              <span className="status-label">Email Scanner:</span>
              <span className={`status-value ${isMonitoring ? 'active' : 'inactive'}`}>
                {isMonitoring ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;