import { Link } from 'react-router-dom';
import { Heart, Users, Activity, FileText, Bell, Zap, TrendingUp, ShieldCheck } from 'lucide-react';
import './Dashboard.css';

export default function Dashboard() {
  const isLoading = false;
  const stats = [
    {
      title: 'Health Score',
      value: '92',
      desc: 'Top 15% for your age',
      icon: ShieldCheck,
      bgClass: 'bg-gradient-primary',
      link: '/profile'
    },
    {
      title: 'Fitness Trends',
      value: '8.5K',
      desc: 'Steps today (Active)',
      icon: Activity,
      bgClass: 'bg-gradient-accent',
      link: '/fitness'
    },
    {
      title: 'Medical Documents',
      value: '12',
      desc: '2 Recent OCR Scans',
      icon: FileText,
      bgClass: 'glass-card',
      link: '/reports'
    },
    {
      title: 'Health Reminders',
      value: '3',
      desc: 'Upcoming today',
      icon: Bell,
      bgClass: 'glass-card',
      link: '/reminders'
    },
  ];

  const recentMetrics = [
    { type: 'Blood Glucose', value: '95', unit: 'mg/dL', status: 'Normal' },
    { type: 'Blood Pressure', value: '120/80', unit: 'mmHg', status: 'Normal' },
    { type: 'Heart Rate', value: '72', unit: 'bpm', status: 'Optimal' },
  ];

  return (
    <div className="container animate-enter">
      <div className="page-header">
        <div>
          <h1>Welcome back, <span className="text-gradient">Alex</span></h1>
          <p>Here is your daily health intelligence overview.</p>
        </div>
      </div>

      <div className="grid grid-cols-4 mb-4">
        {stats.map((stat, idx) => {
          const Icon = stat.icon;
          const isGradient = stat.bgClass.includes('bg-gradient');
          return (
            <Link key={idx} to={stat.link} className={`stat-card ${stat.bgClass}`}>
              <div className="stat-header">
                <h3 className={isGradient ? 'text-white' : 'text-muted'}>{stat.title}</h3>
                <div className={`stat-icon-wrapper ${isGradient ? 'icon-light' : 'icon-gradient'}`}>
                  <Icon size={20} />
                </div>
              </div>
              <div className="stat-content">
                <div className="stat-value">{stat.value}</div>
                <div className="stat-desc">
                  {isGradient && <TrendingUp size={14} className="mr-1 inline" />}
                  {stat.desc}
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      <div className="grid grid-cols-3">
        <div className="col-span-2">
          <div className="glass-card full-height">
            <div className="flex-between mb-3">
              <h2>Health Intelligence Metrics</h2>
              <Link to="/metrics" className="btn btn-secondary btn-sm">View All</Link>
            </div>
            
            <div className="metrics-list">
              {recentMetrics.map((metric, idx) => (
                <div key={idx} className="metric-row">
                  <div className="metric-info">
                    <div className="metric-icon-bg">
                      <Heart size={18} className="text-primary" />
                    </div>
                    <div>
                      <h4>{metric.type}</h4>
                      <p className="text-muted text-sm">Last updated 2h ago</p>
                    </div>
                  </div>
                  <div className="metric-value-container">
                    <div className="metric-value">
                      {metric.value} <span>{metric.unit}</span>
                    </div>
                    <span className="badge badge-success">{metric.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="col-span-1">
          <div className="glass-card full-height">
            <h2>Quick AI Actions</h2>
            <p className="text-muted text-sm mb-3">Powered by Assistant AI</p>
            
            <div className="quick-actions-list">
              <Link to="/assistant" className="action-card">
                <div className="action-icon">
                  <Zap size={20} className="text-accent" />
                </div>
                <div className="action-text">
                  <h4>Symptom Checker</h4>
                  <p>Describe what you're feeling</p>
                </div>
              </Link>
              
              <Link to="/reports" className="action-card">
                <div className="action-icon">
                  <FileText size={20} className="text-primary" />
                </div>
                <div className="action-text">
                  <h4>OCR Report Scan</h4>
                  <p>Extract data from lab results</p>
                </div>
              </Link>

              <Link to="/wearables" className="action-card">
                <div className="action-icon">
                  <Activity size={20} className="text-success" />
                </div>
                <div className="action-text">
                  <h4>Sync Wearables</h4>
                  <p>Update your fitness band data</p>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
