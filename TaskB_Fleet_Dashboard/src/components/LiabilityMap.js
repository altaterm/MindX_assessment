import React, { useState, useMemo } from 'react';
import './LiabilityMap.css';

function LiabilityMap({ vessels, targetIntensity }) {
  const [filterStatus, setFilterStatus] = useState('all'); // 'all', 'surplus', 'deficit'
  const [sortBy, setSortBy] = useState('compliance_balance'); // 'compliance_balance', 'ghg_intensity', 'vessel_id'
  const [sortOrder, setSortOrder] = useState('desc'); // 'asc', 'desc'
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;

  // Filter and sort vessels
  const filteredAndSortedVessels = useMemo(() => {
    let result = [...vessels];

    // Apply status filter
    if (filterStatus !== 'all') {
      result = result.filter(v => v.status.toLowerCase() === filterStatus);
    }

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(v => 
        v.vessel_id.toLowerCase().includes(term) ||
        v.ship_type.toLowerCase().includes(term) ||
        v.route_id.toLowerCase().includes(term)
      );
    }

    // Apply sorting
    result.sort((a, b) => {
      let aVal, bVal;
      
      if (sortBy === 'vessel_id') {
        aVal = a.vessel_id;
        bVal = b.vessel_id;
      } else {
        aVal = parseFloat(a[sortBy]);
        bVal = parseFloat(b[sortBy]);
      }

      if (sortOrder === 'asc') {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });

    return result;
  }, [vessels, filterStatus, searchTerm, sortBy, sortOrder]);

  // Pagination
  const totalPages = Math.ceil(filteredAndSortedVessels.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentVessels = filteredAndSortedVessels.slice(startIndex, endIndex);

  // Statistics
  const stats = useMemo(() => {
    const surplus = filteredAndSortedVessels.filter(v => v.status === 'Surplus').length;
    const deficit = filteredAndSortedVessels.filter(v => v.status === 'Deficit').length;
    
    return {
      total: filteredAndSortedVessels.length,
      surplus,
      deficit
    };
  }, [filteredAndSortedVessels]);

  // Get risk level based on compliance balance
  const getRiskLevel = (complianceBalance) => {
    if (complianceBalance >= 10) return 'low';
    if (complianceBalance >= 0) return 'moderate';
    if (complianceBalance >= -10) return 'high';
    return 'critical';
  };

  // Get risk color
  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'low': return '#27ae60';
      case 'moderate': return '#f39c12';
      case 'high': return '#e67e22';
      case 'critical': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('desc');
    }
  };

  return (
    <div className="liability-map">
      {/* Controls Section */}
      <div className="map-controls">
        <div className="control-group">
          <label htmlFor="search">Search:</label>
          <input
            id="search"
            type="text"
            placeholder="Search vessel ID, ship type, or route..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1);
            }}
            className="search-input"
          />
        </div>

        <div className="control-group">
          <label htmlFor="filter">Filter:</label>
          <select
            id="filter"
            value={filterStatus}
            onChange={(e) => {
              setFilterStatus(e.target.value);
              setCurrentPage(1);
            }}
            className="filter-select"
          >
            <option value="all">All Vessels ({vessels.length})</option>
            <option value="surplus">Surplus Only</option>
            <option value="deficit">Deficit Only</option>
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="sort">Sort By:</label>
          <select
            id="sort"
            value={sortBy}
            onChange={(e) => {
              setSortBy(e.target.value);
              setCurrentPage(1);
            }}
            className="sort-select"
          >
            <option value="compliance_balance">Compliance Balance</option>
            <option value="ghg_intensity">GHG Intensity</option>
            <option value="vessel_id">Vessel ID</option>
          </select>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="stats-bar">
        <div className="stat-item">
          <span className="stat-label">Showing:</span>
          <span className="stat-value">{stats.total} vessels</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Surplus:</span>
          <span className="stat-value surplus">{stats.surplus}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Deficit:</span>
          <span className="stat-value deficit">{stats.deficit}</span>
        </div>
      </div>

      {/* Vessels Grid */}
      {currentVessels.length === 0 ? (
        <div className="no-results">
          <p>No vessels found matching your criteria.</p>
        </div>
      ) : (
        <>
          <div className="vessels-grid">
            {currentVessels.map((vessel, index) => {
              const riskLevel = getRiskLevel(vessel.compliance_balance);
              const riskColor = getRiskColor(riskLevel);

              return (
                <div 
                  key={`${vessel.vessel_id}-${vessel.month}-${index}`} 
                  className={`vessel-card ${vessel.status.toLowerCase()}`}
                  style={{ borderLeftColor: riskColor }}
                >
                  <div className="vessel-header">
                    <div className="vessel-id">{vessel.vessel_id}</div>
                    <div className={`status-badge ${vessel.status.toLowerCase()}`}>
                      {vessel.status}
                    </div>
                  </div>

                  <div className="vessel-info">
                    <div className="info-row">
                      <span className="info-label">Ship Type:</span>
                      <span className="info-value">{vessel.ship_type}</span>
                    </div>
                    <div className="info-row">
                      <span className="info-label">Route:</span>
                      <span className="info-value">{vessel.route_id}</span>
                    </div>
                    <div className="info-row">
                      <span className="info-label">Month:</span>
                      <span className="info-value">{vessel.month}</span>
                    </div>
                  </div>

                  <div className="vessel-metrics">
                    <div className="metric">
                      <div className="metric-label">Distance</div>
                      <div className="metric-value">{vessel.distance.toFixed(1)} km</div>
                    </div>
                    <div className="metric">
                      <div className="metric-label">CO₂</div>
                      <div className="metric-value">{vessel.co2_emission.toFixed(0)} kg</div>
                    </div>
                    <div className="metric">
                      <div className="metric-label">GHG Intensity</div>
                      <div className="metric-value">{vessel.ghg_intensity.toFixed(2)} kg/km</div>
                    </div>
                  </div>

                  <div className="compliance-info">
                    <div className="compliance-row">
                      <span className="label">Target:</span>
                      <span className="value">{vessel.target_intensity.toFixed(2)} kg/km</span>
                    </div>
                    <div className="compliance-row balance">
                      <span className="label">Balance:</span>
                      <span className={`value ${vessel.status.toLowerCase()}`}>
                        {vessel.compliance_balance >= 0 ? '+' : ''}
                        {vessel.compliance_balance.toFixed(2)} kg/km
                      </span>
                    </div>
                  </div>

                  <div className="risk-indicator">
                    <div 
                      className="risk-bar" 
                      style={{ 
                        width: '100%',
                        backgroundColor: riskColor,
                        height: '4px',
                        borderRadius: '2px'
                      }}
                    ></div>
                    <div className="risk-label" style={{ color: riskColor }}>
                      {riskLevel.toUpperCase()} RISK
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="pagination">
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                className="page-button"
              >
                ← Previous
              </button>

              <div className="page-info">
                Page {currentPage} of {totalPages}
                <span className="page-range">
                  (Showing {startIndex + 1}-{Math.min(endIndex, filteredAndSortedVessels.length)} of {filteredAndSortedVessels.length})
                </span>
              </div>

              <button
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
                className="page-button"
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}

      {/* Legend */}
      <div className="risk-legend">
        <div className="legend-title">Risk Level Guide:</div>
        <div className="legend-items">
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#27ae60' }}></div>
            <span>Low (≥ +10 kg/km)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#f39c12' }}></div>
            <span>Moderate (0 to +10 kg/km)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#e67e22' }}></div>
            <span>High (-10 to 0 kg/km)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#e74c3c' }}></div>
            <span>Critical (&lt; -10 kg/km)</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LiabilityMap;

