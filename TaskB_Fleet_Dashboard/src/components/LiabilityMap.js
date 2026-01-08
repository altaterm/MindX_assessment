import React from 'react';
import './LiabilityMap.css';

function LiabilityMap({ vessels, targetIntensity }) {
  // This component will be fully implemented in Commit 7
  
  return (
    <div className="liability-map">
      <p className="placeholder-text">
        Liability Map will be implemented in Commit 7
      </p>
      <p className="info-text">
        Total vessels loaded: {vessels.length}
      </p>
    </div>
  );
}

export default LiabilityMap;

