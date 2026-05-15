import { Activity, Flame, Moon, Footprints } from 'lucide-react';
import './FitnessSummary.css';

export default function FitnessSummary() {
  const metrics = [
    { name: 'Steps', value: '8,542', goal: '10,000', icon: Footprints, color: 'primary', percent: 85 },
    { name: 'Calories', value: '1,840', goal: '2,200', icon: Flame, color: 'danger', percent: 83 },
    { name: 'Active Min', value: '45', goal: '30', icon: Activity, color: 'success', percent: 150 },
    { name: 'Sleep', value: '7h 15m', goal: '8h', icon: Moon, color: 'accent', percent: 90 },
  ];

  return (
    <div className="container animate-enter">
      <div className="page-header">
        <div>
          <h1 className="text-gradient">Fitness Summary</h1>
          <p>Track your daily activity and sleep metrics</p>
        </div>
      </div>

      <div className="grid grid-cols-2">
        <div className="glass-card flex items-center justify-center col-span-2 md-col-span-1 min-h-300">
          <div className="activity-rings">
            <svg viewBox="0 0 100 100" className="circular-chart primary">
              <path className="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path className="circle" strokeDasharray="85, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            </svg>
            <svg viewBox="0 0 100 100" className="circular-chart danger" style={{ width: '80%', position: 'absolute' }}>
              <path className="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path className="circle" strokeDasharray="83, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            </svg>
            <svg viewBox="0 0 100 100" className="circular-chart success" style={{ width: '60%', position: 'absolute' }}>
              <path className="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path className="circle" strokeDasharray="100, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            </svg>
            <div className="activity-center">
              <Activity size={32} className="text-primary pulse" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 col-span-2 md-col-span-1">
          {metrics.map((metric, idx) => {
            const Icon = metric.icon;
            return (
              <div key={idx} className={`glass-card metric-square bg-gradient-${metric.color}`}>
                <div className="metric-square-header">
                  <Icon size={24} className="text-white opacity-80" />
                  <span className="text-white opacity-80 text-sm font-semibold">{metric.name}</span>
                </div>
                <div className="metric-square-value text-white">{metric.value}</div>
                <div className="progress-mini">
                  <div className="progress-mini-fill bg-white" style={{ width: `${Math.min(metric.percent, 100)}%` }}></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
