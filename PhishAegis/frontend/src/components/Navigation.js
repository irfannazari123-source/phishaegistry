import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

const Navigation = ({ user, onLogout }) => {
  const location = useLocation();

  return (
    <nav className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <i className="fas fa-shield-alt"></i>
          <span>PhishGuard AI</span>
        </div>
      </div>

      <div className="user-info">
        <img src={user.picture || '/images/default-avatar.png'} alt={user.name} className="user-avatar" />
        <div className="user-details">
          <h4>{user.name}</h4>
          <p>{user.email}</p>
        </div>
      </div>

      <ul className="sidebar-nav">
        <li className={location.pathname === '/dashboard' ? 'active' : ''}>
          <Link to="/dashboard">
            <i className="fas fa-tachometer-alt"></i>
            <span>Dashboard</span>
          </Link>
        </li>
        <li className={location.pathname === '/alerts' ? 'active' : ''}>
          <Link to="/alerts">
            <i className="fas fa-bell"></i>
            <span>Alerts</span>
            <span className="badge">3</span>
          </Link>
        </li>
        <li className={location.pathname === '/statistics' ? 'active' : ''}>
          <Link to="/statistics">
            <i className="fas fa-chart-bar"></i>
            <span>Statistics</span>
          </Link>
        </li>
        <li className={location.pathname === '/team' ? 'active' : ''}>
          <Link to="/team">
            <i className="fas fa-users"></i>
            <span>Our Team</span>
          </Link>
        </li>
        <li className={location.pathname === '/about' ? 'active' : ''}>
          <Link to="/about">
            <i className="fas fa-info-circle"></i>
            <span>About</span>
          </Link>
        </li>
      </ul>

      <div className="sidebar-footer">
        <button onClick={onLogout} className="logout-btn">
          <i className="fas fa-sign-out-alt"></i>
          <span>Logout</span>
        </button>
      </div>
    </nav>
  );
};

export default Navigation;