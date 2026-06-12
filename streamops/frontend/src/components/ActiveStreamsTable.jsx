import { useState, useEffect } from 'react';
import client from '../api/client';
import './ActiveStreamsTable.css';

export function ActiveStreamsTable() {
  const [streams, setStreams] = useState([]);

  useEffect(() => {
    const fetchStreams = async () => {
      try {
        const response = await client.get('/streams');
        setStreams(response.data);
      } catch (error) {
        console.error('Error fetching streams:', error);
      }
    };

    fetchStreams();
    const intervalId = setInterval(fetchStreams, 5000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="hud-card active-streams-card">
      <div className="card-header">
        <span className="text-label card-title">ACTIVE STREAMS</span>
        <span className="text-label header-status">PULLING LIVE DATA</span>
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
            {streams.slice(0, 5).map((stream) => (
              <tr key={stream.id} className="table-row">
                <td className="text-mono cell-id">{stream.id.substring(0, 8)}</td>
                <td className="text-data cell-title">{stream.title}</td>
                <td className="text-mono cell-viewers text-right">{stream.viewer_count.toLocaleString()}</td>
                <td className="cell-status text-right">
                  <span className="text-label status-text healthy-text">{stream.is_live ? 'LIVE' : 'OFFLINE'}</span>
                  <span className={`status-dot ${stream.is_live ? 'healthy' : 'error'}`}></span>
                </td>
              </tr>
            ))}
            {streams.length === 0 && (
              <tr>
                <td colSpan="4" style={{ textAlign: 'center', padding: '1rem', color: 'var(--text-secondary)' }}>
                  No active streams
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
