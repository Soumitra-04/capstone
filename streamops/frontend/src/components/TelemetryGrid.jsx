import { Zap } from 'lucide-react';
import './TelemetryGrid.css';

export function TelemetryGrid() {
  return (
    <div className="telemetry-grid">
      {/* Top Left: API Performance */}
      <div className="hud-card grid-card">
        <div className="text-label card-title">API PERFORMANCE</div>
        <div className="perf-list">
          <div className="perf-row">
            <span className="text-data">User Latency:</span>
            <span className="text-mono healthy-text">48ms</span>
          </div>
          <div className="perf-row">
            <span className="text-data">Vibe:</span>
            <span className="text-mono healthy-text">71ms</span>
          </div>
          <div className="perf-row">
            <span className="text-data">Content:</span>
            <span className="text-mono healthy-text">62ms</span>
          </div>
        </div>
        <div className="perf-avg">
          <span className="text-label">AVERAGE RESPONSE TIME:</span>
          <span className="text-mono healthy-text">60MS</span>
        </div>
      </div>

      {/* Top Right: Traffic Metrics */}
      <div className="hud-card grid-card traffic-card">
        <div className="text-label card-title">TRAFFIC METRICS</div>
        <div className="traffic-grid">
          <div className="metric-box">
            <div className="text-label metric-label">REQUESTS TODAY</div>
            <div className="text-data metric-value">12,450</div>
          </div>
          <div className="metric-box">
            <div className="text-label metric-label">REQ/MIN</div>
            <div className="text-data metric-value">180</div>
          </div>
          <div className="metric-box">
            <div className="text-label metric-label">ERROR RATE</div>
            <div className="text-data metric-value">0.3%</div>
          </div>
          <div className="metric-box success-box">
            <div className="text-label metric-label">SUCCESS RATE</div>
            <div className="text-data metric-value healthy-text">99.7%</div>
          </div>
        </div>
      </div>

      {/* Bottom Left: Deployment Info */}
      <div className="hud-card grid-card">
        <div className="text-label card-title">DEPLOYMENT INFO</div>
        <div className="deploy-list">
          <div className="deploy-row">
            <span className="text-data deploy-label">Version:</span>
            <span className="text-mono deploy-value">v0.3.0</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">Environment:</span>
            <span className="text-mono deploy-value">Kubernetes</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">Build:</span>
            <span className="text-mono deploy-value">#42</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">Branch:</span>
            <span className="text-mono deploy-value healthy-text">main</span>
          </div>
        </div>
      </div>

      {/* Bottom Right: Load Test Results */}
      <div className="hud-card grid-card load-test-card">
        <div className="text-label card-title">LOAD TEST RESULTS</div>
        <div className="load-list">
          <div className="deploy-row">
            <span className="text-data deploy-label">Requests Sent:</span>
            <span className="text-mono deploy-value">10,000</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">Avg Latency:</span>
            <span className="text-mono deploy-value">72ms</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">P95:</span>
            <span className="text-mono deploy-value alert-text">105ms</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">Failed:</span>
            <span className="text-mono deploy-value">0</span>
          </div>
        </div>
        <button className="run-test-btn text-label">
          <Zap size={14} className="btn-icon" /> RUN LOAD TEST
        </button>
      </div>
    </div>
  );
}
