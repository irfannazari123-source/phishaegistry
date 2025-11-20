import React from 'react';
import './Team.css';

const Team = () => {
  const teamMembers = [
    {
      name: "John Doe",
      role: "Project Lead & Full Stack Developer",
      image: "/images/john-doe.jpg",
      description: "Expert in cybersecurity with 5+ years of experience in full-stack development and system architecture. Specializes in React, Python, and cloud technologies.",
      email: "john.doe@phishguard.ai",
      skills: ["React", "Python", "Cybersecurity", "Docker"]
    },
    {
      name: "Jane Smith",
      role: "AI/ML Specialist",
      image: "/images/jane-smith.jpg",
      description: "Master's in Machine Learning with focus on NLP and email security applications. Developed the core phishing detection algorithm.",
      email: "jane.smith@phishguard.ai",
      skills: ["Machine Learning", "NLP", "Python", "Data Science"]
    },
    {
      name: "Mike Johnson",
      role: "Backend Developer",
      image: "/images/mike-johnson.jpg",
      description: "Specializes in real-time systems, API development, and database management. Built the scalable backend infrastructure.",
      email: "mike.johnson@phishguard.ai",
      skills: ["Node.js", "MongoDB", "API Design", "System Architecture"]
    },
    {
      name: "Dr. Sarah Williams",
      role: "Project Supervisor",
      image: "/images/sarah-williams.jpg",
      description: "Professor of Computer Science with 15+ years of experience in cybersecurity research and education. Provided academic guidance and industry insights.",
      email: "sarah.williams@phishguard.ai",
      skills: ["Cybersecurity", "Research", "Mentoring", "Academic Leadership"]
    }
  ];

  return (
    <div className="team-page">
      <div className="team-header">
        <h1>Our Team</h1>
        <p>Meet the talented individuals behind PhishGuard AI</p>
      </div>

      <div className="team-grid">
        {teamMembers.map((member, index) => (
          <div key={index} className="team-card">
            <div className="member-image">
              <img
                src={member.image}
                alt={member.name}
                onError={(e) => {
                  e.target.src = `https://via.placeholder.com/200x200/1a73e8/ffffff?text=${member.name.split(' ').map(n => n[0]).join('')}`;
                }}
              />
              <div className="member-overlay">
                <div className="social-links">
                  <a href={`mailto:${member.email}`} className="social-link">
                    <i className="fas fa-envelope"></i>
                  </a>
                  <a href="#" className="social-link">
                    <i className="fab fa-linkedin"></i>
                  </a>
                  <a href="#" className="social-link">
                    <i className="fab fa-github"></i>
                  </a>
                </div>
              </div>
            </div>
            <div className="member-info">
              <h3>{member.name}</h3>
              <p className="role">{member.role}</p>
              <p className="description">{member.description}</p>

              <div className="skills">
                {member.skills.map((skill, skillIndex) => (
                  <span key={skillIndex} className="skill-tag">{skill}</span>
                ))}
              </div>

              <a href={`mailto:${member.email}`} className="contact-link">
                <i className="fas fa-envelope"></i>
                Contact {member.name.split(' ')[0]}
              </a>
            </div>
          </div>
        ))}
      </div>

      <div className="team-stats">
        <div className="stat-item">
          <h3>4+</h3>
          <p>Team Members</p>
        </div>
        <div className="stat-item">
          <h3>6</h3>
          <p>Months of Development</p>
        </div>
        <div className="stat-item">
          <h3>98.7%</h3>
          <p>Detection Accuracy</p>
        </div>
        <div className="stat-item">
          <h3>1000+</h3>
          <p>Emails Analyzed</p>
        </div>
      </div>
    </div>
  );
};

export default Team;