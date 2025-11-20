import React from 'react';
import './Statistics.css';

const Statistics = ({ user }) => {
  // Mock statistics data
  const statsData = {
    totalScanned: 1247,
    phishingDetected: 24,
    falsePositives: 2,
    detectionAccuracy: 98.7,
    avgResponseTime: 0.2,
    topThreats: [
      { type: 'Financial Phishing', count: 12 },
      { type: 'Account Verification', count: 8 },
      { type: 'Social Engineering', count: 4 }
    ],
    dailyStats: [
      { date: '2023-11-27', scanned: 156, threats: 3 },
      { date: '2023-11-28', scanned: 142, threats: 2 },
      { date: '2023-11-29', scanned: 178, threats: 5 },
      { date: '2023-11-30', scanned: 165, threats: 4 },
      { date: '2023-12-01', scanned: 89, threats: 2 }
    ]
  };

  return (
    <div className="statistics-page">
      <div className="stats-header">
        <h1>Analytics & Statistics</h1>
        <p>Comprehensive overview of email security performance</p>
      </div>

      <div className="stats-overview">
        <div className="stat-card large">
          <h3>Detection Performance</h3>
          <div className="performance-metric">
            <div className="metric-value">{statsData.detectionAccuracy}%</div>
            <div className="metric-label">Accuracy Rate</div>
          </div>
        </div>

        <div className="stat-card">
          <h3>Total Emails Scanned</h3>
          <div className="metric-value">{statsData.totalScanned}</div>
        </div>

        <div className="stat-card">
          <h3>Phishing Detected</h3>
          <div className="metric-value">{statsData.phishingDetected}</div>
        </div>

        <div className="stat-card">
          <h3>False Positives</h3>
          <div className="metric-value">{statsData.falsePositives}</div>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-card">
          <h3>Threat Distribution</h3>
          <div className="threats-list">
            {statsData.topThreats.map((threat, index) => (
              <div key={index} className="threat-item">
                <span className="threat-type">{threat.type}</span>
                <span className="threat-count">{threat.count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="chart-card">
          <h3>Daily Activity</h3>
          <div className="daily-stats">
            {statsData.dailyStats.map((day, index) => (
              <div key={index} className="day-stat">
                <div className="day-label">
                  {new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' })}
                </div>
                <div className="day-bars">
                  <div
                    className="bar scanned"
                    style={{ height: `${(day.scanned / 200) * 100}%` }}
                    title={`Scanned: ${day.scanned}`}
                  ></div>
                  <div
                    className="bar threats"
                    style={{ height: `${(day.threats / 10) * 100}%` }}
                    title={`Threats: ${day.threats}`}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Statistics;