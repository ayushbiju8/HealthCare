import { useState } from 'react';
import { FileText, Plus, Filter, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import './HealthMetrics.css';

export default function HealthMetrics() {
  const [metrics] = useState([
    { id: 1, type: 'Blood Glucose', value: '95', unit: 'mg/dL', status: 'Normal', trend: 'down', date: '2026-05-15' },
    { id: 2, type: 'Blood Pressure', value: '120/80', unit: 'mmHg', status: 'Optimal', trend: 'stable', date: '2026-05-14' },
    { id: 3, type: 'Heart Rate', value: '72', unit: 'bpm', status: 'Normal', trend: 'up', date: '2026-05-13' },
    { id: 4, type: 'Cholesterol', value: '180', unit: 'mg/dL', status: 'Normal', trend: 'down', date: '2026-05-10' },
    { id: 5, type: 'BMI', value: '24.5', unit: '', status: 'Warning', trend: 'up', date: '2026-04-01' }
  ]);

  const renderTrend = (trend) => {
    switch(trend) {
      case 'up': return <TrendingUp size={16} className="text-danger" />;
      case 'down': return <TrendingDown size={16} className="text-success" />;
      default: return <Minus size={16} className="text-muted" />;
    }
  };

  const getStatusBadgeClass = (status) => {
    switch(status) {
      case 'Normal':
      case 'Optimal': return 'badge-success';
      case 'Warning': return 'badge-warning';
      case 'Critical': return 'badge-danger';
      default: return 'badge-primary';
    }
  };

  return (
    <div className="container animate-enter">
      <div className="page-header">
        <div>
          <h1 className="text-gradient">Health Metrics</h1>
          <p>Track your vital signs and key health indicators over time</p>
        </div>
        <div className="flex gap-2">
          <button className="btn btn-secondary">
            <Filter size={18} />
            Filter
          </button>
          <button className="btn btn-primary">
            <Plus size={18} />
            Log Metric
          </button>
        </div>
      </div>

      <div className="glass-card table-card">
        <div className="table-responsive">
          <table className="premium-table">
            <thead>
              <tr>
                <th>Metric Type</th>
                <th>Value</th>
                <th>Status</th>
                <th>Trend</th>
                <th>Date Recorded</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {metrics.map((metric) => (
                <tr key={metric.id}>
                  <td>
                    <div className="flex items-center gap-3">
                      <div className="metric-icon-small bg-gradient-primary">
                        <FileText size={16} className="text-white" />
                      </div>
                      <span className="font-semibold">{metric.type}</span>
                    </div>
                  </td>
                  <td>
                    <span className="font-display font-semibold text-lg">{metric.value}</span>
                    <span className="text-muted text-sm ml-1">{metric.unit}</span>
                  </td>
                  <td>
                    <span className={`badge ${getStatusBadgeClass(metric.status)}`}>
                      {metric.status}
                    </span>
                  </td>
                  <td>
                    <div className="trend-indicator">
                      {renderTrend(metric.trend)}
                    </div>
                  </td>
                  <td className="text-muted">{metric.date}</td>
                  <td>
                    <button className="btn btn-secondary btn-sm">Details</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
