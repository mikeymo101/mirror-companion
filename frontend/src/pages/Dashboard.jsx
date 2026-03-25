import { Link } from 'react-router-dom';
import './Dashboard.css';

export default function Dashboard() {
  return (
    <div className="dashboard">
      <div className="dashboard__card">
        <h1 className="dashboard__title">Parent Dashboard</h1>
        <div className="dashboard__divider" />
        <p className="dashboard__message">Coming in Phase 4</p>
        <p className="dashboard__sub">
          The parent dashboard will let you manage your child's profile,
          view conversation logs, configure chores and routines, and
          customize the mirror companion -- all from your phone.
        </p>
        <div className="dashboard__features">
          <div className="dashboard__feature">
            <span className="dashboard__feature-icon">&#128100;</span>
            <span>Child Profile</span>
          </div>
          <div className="dashboard__feature">
            <span className="dashboard__feature-icon">&#128172;</span>
            <span>Conversation Logs</span>
          </div>
          <div className="dashboard__feature">
            <span className="dashboard__feature-icon">&#9881;</span>
            <span>Settings</span>
          </div>
          <div className="dashboard__feature">
            <span className="dashboard__feature-icon">&#9989;</span>
            <span>Chore Tracking</span>
          </div>
        </div>
        <Link to="/" className="dashboard__link">
          &#8592; Back to Mirror
        </Link>
      </div>
    </div>
  );
}
