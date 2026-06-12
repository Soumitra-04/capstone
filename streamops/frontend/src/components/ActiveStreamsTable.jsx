import { useState, useEffect } from 'react';
import './ActiveStreamsTable.css';

export function ActiveStreamsTable() {
  const [streams, setStreams] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStreams = async () => {
      try {
        const res = await fetch('/api/streams');
        if (res.ok) {
          const data = await res.json();
          setStreams(data);
        }
      } catch (err) {
        console.error('Error fetching streams:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStreams();
    const interval = setInterval(fetchStreams, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="hud-card active-streams-card">
      <div className="card-header">
        <span className="text-label card-title">ACTIVE STREAMS</span>
        <span className="text-label header-status">
          {loading ? 'LOADING...' : 'PULLING LIVE DATA'}
        </span>
      </div>

      <div className="table-container">
        <table className="streams-table">
          <thead>
            <tr>
              <th className="text-label text-left">ID</th>
              <th className="text-label text-left">TITLE</th>
              <th className="text-label text-right">VIEWERS</th>
              <th className="text-label text-right">STATUS</th>
            </tr>
          </thead>
          <tbody>
            {!loading && streams.length === 0 && (
              <tr>
                <td colSpan="4" className="text-label text-center" style={{ padding: '2rem 0', opacity: 0.5 }}>
                  No active streams
                </td>
              </tr>
            )}
            {streams.map((stream) => (
              <tr key={stream.id} className="table-row">
                <td className="text-mono cell-id">{stream.id}</td>
                <td className="text-data cell-title">{stream.title}</td>
                <td className="text-mono cell-viewers text-right">
                  {stream.viewer_count.toLocaleString()}
                </td>
                <td className="cell-status text-right">
                  <span className={`text-label status-text ${stream.is_live ? 'healthy-text' : ''}`}>
                    {stream.is_live ? 'LIVE' : 'OFFLINE'}
                  </span>
                  <span className={`status-dot ${stream.is_live ? 'healthy' : 'offline'}`} style={!stream.is_live ? { backgroundColor: '#555', boxShadow: 'none' } : {}}></span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
