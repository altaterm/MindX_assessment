import React from 'react';
import './PoolingSimulator.css';

function PoolingSimulator({ vessels }) {
  // This component will be fully implemented in Commit 8
  
  return (
    <div className="pooling-simulator">
      <p className="placeholder-text">
        Pooling Simulator will be implemented in Commit 8
      </p>
      <p className="info-text">
        Vessels available for pooling: {vessels.length}
      </p>
    </div>
  );
}

export default PoolingSimulator;

