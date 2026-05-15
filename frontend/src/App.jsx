import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import SettingsPanel from './components/SettingsPanel';
import Dashboard from './pages/Dashboard';
import UserProfile from './pages/UserProfile';
import HealthProfile from './pages/HealthProfile';
import EmergencyContact from './pages/EmergencyContact';
import FitnessSummary from './pages/FitnessSummary';
import WearableIntegration from './pages/WearableIntegration';
import HealthMetrics from './pages/HealthMetrics';
import MedicalReports from './pages/MedicalReports';
import Reminders from './pages/Reminders';
import AIAssistant from './pages/AIAssistant';
import './App.css';

function App() {
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem('theme');
    if (stored) {
      return stored;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  });

  const [density, setDensity] = useState(() => {
    return localStorage.getItem('density') || 'comfortable';
  });

  const [accent, setAccent] = useState(() => {
    return localStorage.getItem('accent') || 'blue';
  });

  const [motion, setMotion] = useState(() => {
    const stored = localStorage.getItem('motion');
    if (stored) {
      return stored;
    }
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches
      ? 'reduced'
      : 'full';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    document.documentElement.setAttribute('data-density', density);
    localStorage.setItem('density', density);
  }, [density]);

  useEffect(() => {
    document.documentElement.setAttribute('data-accent', accent);
    localStorage.setItem('accent', accent);
  }, [accent]);

  useEffect(() => {
    document.documentElement.setAttribute('data-motion', motion);
    localStorage.setItem('motion', motion);
  }, [motion]);

  const handleThemeToggle = () => {
    setTheme((current) => (current === 'dark' ? 'light' : 'dark'));
  };

  return (
    <Router>
      <div className="app-container">
        <Navbar theme={theme} onToggleTheme={handleThemeToggle} />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/profile" element={<UserProfile />} />
            <Route path="/health-profile" element={<HealthProfile />} />
            <Route path="/emergency-contacts" element={<EmergencyContact />} />
            <Route path="/fitness" element={<FitnessSummary />} />
            <Route path="/wearables" element={<WearableIntegration />} />
            <Route path="/metrics" element={<HealthMetrics />} />
            <Route path="/reports" element={<MedicalReports />} />
            <Route path="/reminders" element={<Reminders />} />
            <Route path="/assistant" element={<AIAssistant />} />
          </Routes>
        </main>
        <SettingsPanel
          density={density}
          setDensity={setDensity}
          accent={accent}
          setAccent={setAccent}
          motion={motion}
          setMotion={setMotion}
        />
      </div>
    </Router>
  );
}

export default App;
