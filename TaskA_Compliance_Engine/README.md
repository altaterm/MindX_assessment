# Task A: Compliance Engine

## Overview

Python-based machine learning engine that predicts CO2 emissions and computes vessel compliance with GHG intensity regulations.

## Components

1. **exploratory.ipynb** - Dataset analysis and feature engineering
2. **model.py** - ML model training and prediction
3. **compliance.py** - GHG intensity and compliance calculations
4. **run_pipeline.py** - End-to-end pipeline execution

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run Complete Pipeline

```bash
python run_pipeline.py
```

This will:
1. Load the dataset
2. Train the ML model
3. Predict CO2 emissions
4. Calculate GHG intensity
5. Compute compliance balance
6. Generate `output/compliance_results.json`

### Explore Data

```bash
jupyter notebook exploratory.ipynb
```

## Output Format

`output/compliance_results.json` contains:

```json
{
  "vessel_id": "NG001",
  "ship_type": "Oil Service Boat",
  "distance": 132.26,
  "co2_emission": 10625.76,
  "ghg_intensity": 80.35,
  "target_intensity": 76.33,
  "compliance_balance": -4.02,
  "status": "Deficit"
}
```

## Methodology

### 1. CO2 Prediction Model
- **Algorithm**: Linear Regression
- **Features**: Ship Type (encoded), Distance, Fuel Consumption
- **Target**: CO2 Emissions (Kg)

### 2. GHG Intensity Calculation
```
GHG Intensity = CO2 Emission (Kg) / Distance (km)
```

### 3. Regulatory Benchmark
```
Target Intensity = Fleet Average Intensity × 0.95
```

### 4. Compliance Balance
```
Compliance Balance = Target Intensity - Vessel Intensity

If CB > 0: Surplus (vessel is compliant)
If CB < 0: Deficit (vessel needs offsetting)
```

## Assumptions

- Dataset represents typical Nigerian maritime operations
- Distance is in kilometers
- CO2 emissions are in kilograms
- All vessels subject to same 2026 regulatory target
- 5% reduction from fleet average represents compliance threshold

## Performance Metrics

*Will be updated after model training*

- RMSE: TBD
- MAE: TBD
- R² Score: TBD

