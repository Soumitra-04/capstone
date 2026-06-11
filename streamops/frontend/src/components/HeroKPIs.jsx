import './HeroKPIs.css';

const kpis = [
  { label: 'USERS', value: '125', unit: '' },
  { label: 'STREAMS', value: '18', unit: '' },
  { label: 'GAMES', value: '34', unit: '' },
  { label: 'LATENCY', value: '72', unit: 'ms' },
];

export function HeroKPIs() {
  return (
    <div className="hero-kpis">
      {kpis.map((kpi, idx) => (
        <div key={idx} className="hud-card kpi-card">
          <div className="text-label kpi-label">{kpi.label}</div>
          <div className="kpi-value-container">
            <span className="text-data kpi-value">{kpi.value}</span>
            {kpi.unit && <span className="text-data kpi-unit">{kpi.unit}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}
