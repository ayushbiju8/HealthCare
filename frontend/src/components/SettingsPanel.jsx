import { SlidersHorizontal } from 'lucide-react';
import { useState } from 'react';
import './SettingsPanel.css';

export default function SettingsPanel({ density, setDensity, accent, setAccent, motion, setMotion }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="settings-panel">
      <button
        className="settings-trigger"
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-label="Open settings"
      >
        <SlidersHorizontal size={18} />
      </button>

      {isOpen && (
        <div className="settings-card">
          <div className="settings-header">
            <h3>Quick Settings</h3>
            <p>Customize the interface</p>
          </div>

          <div className="settings-section">
            <label htmlFor="density-select">Layout density</label>
            <select
              id="density-select"
              value={density}
              onChange={(event) => setDensity(event.target.value)}
            >
              <option value="comfortable">Comfortable</option>
              <option value="compact">Compact</option>
            </select>
          </div>

          <div className="settings-section">
            <label htmlFor="accent-select">Accent color</label>
            <select
              id="accent-select"
              value={accent}
              onChange={(event) => setAccent(event.target.value)}
            >
              <option value="blue">Blue</option>
              <option value="teal">Teal</option>
              <option value="violet">Violet</option>
              <option value="rose">Rose</option>
              <option value="amber">Amber</option>
            </select>
          </div>

          <div className="settings-section settings-toggle">
            <div>
              <h4>Reduce motion</h4>
              <p>Minimize animations</p>
            </div>
            <button
              type="button"
              className={`toggle-pill ${motion === 'reduced' ? 'active' : ''}`}
              onClick={() => setMotion(motion === 'reduced' ? 'full' : 'reduced')}
              aria-pressed={motion === 'reduced'}
            >
              <span className="toggle-knob" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
