import { Heart, Activity, Thermometer, Droplet, Plus } from 'lucide-react';

export default function HealthProfile() {
  return (
    <div className="container animate-enter">
      <div className="page-header">
        <div>
          <h1 className="text-gradient">Health Information</h1>
          <p>Your medical history and physiological data</p>
        </div>
      </div>

      <div className="grid grid-cols-3 mb-6">
        <div className="glass-card bg-gradient-primary text-white p-6">
          <div className="flex items-center gap-4 mb-2">
            <Droplet size={32} />
            <span className="text-4xl font-display font-bold">O+</span>
          </div>
          <p className="opacity-80">Blood Group</p>
        </div>
        <div className="glass-card bg-gradient-accent text-white p-6">
          <div className="flex items-center gap-4 mb-2">
            <Activity size={32} />
            <span className="text-4xl font-display font-bold">180</span>
          </div>
          <p className="opacity-80">Height (cm)</p>
        </div>
        <div className="glass-card bg-gradient-success text-white p-6">
          <div className="flex items-center gap-4 mb-2">
            <Thermometer size={32} />
            <span className="text-4xl font-display font-bold">75</span>
          </div>
          <p className="opacity-80">Weight (kg)</p>
        </div>
      </div>

      <div className="grid grid-cols-2">
        <div className="glass-card">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl">Allergies</h3>
            <button className="btn btn-secondary btn-sm"><Plus size={16}/></button>
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="badge badge-danger">Penicillin</span>
            <span className="badge badge-danger">Peanuts</span>
            <span className="badge badge-warning">Dust Mites</span>
          </div>
        </div>
        
        <div className="glass-card">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl">Chronic Conditions</h3>
            <button className="btn btn-secondary btn-sm"><Plus size={16}/></button>
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="badge badge-primary">Mild Asthma</span>
            <span className="badge badge-primary">Seasonal Allergies</span>
          </div>
        </div>
      </div>
    </div>
  );
}
