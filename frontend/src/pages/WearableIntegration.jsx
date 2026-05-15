import { useState } from 'react';
import { Watch, Smartphone, Activity, CheckCircle, RefreshCw, Plus } from 'lucide-react';
import './WearableIntegration.css';

export default function WearableIntegration() {
  const [syncingId, setSyncingId] = useState(null);

  const devices = [
    {
      id: 1,
      name: 'Apple Watch Series 9',
      type: 'Smartwatch',
      status: 'Connected',
      lastSync: 'Just now',
      battery: '85%',
      icon: Watch,
      color: 'primary'
    },
    {
      id: 2,
      name: 'Oura Ring Gen3',
      type: 'Smart Ring',
      status: 'Connected',
      lastSync: '2 hours ago',
      battery: '42%',
      icon: Activity,
      color: 'accent'
    }
  ];

  const handleSync = (id) => {
    setSyncingId(id);
    setTimeout(() => {
      setSyncingId(null);
    }, 2000);
  };

  return (
    <div className="container animate-enter">
      <div className="page-header">
        <div>
          <h1 className="text-gradient">Wearables & Integrations</h1>
          <p>Manage your connected health devices and sync data</p>
        </div>
        <button className="btn btn-primary">
          <Plus size={18} />
          Add Device
        </button>
      </div>

      <div className="grid grid-cols-2">
        {devices.map((device) => {
          const Icon = device.icon;
          const isSyncing = syncingId === device.id;
          
          return (
            <div key={device.id} className="glass-card device-card">
              <div className="device-header">
                <div className={`device-icon-wrapper bg-gradient-${device.color}`}>
                  <Icon size={28} className="text-white" />
                  {isSyncing && (
                    <div className="sync-pulse-ring"></div>
                  )}
                </div>
                <div className="device-status">
                  <span className="badge badge-success">
                    <CheckCircle size={12} className="mr-1 inline" />
                    {device.status}
                  </span>
                </div>
              </div>
              
              <div className="device-info mt-4">
                <h2>{device.name}</h2>
                <p className="text-muted">{device.type}</p>
              </div>
              
              <div className="device-stats mt-4 flex-between">
                <div>
                  <p className="text-muted text-sm">Battery</p>
                  <p className="font-semibold">{device.battery}</p>
                </div>
                <div>
                  <p className="text-muted text-sm">Last Sync</p>
                  <p className="font-semibold">{device.lastSync}</p>
                </div>
              </div>
              
              <div className="device-actions mt-4 pt-4 border-t">
                <button 
                  className={`btn w-full ${isSyncing ? 'btn-secondary' : 'btn-primary'}`}
                  onClick={() => handleSync(device.id)}
                  disabled={isSyncing}
                >
                  <RefreshCw size={18} className={isSyncing ? 'spin-fast' : ''} />
                  {isSyncing ? 'Syncing Data...' : 'Sync Now'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
