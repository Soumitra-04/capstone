import { Routes, Route } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { HeroKPIs } from './components/HeroKPIs';
import { ServiceHealth } from './components/ServiceHealth';
import { ActiveStreamsTable } from './components/ActiveStreamsTable';
import { TelemetryGrid } from './components/TelemetryGrid';
import './App.css';

function Overview() {
  return (
    <div className="dashboard-content">
      <HeroKPIs />
      
      <div className="middle-row">
        <div className="health-column">
          <ServiceHealth />
        </div>
        <div className="streams-column">
          <ActiveStreamsTable />
        </div>
      </div>
      
      <div className="bottom-row">
        <TelemetryGrid />
      </div>
    </div>
  );
}

function Placeholder({ title }) {
  return (
    <div className="dashboard-content" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)' }}>
      <h2>{title} Page coming soon...</h2>
    </div>
  );
}

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        <Header />
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/nodes" element={<Placeholder title="Nodes" />} />
          <Route path="/deployments" element={<Placeholder title="Deployments" />} />
          <Route path="/security" element={<Placeholder title="Security" />} />
          <Route path="/history" element={<Placeholder title="History" />} />
          <Route path="/docs" element={<Placeholder title="Documentation" />} />
          <Route path="/support" element={<Placeholder title="Support" />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
