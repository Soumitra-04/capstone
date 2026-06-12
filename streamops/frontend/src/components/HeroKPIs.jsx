import { useState, useEffect } from 'react';
import './HeroKPIs.css';

export function HeroKPIs() {
  const [usersCount, setUsersCount] = useState('--');
  const [streamsCount, setStreamsCount] = useState('--');
  const [gamesCount, setGamesCount] = useState('--');

  useEffect(() => {
    const fetchKPIs = async () => {
      try {
        const [usersRes, streamsRes, gamesRes] = await Promise.all([
          fetch('/api/users').catch(() => null),
          fetch('/api/streams').catch(() => null),
          fetch('/api/games').catch(() => null)
        ]);

        if (usersRes && usersRes.ok) {
          const users = await usersRes.json();
          setUsersCount(users.length);
        }
        
        if (streamsRes && streamsRes.ok) {
          const streams = await streamsRes.json();
          const liveStreams = streams.filter(s => s.is_live);
          setStreamsCount(liveStreams.length);
        }

        if (gamesRes && gamesRes.ok) {
          const games = await gamesRes.json();
          setGamesCount(games.length);
        }
      } catch (err) {
        console.error('Error fetching KPIs:', err);
      }
    };

    fetchKPIs();
    const interval = setInterval(fetchKPIs, 5000);
    return () => clearInterval(interval);
  }, []);

  const kpis = [
    { label: 'USERS', value: usersCount, unit: '' },
    { label: 'STREAMS', value: streamsCount, unit: '' },
    { label: 'GAMES', value: gamesCount, unit: '' },
    { label: 'LATENCY', value: '72', unit: 'ms' },
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
