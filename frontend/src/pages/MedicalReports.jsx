import { useState, useEffect } from 'react';
import { Upload, FileText, Download, CheckCircle, Clock, AlertCircle, Search } from 'lucide-react';
import './MedicalReports.css';

export default function MedicalReports() {
  const [isScanning, setIsScanning] = useState(false);
  const [scanProgress, setScanProgress] = useState(0);

  const reports = [
    {
      id: 1,
      title: 'Comprehensive Blood Test',
      date: '2026-05-10',
      type: 'Lab Result',
      status: 'Processed',
      insights: 'Cholesterol levels slightly elevated. All other markers normal.',
    },
    {
      id: 2,
      title: 'Annual Physical Report',
      date: '2026-04-15',
      type: 'Clinical',
      status: 'Processed',
      insights: 'General health is good. Recommended to increase cardiovascular exercise.',
    },
    {
      id: 3,
      title: 'Chest X-Ray Results',
      date: '2026-05-14',
      type: 'Imaging',
      status: 'Pending',
      insights: 'Awaiting OCR extraction and radiologist review.',
    }
  ];

  const handleUpload = () => {
    setIsScanning(true);
    setScanProgress(0);
    
    // Simulate OCR scanning process
    const interval = setInterval(() => {
      setScanProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(() => setIsScanning(false), 1000);
          return 100;
        }
        return prev + 5;
      });
    }, 150);
  };

  return (
    <div className="container animate-enter">
      <div className="page-header">
        <div>
          <h1 className="text-gradient">Medical Reports & OCR</h1>
          <p>AI-powered document analysis and records management</p>
        </div>
      </div>

      <div className="grid grid-cols-3">
        <div className="col-span-1">
          <div className="glass-card scanner-card">
            <div className="scanner-header">
              <h2>Smart Upload</h2>
              <div className="badge badge-accent">OCR Engine Ready</div>
            </div>
            
            <div className={`upload-zone ${isScanning ? 'scanning' : ''}`} onClick={!isScanning ? handleUpload : undefined}>
              {isScanning ? (
                <div className="scanner-active">
                  <div className="scan-line"></div>
                  <FileText size={48} className="text-primary pulse" />
                  <div className="scan-progress-text">Extracting Data... {scanProgress}%</div>
                  <div className="scan-progress-bar">
                    <div className="scan-progress-fill" style={{ width: `${scanProgress}%` }}></div>
                  </div>
                </div>
              ) : (
                <div className="upload-content">
                  <Upload size={48} className="text-muted mb-3" />
                  <h3>Drop your report here</h3>
                  <p className="text-muted text-sm text-center">Supported formats: PDF, JPG, PNG.<br/>Our AI will extract the vital metrics automatically.</p>
                  <button className="btn btn-primary mt-4">Browse Files</button>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="col-span-2">
          <div className="glass-card full-height">
            <div className="flex-between mb-4">
              <h2>Recent Documents</h2>
              <div className="search-box">
                <Search size={18} className="text-muted" />
                <input type="text" placeholder="Search reports..." className="search-input" />
              </div>
            </div>

            <div className="reports-list">
              {reports.map((report) => (
                <div key={report.id} className="report-item">
                  <div className="report-icon-wrapper">
                    <FileText size={24} className="text-primary" />
                  </div>
                  <div className="report-details">
                    <div className="flex-between">
                      <h4>{report.title}</h4>
                      {report.status === 'Processed' ? (
                        <span className="badge badge-success"><CheckCircle size={12} className="mr-1 inline"/> Processed</span>
                      ) : (
                        <span className="badge badge-warning"><Clock size={12} className="mr-1 inline"/> Processing</span>
                      )}
                    </div>
                    <div className="report-meta">
                      <span className="text-muted text-sm">{report.date}</span>
                      <span className="dot-separator">•</span>
                      <span className="badge badge-primary">{report.type}</span>
                    </div>
                    <div className="report-insights">
                      <AlertCircle size={14} className="text-accent" />
                      <p>{report.insights}</p>
                    </div>
                  </div>
                  <div className="report-actions">
                    <button className="btn btn-secondary btn-icon" title="Download">
                      <Download size={18} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
