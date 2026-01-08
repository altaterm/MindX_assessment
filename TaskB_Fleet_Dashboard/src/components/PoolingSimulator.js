import React, { useState, useMemo } from 'react';
import './PoolingSimulator.css';

function PoolingSimulator({ vessels }) {
  const [selectedDeficit, setSelectedDeficit] = useState(null);
  const [selectedSurplus, setSelectedSurplus] = useState(null);
  const [simulationResult, setSimulationResult] = useState(null);

  // Separate vessels by status
  const { deficitVessels, surplusVessels } = useMemo(() => {
    const deficit = vessels.filter(v => v.status === 'Deficit');
    const surplus = vessels.filter(v => v.status === 'Surplus');
    
    // Sort by absolute compliance balance (most critical first)
    deficit.sort((a, b) => a.compliance_balance - b.compliance_balance);
    surplus.sort((a, b) => b.compliance_balance - a.compliance_balance);
    
    return {
      deficitVessels: deficit,
      surplusVessels: surplus
    };
  }, [vessels]);

  // Calculate pooling result
  const simulatePooling = () => {
    if (!selectedDeficit || !selectedSurplus) {
      return;
    }

    const deficitBalance = selectedDeficit.compliance_balance;
    const surplusBalance = selectedSurplus.compliance_balance;
    const netBalance = surplusBalance + deficitBalance;

    setSimulationResult({
      deficitVessel: selectedDeficit,
      surplusVessel: selectedSurplus,
      deficitBalance,
      surplusBalance,
      netBalance,
      isSuccessful: netBalance >= 0,
      remainingDeficit: netBalance < 0 ? Math.abs(netBalance) : 0,
      remainingSurplus: netBalance > 0 ? netBalance : 0
    });
  };

  // Reset simulation
  const resetSimulation = () => {
    setSelectedDeficit(null);
    setSelectedSurplus(null);
    setSimulationResult(null);
  };

  // Get vessel display name
  const getVesselDisplayName = (vessel) => {
    return `${vessel.vessel_id} - ${vessel.ship_type} (${vessel.month})`;
  };

  return (
    <div className="pooling-simulator">
      {/* Instructions */}
      <div className="simulator-instructions">
        <h3>How It Works</h3>
        <p>
          Select one <strong className="deficit-text">Deficit</strong> vessel and one{' '}
          <strong className="surplus-text">Surplus</strong> vessel to simulate compliance pooling.
          The simulator will calculate if the surplus can offset the deficit.
        </p>
      </div>

      {/* Selection Area */}
      <div className="selection-area">
        {/* Deficit Vessel Selection */}
        <div className="selection-panel deficit-panel">
          <h3 className="panel-title">
            <span className="panel-icon">⚠️</span>
            Select Deficit Vessel
          </h3>
          <div className="vessel-count">
            {deficitVessels.length} deficit vessels available
          </div>
          
          <div className="vessel-list">
            {deficitVessels.slice(0, 10).map((vessel, index) => (
              <div
                key={`deficit-${vessel.vessel_id}-${vessel.month}-${index}`}
                className={`vessel-option deficit ${selectedDeficit?.vessel_id === vessel.vessel_id && selectedDeficit?.month === vessel.month ? 'selected' : ''}`}
                onClick={() => setSelectedDeficit(vessel)}
              >
                <div className="option-header">
                  <span className="vessel-name">{getVesselDisplayName(vessel)}</span>
                  <span className="balance-badge deficit">
                    {vessel.compliance_balance.toFixed(2)} kg/km
                  </span>
                </div>
                <div className="option-details">
                  <span>Route: {vessel.route_id}</span>
                  <span>GHG: {vessel.ghg_intensity.toFixed(2)} kg/km</span>
                </div>
              </div>
            ))}
            {deficitVessels.length > 10 && (
              <div className="more-vessels">
                + {deficitVessels.length - 10} more deficit vessels
              </div>
            )}
            {deficitVessels.length === 0 && (
              <div className="no-vessels">No deficit vessels available</div>
            )}
          </div>
        </div>

        {/* Surplus Vessel Selection */}
        <div className="selection-panel surplus-panel">
          <h3 className="panel-title">
            <span className="panel-icon">✅</span>
            Select Surplus Vessel
          </h3>
          <div className="vessel-count">
            {surplusVessels.length} surplus vessels available
          </div>
          
          <div className="vessel-list">
            {surplusVessels.slice(0, 10).map((vessel, index) => (
              <div
                key={`surplus-${vessel.vessel_id}-${vessel.month}-${index}`}
                className={`vessel-option surplus ${selectedSurplus?.vessel_id === vessel.vessel_id && selectedSurplus?.month === vessel.month ? 'selected' : ''}`}
                onClick={() => setSelectedSurplus(vessel)}
              >
                <div className="option-header">
                  <span className="vessel-name">{getVesselDisplayName(vessel)}</span>
                  <span className="balance-badge surplus">
                    +{vessel.compliance_balance.toFixed(2)} kg/km
                  </span>
                </div>
                <div className="option-details">
                  <span>Route: {vessel.route_id}</span>
                  <span>GHG: {vessel.ghg_intensity.toFixed(2)} kg/km</span>
                </div>
              </div>
            ))}
            {surplusVessels.length > 10 && (
              <div className="more-vessels">
                + {surplusVessels.length - 10} more surplus vessels
              </div>
            )}
            {surplusVessels.length === 0 && (
              <div className="no-vessels">No surplus vessels available</div>
            )}
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        <button
          className="simulate-button"
          onClick={simulatePooling}
          disabled={!selectedDeficit || !selectedSurplus}
        >
          🔄 Simulate Pooling
        </button>
        <button
          className="reset-button"
          onClick={resetSimulation}
          disabled={!selectedDeficit && !selectedSurplus && !simulationResult}
        >
          🔃 Reset
        </button>
      </div>

      {/* Simulation Result */}
      {simulationResult && (
        <div className={`simulation-result ${simulationResult.isSuccessful ? 'success' : 'partial'}`}>
          <div className="result-header">
            <h3>
              {simulationResult.isSuccessful ? '✅ Pooling Successful!' : '⚠️ Partial Offset'}
            </h3>
          </div>

          <div className="result-content">
            {/* Selected Vessels Summary */}
            <div className="vessels-summary">
              <div className="summary-card deficit">
                <div className="card-title">Deficit Vessel</div>
                <div className="card-vessel-name">
                  {getVesselDisplayName(simulationResult.deficitVessel)}
                </div>
                <div className="card-balance">
                  {simulationResult.deficitBalance.toFixed(2)} kg/km
                </div>
              </div>

              <div className="calculation-symbol">+</div>

              <div className="summary-card surplus">
                <div className="card-title">Surplus Vessel</div>
                <div className="card-vessel-name">
                  {getVesselDisplayName(simulationResult.surplusVessel)}
                </div>
                <div className="card-balance">
                  +{simulationResult.surplusBalance.toFixed(2)} kg/km
                </div>
              </div>

              <div className="calculation-symbol">=</div>

              <div className={`summary-card net ${simulationResult.isSuccessful ? 'success' : 'warning'}`}>
                <div className="card-title">Net Balance</div>
                <div className="card-vessel-name">Combined Result</div>
                <div className="card-balance">
                  {simulationResult.netBalance >= 0 ? '+' : ''}
                  {simulationResult.netBalance.toFixed(2)} kg/km
                </div>
              </div>
            </div>

            {/* Detailed Calculation */}
            <div className="calculation-details">
              <h4>Calculation Breakdown:</h4>
              <div className="calculation-steps">
                <div className="calc-step">
                  <span className="calc-label">Deficit Balance:</span>
                  <span className="calc-value deficit">{simulationResult.deficitBalance.toFixed(4)} kg/km</span>
                </div>
                <div className="calc-step">
                  <span className="calc-label">Surplus Balance:</span>
                  <span className="calc-value surplus">+{simulationResult.surplusBalance.toFixed(4)} kg/km</span>
                </div>
                <div className="calc-step total">
                  <span className="calc-label">Net Balance:</span>
                  <span className={`calc-value ${simulationResult.netBalance >= 0 ? 'surplus' : 'deficit'}`}>
                    {simulationResult.netBalance >= 0 ? '+' : ''}
                    {simulationResult.netBalance.toFixed(4)} kg/km
                  </span>
                </div>
              </div>
            </div>

            {/* Result Interpretation */}
            <div className="result-interpretation">
              {simulationResult.isSuccessful ? (
                <>
                  <div className="interpretation-icon success">✅</div>
                  <div className="interpretation-text">
                    <h4>Compliance Achieved!</h4>
                    <p>
                      The surplus vessel has <strong>successfully offset</strong> the deficit vessel's 
                      non-compliance. The combined net balance is positive.
                    </p>
                    {simulationResult.remainingSurplus > 0 && (
                      <p className="bonus-info">
                        <strong>Bonus:</strong> There is still{' '}
                        <span className="highlight-surplus">
                          +{simulationResult.remainingSurplus.toFixed(2)} kg/km
                        </span>{' '}
                        of surplus remaining that could be used to offset other vessels.
                      </p>
                    )}
                  </div>
                </>
              ) : (
                <>
                  <div className="interpretation-icon warning">⚠️</div>
                  <div className="interpretation-text">
                    <h4>Partial Offset</h4>
                    <p>
                      The surplus vessel has <strong>partially offset</strong> the deficit, but it's not 
                      enough to achieve full compliance.
                    </p>
                    <p className="deficit-info">
                      <strong>Remaining Deficit:</strong>{' '}
                      <span className="highlight-deficit">
                        {simulationResult.remainingDeficit.toFixed(2)} kg/km
                      </span>{' '}
                      still needs to be offset by additional surplus vessels or other measures.
                    </p>
                  </div>
                </>
              )}
            </div>

            {/* Business Implications */}
            <div className="business-implications">
              <h4>💼 Business Implications:</h4>
              <ul>
                {simulationResult.isSuccessful ? (
                  <>
                    <li>✅ Both vessels can be pooled for compliance reporting</li>
                    <li>✅ Deficit vessel avoids potential penalties</li>
                    <li>✅ Surplus vessel's credits are utilized effectively</li>
                    {simulationResult.remainingSurplus > 0 && (
                      <li>✅ Remaining surplus can offset additional deficits</li>
                    )}
                  </>
                ) : (
                  <>
                    <li>⚠️ Partial compliance improvement achieved</li>
                    <li>⚠️ Additional surplus vessels needed for full compliance</li>
                    <li>⚠️ Consider operational efficiency improvements</li>
                    <li>⚠️ May require purchasing external carbon credits</li>
                  </>
                )}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default PoolingSimulator;

