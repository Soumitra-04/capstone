import './ActiveStreamsTable.css';

const streams = [
  { id: '1', title: 'Valorant Finals', viewers: '1,250', status: 'LIVE' },
  { id: '2', title: 'GTA RP', viewers: '824', status: 'LIVE' },
  { id: '3', title: 'CS2 Ranked', viewers: '213', status: 'LIVE' },
];

export function ActiveStreamsTable() {
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
            {streams.map((stream) => (
              <tr key={stream.id} className="table-row">
                <td className="text-mono cell-id">{stream.id}</td>
                <td className="text-data cell-title">{stream.title}</td>
                <td className="text-mono cell-viewers text-right">{stream.viewers}</td>
                <td className="cell-status text-right">
                  <span className="text-label status-text healthy-text">{stream.status}</span>
                  <span className="status-dot healthy"></span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
