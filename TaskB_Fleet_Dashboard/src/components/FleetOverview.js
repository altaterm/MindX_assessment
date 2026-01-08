import React from 'react';
import './FleetOverview.css';

function FleetOverview({ summary }) {
  const surplusPercentage = (summary.surplus_count / summary.total_vessels * 100).toFixed(1);
  const deficitPercentage = (summary.deficit_count / summary.total_vessels * 100).toFixed(1);
  
  const netPosition = summary.total_surplus + summary.total_deficit;
  const netStatus = netPosition >= 0 ? 'positive' : 'negative';

  return (
    <div className="fleet-overview">
      <h2 className="overview-title">🎯 Fleet Overview</h2>
      
      <div className="overview-grid">
        {/* Total Vessels Card */}
        <div className="overview-card total">
          <div className="card-icon">⚓</div>
          <div className="card-content">
            <h3>{summary.total_vessels}</h3>
            <p>Total Vessels</p>
          </div>
        </div>

        {/* Surplus Card */}
        <div className="overview-card surplus">
          <div className="card-icon">✅</div>
          <div className="card-content">
            <h3>{summary.surplus_count}</h3>
            <p>Surplus Vessels</p>
            <span className="card-percentage">{surplusPercentage}%</span>
          </div>
        </div>

        {/* Deficit Card */}
        <div className="overview-card deficit">
          <div className="card-icon">⚠️</div>
          <div className="card-content">
            <h3>{summary.deficit_count}</h3>
            <p>Deficit Vessels</p>
            <span className="card-percentage">{deficitPercentage}%</span>
          </div>
        </div>

        {/* Target Year Card */}
        <div className="overview-card target">
          <div className="card-icon">🎯</div>
          <div className="card-content">
            <h3>{summary.target_year}</h3>
            <p>Target Year</p>
            <span className="card-percentage">{summary.reduction_percentage}% reduction</span>
          </div>
        </div>
      </div>

      {/* Detailed Metrics */}
      <div className="metrics-section">
        <div className="metric-row">
          <div className="metric-label">Fleet Average Intensity</div>
          <div className="metric-value">{summary.fleet_average_intensity.toFixed(4)} kg/km</div>
        </div>
        
        <div className="metric-row">
          <div className="metric-label">Target Intensity</div>
          <div className="metric-value highlight">{summary.target_intensity.toFixed(4)} kg/km</div>
        </div>
        
        <div className="metric-row">
          <div className="metric-label">Total Surplus Available</div>
          <div className="metric-value positive">+{summary.total_surplus.toFixed(2)} kg/km</div>
        </div>
        
        <div className="metric-row">
          <div className="metric-label">Total Deficit</div>
          <div className="metric-value negative">{summary.total_deficit.toFixed(2)} kg/km</div>
        </div>
        
        <div className="metric-row net">
          <div className="metric-label">Net Fleet Position</div>
          <div className={`metric-value ${netStatus}`}>
            {netPosition >= 0 ? '+' : ''}{netPosition.toFixed(2)} kg/km
          </div>
        </div>
      </div>

      {/* Visual Progress Bar */}
      <div className="compliance-bar">
        <div className="bar-label">Fleet Compliance Status</div>
        <div className="bar-container">
          <div 
            className="bar-fill surplus-bar" 
            style={{ width: `${surplusPercentage}%` }}
          >
            {surplusPercentage}%
          </div>
          <div 
            className="bar-fill deficit-bar" 
            style={{ width: `${deficitPercentage}%` }}
          >
            {deficitPercentage}%
          </div>
        </div>
        <div className="bar-legend">
          <span className="legend-item">
            <span className="legend-dot surplus"></span> Surplus
          </span>
          <span className="legend-item">
            <span className="legend-dot deficit"></span> Deficit
          </span>
        </div>
      </div>
    </div>
  );
}

export default FleetOverview;

