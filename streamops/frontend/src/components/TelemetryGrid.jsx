import { useState, useEffect } from 'react';
import { Zap, Loader2 } from 'lucide-react';
import apiClient from '../api/client';
import './TelemetryGrid.css';

export function TelemetryGrid() {
  const [telemetry, setTelemetry] = useState({
    latency: { user_ms: '--', stream_ms: '--', content_ms: '--', average_ms: '--' },
    traffic: { total_requests: 0, error_count: 0, error_rate_pct: 0, success_rate_pct: 0 },
    deployment: { version: '--', environment: '--', git_sha: '--' }
  });

  const [loadTest, setLoadTest] = useState({
    avg_response_time_ms: 0,
    p95_response_time_ms: 0,
    error_count: 0,
    total_count: 0
  });

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        const res = await apiClient.get('/streams/ops/telemetry');
        if (res.data) setTelemetry(res.data);
      } catch (err) {
        console.error('Failed to fetch telemetry:', err);
      }
    };
    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchLoadTest = async () => {
    setIsLoading(true);
    try {
      const res = await apiClient.get('/streams/ops/last-load-test');
      if (res.data) setLoadTest(res.data);
    } catch (err) {
      console.error('Failed to fetch load test:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchLoadTest();
  }, []);

  return (
    <div className="telemetry-grid">
      {/* Top Left: API Performance */}
      <div className="hud-card grid-card">
        <div className="text-label card-title">API PERFORMANCE</div>
        <div className="perf-list">
          <div className="perf-row">
            <span className="text-data">User Latency:</span>
            <span className="text-mono healthy-text">{telemetry.latency.user_ms}{telemetry.latency.user_ms !== '--' ? 'ms' : ''}</span>
          </div>
          <div className="perf-row">
            <span className="text-data">Vibe:</span>
            <span className="text-mono healthy-text">{telemetry.latency.stream_ms}{telemetry.latency.stream_ms !== '--' ? 'ms' : ''}</span>
          </div>
          <div className="perf-row">
            <span className="text-data">Content:</span>
            <span className="text-mono healthy-text">{telemetry.latency.content_ms}{telemetry.latency.content_ms !== '--' ? 'ms' : ''}</span>
          </div>
        </div>
        <div className="perf-avg">
          <span className="text-label">AVERAGE RESPONSE TIME:</span>
          <span className="text-mono healthy-text">
            {telemetry.latency.average_ms !== undefined && telemetry.latency.average_ms !== '--' 
              ? telemetry.latency.average_ms 
              : Math.round(((telemetry.latency.user_ms || 0) + (telemetry.latency.stream_ms || 0) + (telemetry.latency.content_ms || 0)) / 3) || '--'}
            MS
          </span>
        </div>
      </div>

      {/* Top Right: Traffic Metrics */}
      <div className="hud-card grid-card traffic-card">
        <div className="text-label card-title">TRAFFIC METRICS</div>
        <div className="traffic-grid">
          <div className="metric-box">
            <div className="text-label metric-label">REQUESTS TODAY</div>
            <div className="text-data metric-value">{telemetry.traffic.total_requests.toLocaleString()}</div>
          </div>
          <div className="metric-box">
            <div className="text-label metric-label">ERROR COUNT</div>
            <div className="text-data metric-value">{telemetry.traffic.error_count.toLocaleString()}</div>
          </div>
          <div className="metric-box">
            <div className="text-label metric-label">ERROR RATE</div>
            <div className="text-data metric-value">{telemetry.traffic.error_rate_pct}%</div>
          </div>
          <div className="metric-box success-box">
            <div className="text-label metric-label">SUCCESS RATE</div>
            <div className="text-data metric-value healthy-text">{telemetry.traffic.success_rate_pct}%</div>
          </div>
        </div>
      </div>

      {/* Bottom Left: Deployment Info */}
      <div className="hud-card grid-card">
        <div className="text-label card-title">DEPLOYMENT INFO</div>
        <div className="deploy-list">
          <div className="deploy-row">
            <span className="text-data deploy-label">Version:</span>
            <span className="text-mono deploy-value">{telemetry.deployment.version}</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">Environment:</span>
            <span className="text-mono deploy-value">{telemetry.deployment.environment}</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">Git SHA:</span>
            <span className="text-mono deploy-value healthy-text">{telemetry.deployment.git_sha}</span>
          </div>
        </div>
      </div>

      {/* Bottom Right: Load Test Results */}
      <div className="hud-card grid-card load-test-card">
        <div className="text-label card-title">LOAD TEST RESULTS</div>
        <div className="load-list">
          <div className="deploy-row">
            <span className="text-data deploy-label">Requests Sent:</span>
            <span className="text-mono deploy-value">{loadTest.total_count.toLocaleString()}</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">Avg Latency:</span>
            <span className="text-mono deploy-value">{loadTest.avg_response_time_ms}ms</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">P95:</span>
            <span className="text-mono deploy-value alert-text">{loadTest.p95_response_time_ms}ms</span>
          </div>
          <div className="deploy-row">
            <span className="text-data deploy-label">Failed:</span>
            <span className="text-mono deploy-value">{loadTest.error_count.toLocaleString()}</span>
          </div>
        </div>
        <button 
          className="run-test-btn text-label"
          onClick={fetchLoadTest}
          disabled={isLoading}
          style={{ opacity: isLoading ? 0.7 : 1, cursor: isLoading ? 'not-allowed' : 'pointer' }}
        >
          {isLoading ? (
            <><Loader2 size={14} className="btn-icon" style={{ animation: 'spin 1s linear infinite' }} /> FETCHING...</>
          ) : (
            <><Zap size={14} className="btn-icon" /> REFRESH RESULTS</>
          )}
        </button>
        <style>{`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    </div>
  );
}
