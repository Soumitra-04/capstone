import './ServiceHealth.css';

const services = [
  { name: 'User Service', status: 'HEALTHY' },
  { name: 'Vibe Service', status: 'HEALTHY' },
  { name: 'Content Service', status: 'HEALTHY' },
];

export function ServiceHealth() {
  return (
    <div className="hud-card service-health-card">
      <div className="text-label card-title">SERVICE HEALTH</div>
      
      <div className="service-list">
        {services.map((svc, idx) => (
          <div key={idx} className="service-row">
            <span className="text-data service-name">{svc.name}</span>
            <div className="service-status">
              <span className="text-label status-text healthy-text">{svc.status}</span>
              <span className={`status-dot ${svc.status.toLowerCase()}`}></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
