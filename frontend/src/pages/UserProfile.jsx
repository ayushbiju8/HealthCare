import { User, Mail, Phone, MapPin, Edit3, Shield } from 'lucide-react';

export default function UserProfile() {
  return (
    <div className="container animate-enter">
      <div className="page-header">
        <div>
          <h1 className="text-gradient">User Profile</h1>
          <p>Manage your account settings and personal information</p>
        </div>
        <button className="btn btn-primary">
          <Edit3 size={18} />
          Edit Profile
        </button>
      </div>

      <div className="grid grid-cols-3">
        <div className="col-span-1">
          <div className="glass-card flex flex-col items-center p-6 text-center">
            <div className="w-32 h-32 rounded-full bg-gradient-primary flex items-center justify-center mb-4 text-white font-display text-4xl shadow-glow">
              A
            </div>
            <h2 className="text-2xl mb-1">Alex Carter</h2>
            <p className="text-muted mb-4">alex.carter@example.com</p>
            <div className="badge badge-success mb-6">
              <Shield size={14} className="mr-1 inline" />
              Verified Account
            </div>
          </div>
        </div>

        <div className="col-span-2">
          <div className="glass-card">
            <h3 className="text-xl mb-6 pb-2 border-b border-solid">Personal Information</h3>
            
            <div className="grid grid-cols-2 gap-6">
              <div className="form-group">
                <label>First Name</label>
                <div className="form-control flex items-center gap-2">
                  <User size={18} className="text-muted" />
                  <span>Alex</span>
                </div>
              </div>
              <div className="form-group">
                <label>Last Name</label>
                <div className="form-control flex items-center gap-2">
                  <User size={18} className="text-muted" />
                  <span>Carter</span>
                </div>
              </div>
              <div className="form-group">
                <label>Email Address</label>
                <div className="form-control flex items-center gap-2">
                  <Mail size={18} className="text-muted" />
                  <span>alex.carter@example.com</span>
                </div>
              </div>
              <div className="form-group">
                <label>Phone Number</label>
                <div className="form-control flex items-center gap-2">
                  <Phone size={18} className="text-muted" />
                  <span>+1 (555) 123-4567</span>
                </div>
              </div>
              <div className="form-group col-span-2">
                <label>Address</label>
                <div className="form-control flex items-center gap-2">
                  <MapPin size={18} className="text-muted" />
                  <span>123 Health Ave, Wellness City, CA 90210</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
