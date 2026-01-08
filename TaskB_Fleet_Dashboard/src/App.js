import React, { useState, useEffect } from 'react';
import './App.css';
import FleetOverview from './components/FleetOverview';
import LiabilityMap from './components/LiabilityMap';
import PoolingSimulator from './components/PoolingSimulator';

function App() {
  const [complianceData, setComplianceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadComplianceData();
  }, []);

  const loadComplianceData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Try to load from public folder first
      const response = await fetch('/compliance_results.json');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Validate data structure
      if (!data.metadata || !data.vessels) {
        throw new Error('Invalid data format: missing required fields');
      }

      setComplianceData(data);
      console.log('✓ Compliance data loaded:', {
        total_vessels: data.vessels.length,
        surplus: data.metadata.compliance_summary.surplus_count,
        deficit: data.metadata.compliance_summary.deficit_count
      });
      
    } catch (err) {
      console.error('Error loading compliance data:', err);
      setError(err.message);
      
      // Set demo data for development
      setComplianceData({
        metadata: {
          generated_at: new Date().toISOString(),
          total_records: 0,
          model_performance: {
            test_rmse: 1010.14,
            test_mae: 625.43,
            test_r2: 0.9951
          },
          compliance_summary: {
            target_year: 2026,
            fleet_average_intensity: 78.8535,
            target_intensity: 74.9108,
            reduction_percentage: 5.0,
            total_vessels: 0,
            surplus_count: 0,
            deficit_count: 0,
            total_surplus: 0,
            total_deficit: 0
          }
        },
        vessels: []
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <p>Loading fleet compliance data...</p>
      </div>
    );
  }

  if (error && (!complianceData || complianceData.vessels.length === 0)) {
    return (
      <div className="app-error">
        <div className="error-container">
          <h2>⚠️ Data Loading Error</h2>
          <p>{error}</p>
          <div className="error-instructions">
            <h3>Setup Instructions:</h3>
            <ol>
              <li>Copy <code>compliance_results.json</code> from Task A output to <code>public/</code> folder</li>
              <li>Or run: <code>python TaskA_Compliance_Engine/run_pipeline.py</code></li>
              <li>Then copy the generated JSON to: <code>TaskB_Fleet_Dashboard/public/compliance_results.json</code></li>
              <li>Refresh this page</li>
            </ol>
          </div>
          <button onClick={loadComplianceData} className="retry-button">
            Retry Loading Data
          </button>
        </div>
      </div>
    );
  }

  const summary = complianceData.metadata.compliance_summary;
  const vessels = complianceData.vessels;

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>⚓ MindX Fleet Arbitrage Dashboard</h1>
          <p className="header-subtitle">Maritime Compliance Management System</p>
        </div>
        <div className="header-info">
          <span className="info-badge">Target: {summary.target_year}</span>
          <span className="info-badge">Fleet: {summary.total_vessels} vessels</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {/* Fleet Overview Section */}
        <section className="dashboard-section">
          <FleetOverview summary={summary} />
        </section>

        {/* Liability Map Section */}
        <section className="dashboard-section">
          <h2 className="section-title">📊 Fleet Liability Map</h2>
          <LiabilityMap vessels={vessels} targetIntensity={summary.target_intensity} />
        </section>

        {/* Pooling Simulator Section */}
        <section className="dashboard-section">
          <h2 className="section-title">🔄 Compliance Pooling Simulator</h2>
          <PoolingSimulator vessels={vessels} />
        </section>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>MindX Strategic Navigator Challenge | Task B: Fleet Arbitrage Dashboard</p>
        <p className="footer-timestamp">
          Data generated: {new Date(complianceData.metadata.generated_at).toLocaleString()}
        </p>
      </footer>
    </div>
  );
}

export default App;

