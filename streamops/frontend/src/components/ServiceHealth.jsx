import { useState, useEffect } from 'react';
import apiClient from '../api/client';
import './ServiceHealth.css';

const SERVICES = [
  { name: 'User Service', key: 'user' },
  { name: 'Stream Service', key: 'stream' },
  { name: 'Content Service', key: 'content' },
];

export function ServiceHealth() {
  const [healthData, setHealthData] = useState([]);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await apiClient.get('/streams/ops/health');
        if (res.data && res.data.services) {
          setHealthData(res.data.services);
        }
      } catch (error) {
        console.error('Failed to fetch ops health:', error);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  // Merge the static SERVICES array with dynamic data so the order is maintained,
  // or just use the data if available. The backend returns exact names.
  const displayServices = SERVICES.map(svc => {
    const found = healthData.find(h => h.name === svc.name);
    return {
      name: svc.name,
      status: found ? found.status : 'LOADING...',
      latency_ms: found ? found.latency_ms : null
    };
  });

  return (
    <div className="hud-card service-health-card">
      <div className="text-label card-title">SERVICE HEALTH</div>
      
      <div className="service-list">
        {displayServices.map((svc, idx) => (
          <div key={idx} className="service-row">
            <span className="text-data service-name">{svc.name}</span>
            <div className="service-status">
              <span className={`text-label status-text ${svc.status === 'HEALTHY' ? 'healthy-text' : 'alert-text'}`}>
                {svc.status} {svc.latency_ms !== null && svc.status === 'HEALTHY' ? `· ${svc.latency_ms}ms` : ''}
              </span>
              <span className={`status-dot ${svc.status.toLowerCase()}`}></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
