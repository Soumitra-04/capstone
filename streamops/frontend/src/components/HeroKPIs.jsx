import { useState, useEffect } from 'react';
import client from '../api/client';
import './HeroKPIs.css';

export function HeroKPIs() {
  const [usersCount, setUsersCount] = useState(0);
  const [streamsCount, setStreamsCount] = useState(0);
  const [gamesCount, setGamesCount] = useState(0);
  const [latencyMs, setLatencyMs] = useState('--');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [usersRes, streamsRes, gamesRes, telemetryRes] = await Promise.all([
          client.get('/users').catch(() => ({ data: [] })),
          client.get('/streams').catch(() => ({ data: [] })),
          client.get('/games').catch(() => ({ data: [] })),
          client.get('/streams/ops/telemetry').catch(() => ({ data: null }))
        ]);
        
        setUsersCount(usersRes.data ? usersRes.data.length : 0);
        setStreamsCount(streamsRes.data ? streamsRes.data.length : 0);
        setGamesCount(gamesRes.data ? gamesRes.data.length : 0);
        
        if (telemetryRes.data && telemetryRes.data.latency) {
          const lats = telemetryRes.data.latency;
          if (lats.average_ms !== undefined && lats.average_ms !== '--') {
            setLatencyMs(lats.average_ms);
          } else {
            const avg = Math.round(((lats.user_ms || 0) + (lats.stream_ms || 0) + (lats.content_ms || 0)) / 3);
            setLatencyMs(avg || '--');
          }
        }
      } catch (err) {
        console.error("Failed to fetch KPIs:", err);
      }
    };
    
    fetchData();
    const intervalId = setInterval(fetchData, 5000);
    return () => clearInterval(intervalId);
  }, []);

  const kpis = [
    { label: 'USERS', value: usersCount, unit: '' },
    { label: 'STREAMS', value: streamsCount, unit: '' },
    { label: 'GAMES', value: gamesCount, unit: '' },
    { label: 'LATENCY', value: latencyMs, unit: latencyMs !== '--' ? 'ms' : '' },
  ];

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
