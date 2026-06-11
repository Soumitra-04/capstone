import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { HeroKPIs } from './components/HeroKPIs';
import { ServiceHealth } from './components/ServiceHealth';
import { ActiveStreamsTable } from './components/ActiveStreamsTable';
import { TelemetryGrid } from './components/TelemetryGrid';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        <Header />
        
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
      </main>
    </div>
  );
}

export default App;
