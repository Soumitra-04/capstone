import { useState, useEffect } from 'react';
import './ServiceHealth.css';

export function ServiceHealth() {
  const [healthState, setHealthState] = useState([
    { name: 'User Service', endpoint: '/api/users', status: 'CHECKING...' },
    { name: 'Stream Service', endpoint: '/api/streams', status: 'CHECKING...' },
    { name: 'Content Service', endpoint: '/api/games', status: 'CHECKING...' },
  ]);

  useEffect(() => {
    const checkHealth = async () => {
      const updatedHealth = await Promise.all(
        healthState.map(async (svc) => {
          try {
            const res = await fetch(svc.endpoint);
            return {
              ...svc,
              status: res.ok ? 'HEALTHY' : 'OFFLINE'
            };
          } catch (err) {
            return { ...svc, status: 'OFFLINE' };
          }
        })
      );
      setHealthState(updatedHealth);
    };

    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []); // Run once on mount

  return (
    <div className="hud-card service-health-card">
      <div className="text-label card-title">SERVICE HEALTH</div>
      
      <div className="service-list">
        {healthState.map((svc, idx) => (
          <div key={idx} className="service-row">
            <span className="text-data service-name">{svc.name}</span>
            <div className="service-status">
              <span className={`text-label status-text ${svc.status === 'HEALTHY' ? 'healthy-text' : svc.status === 'OFFLINE' ? '' : 'checking-text'}`}>
                {svc.status}
              </span>
              <span className={`status-dot ${svc.status === 'HEALTHY' ? 'healthy' : svc.status === 'OFFLINE' ? 'offline' : 'checking'}`} 
                    style={svc.status !== 'HEALTHY' ? { backgroundColor: svc.status === 'OFFLINE' ? '#ff3333' : '#888', boxShadow: 'none' } : {}}>
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
