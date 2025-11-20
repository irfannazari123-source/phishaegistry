import React, { useState, useEffect } from 'react';
import './Alerts.css';

const Alerts = ({ user }) => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    // Mock data for demonstration
    const mockAlerts = [
      {
        _id: '1',
        subject: 'Urgent: Verify Your Bank Account',
        probability: 0.95,
        triggered_at: new Date('2023-12-01T10:30:00'),
        is_read: false
      },
      {
        _id: '2',
        subject: 'Your Subscription Has Expired',
        probability: 0.87,
        triggered_at: new Date('2023-12-01T09:15:00'),
        is_read: false
      },
      {
        _id: '3',
        subject: 'Password Reset Required',
        probability: 0.78,
        triggered_at: new Date('2023-11-30T16:45:00'),
        is_read: true
      }
    ];
    setAlerts(mockAlerts);
  }, []);

  return (
    <div className="alerts-page">
      <div className="alerts-header">
        <h1>Security Alerts</h1>
        <p>Recent phishing detection alerts and notifications</p>
      </div>

      <div className="alerts-container">
        {alerts.map(alert => (
          <div key={alert._id} className={`alert-item ${alert.is_read ? 'read' : 'unread'}`}>
            <div className="alert-icon">
              <i className="fas fa-exclamation-triangle"></i>
            </div>
            <div className="alert-content">
              <h3>{alert.subject}</h3>
              <div className="alert-meta">
                <span className="probability">
                  Threat Level: {(alert.probability * 100).toFixed(1)}%
                </span>
                <span className="time">
                  {new Date(alert.triggered_at).toLocaleString()}
                </span>
              </div>
            </div>
            <div className="alert-actions">
              <button className="btn-view">View Details</button>
              <button className="btn-dismiss">Dismiss</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Alerts;