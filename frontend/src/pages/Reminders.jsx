import { Bell, Plus, Clock, Pill, Calendar, CalendarCheck } from 'lucide-react';
import './Reminders.css';

export default function Reminders() {
  const reminders = [
    { id: 1, title: 'Take Vitamin D', time: '08:00 AM', type: 'Medication', icon: Pill, color: 'primary' },
    { id: 2, title: 'Annual Checkup', time: 'Tomorrow, 10:00 AM', type: 'Appointment', icon: Calendar, color: 'accent' },
    { id: 3, title: 'Drink Water', time: 'Every 2 hours', type: 'Routine', icon: Clock, color: 'success' },
    { id: 4, title: 'Renew Prescription', time: 'Next Week', type: 'Pharmacy', icon: CalendarCheck, color: 'warning' }
  ];

  return (
    <div className="container animate-enter">
      <div className="page-header">
        <div>
          <h1 className="text-gradient">Health Reminders</h1>
          <p>Never miss a medication or appointment</p>
        </div>
        <button className="btn btn-primary">
          <Plus size={18} />
          Add Reminder
        </button>
      </div>

      <div className="grid grid-cols-2">
        {reminders.map((reminder) => {
          const Icon = reminder.icon;
          return (
            <div key={reminder.id} className="glass-card reminder-card">
              <div className="reminder-icon-bg bg-gradient-primary">
                <Icon size={24} className="text-white" />
              </div>
              <div className="reminder-content">
                <h3>{reminder.title}</h3>
                <div className="reminder-meta">
                  <span className={`badge badge-${reminder.color} mr-2`}>{reminder.type}</span>
                  <span className="text-muted flex items-center gap-1 text-sm">
                    <Clock size={14} />
                    {reminder.time}
                  </span>
                </div>
              </div>
              <div className="toggle-switch">
                <input type="checkbox" id={`toggle-${reminder.id}`} defaultChecked />
                <label htmlFor={`toggle-${reminder.id}`}></label>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
