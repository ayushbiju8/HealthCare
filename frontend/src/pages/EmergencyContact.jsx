import { PhoneCall, MapPin, AlertTriangle, Plus, Trash2 } from 'lucide-react';

export default function EmergencyContact() {
  const contacts = [
    { id: 1, name: 'Sarah Carter', relation: 'Spouse', phone: '+1 (555) 987-6543', isPrimary: true },
    { id: 2, name: 'Dr. Emily Chen', relation: 'Primary Care Physician', phone: '+1 (555) 456-7890', isPrimary: false }
  ];

  return (
    <div className="container animate-enter">
      <div className="page-header">
        <div>
          <h1 className="text-gradient">Emergency Contacts</h1>
          <p>People to contact in case of a medical emergency</p>
        </div>
        <button className="btn btn-primary">
          <Plus size={18} />
          Add Contact
        </button>
      </div>

      <div className="grid grid-cols-2">
        {contacts.map((contact) => (
          <div key={contact.id} className="glass-card flex justify-between items-center relative overflow-hidden">
            {contact.isPrimary && (
              <div className="absolute top-0 right-0 bg-danger text-white text-xs px-3 py-1 rounded-bl-lg font-bold">
                PRIMARY
              </div>
            )}
            <div className="flex gap-4 items-center">
              <div className={`w-14 h-14 rounded-full flex items-center justify-center text-white ${contact.isPrimary ? 'bg-gradient-danger' : 'bg-gradient-primary'}`}>
                <span className="font-display text-xl font-bold">{contact.name.charAt(0)}</span>
              </div>
              <div>
                <h3 className="text-lg font-semibold">{contact.name}</h3>
                <p className="text-sm text-muted mb-2">{contact.relation}</p>
                <div className="flex items-center gap-2 text-sm">
                  <PhoneCall size={14} className="text-accent" />
                  <span>{contact.phone}</span>
                </div>
              </div>
            </div>
            <div>
              <button className="btn btn-secondary text-danger">
                <Trash2 size={18} />
              </button>
            </div>
          </div>
        ))}
        
        <div className="glass-card flex flex-col items-center justify-center p-8 border-dashed border-2 cursor-pointer hover:border-primary transition-colors">
          <Plus size={32} className="text-muted mb-2" />
          <h3 className="text-lg text-muted">Add New Contact</h3>
        </div>
      </div>
      
      <div className="mt-8 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl flex items-start gap-4">
        <AlertTriangle size={24} className="text-danger flex-shrink-0 mt-1" />
        <div>
          <h4 className="text-danger font-semibold mb-1">Emergency Protocol</h4>
          <p className="text-sm text-muted">In case of a severe medical emergency, call 911 immediately. Your primary contact will be automatically notified if you trigger the SOS function on your connected wearable device.</p>
        </div>
      </div>
    </div>
  );
}
