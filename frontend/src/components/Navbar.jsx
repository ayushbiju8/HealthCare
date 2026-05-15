import { Link, useLocation } from 'react-router-dom';
import {
  Menu,
  X,
  Home,
  User,
  Heart,
  Activity,
  Bell,
  FileText,
  Moon,
  Sun,
  MessageSquare
} from 'lucide-react';
import { useState } from 'react';
import './Navbar.css';

export default function Navbar({ theme, onToggleTheme }) {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/profile', icon: User, label: 'Profile' },
    { path: '/health-profile', icon: Heart, label: 'Health Info' },
    { path: '/fitness', icon: Activity, label: 'Fitness' },
    { path: '/metrics', icon: FileText, label: 'Metrics' },
    { path: '/reminders', icon: Bell, label: 'Reminders' },
    { path: '/assistant', icon: MessageSquare, label: 'AI Assistant' }
  ];

  return (
    <>
      <button
        className="mobile-menu-btn"
        onClick={() => setIsOpen(!isOpen)}
        type="button"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      <nav className={`sidebar ${isOpen ? 'active' : ''}`}>
        <div className="sidebar-header">
          <Link to="/" className="sidebar-brand">
            <div className="brand-icon">
              <Heart size={24} color="white" />
            </div>
            <span>HealthPlus</span>
          </Link>
        </div>

        <ul className="nav-links">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <li key={item.path}>
                <Link to={item.path} className={isActive ? 'active' : ''}>
                  <Icon size={20} className={isActive ? 'icon-active' : ''} />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>

        <div className="sidebar-footer">
          <button
            className="theme-toggle"
            type="button"
            onClick={onToggleTheme}
            aria-label="Toggle color theme"
          >
            {theme === 'dark' ? (
              <>
                <Sun size={20} />
                <span>Light Mode</span>
              </>
            ) : (
              <>
                <Moon size={20} />
                <span>Dark Mode</span>
              </>
            )}
          </button>
        </div>
      </nav>
    </>
  );
}
