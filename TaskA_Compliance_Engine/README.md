# Task A: Compliance Engine

## Overview

Python-based machine learning engine that predicts CO2 emissions and computes vessel compliance with GHG intensity regulations for the Nigerian maritime fleet.

**Status:** ✅ Complete and operational

## Components

1. **exploratory.ipynb** - Comprehensive dataset analysis and feature engineering
2. **model.py** - ML model (Linear Regression) for CO2 prediction
3. **compliance.py** - GHG intensity and regulatory compliance calculations
4. **run_pipeline.py** - End-to-end pipeline orchestration
5. **output/** - Generated compliance results and reports

## Installation

```bash
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8+
- pandas, numpy, scikit-learn
- matplotlib, seaborn (for visualization)
- jupyter (for notebook exploration)

## Quick Start

### Option 1: Run Complete Pipeline (Recommended)

```bash
python run_pipeline.py
```

This executes the full workflow:
1. Loads dataset (1440 records)
2. Trains ML model with 80/20 train-test split
3. Predicts CO2 emissions for all vessels
4. Calculates GHG intensity per vessel
5. Computes 2026 regulatory compliance benchmark
6. Classifies vessels as Surplus or Deficit
7. Generates `output/compliance_results.json`
8. Creates `output/compliance_summary.txt` report

**Output:** Complete JSON file ready for Task B (Fleet Dashboard)

### Option 2: Run Individual Components

**Train Model Only:**
```bash
python model.py
```

**Calculate Compliance Only:**
```bash
python compliance.py
```

**Explore Data:**
```bash
jupyter notebook exploratory.ipynb
```

## Output Files

### compliance_results.json

Complete JSON file with metadata and all vessel records:

```json
{
  "metadata": {
    "generated_at": "2026-01-09T...",
    "total_records": 1440,
    "model_performance": {
      "test_rmse": 1010.14,
      "test_mae": 625.43,
      "test_r2": 0.9951
    },
    "compliance_summary": {
      "target_year": 2026,
      "fleet_average_intensity": 78.8535,
      "target_intensity": 74.9108,
      "surplus_count": 617,
      "deficit_count": 823
    }
  },
  "vessels": [
    {
      "vessel_id": "NG001",
      "ship_type": "Oil Service Boat",
      "route_id": "Warri-Bonny",
      "month": "January",
      "distance": 132.26,
      "fuel_type": "HFO",
      "fuel_consumption": 3779.77,
      "co2_emission": 10625.76,
      "co2_predicted": 10430.62,
      "ghg_intensity": 80.3399,
      "target_intensity": 74.9108,
      "compliance_balance": -5.4291,
      "status": "Deficit",
      "weather_conditions": "Stormy",
      "engine_efficiency": 92.14
    }
  ]
}
```

### compliance_summary.txt

Human-readable executive summary with key statistics and findings.

## Methodology

### 1. CO2 Prediction Model (model.py)

**Algorithm:** Linear Regression with OneHotEncoding

**Features:**
- `ship_type` (categorical) - Encoded: Fishing Trawler, Oil Service Boat, Surfer Boat, Tanker Ship
- `distance` (numerical) - Distance traveled in kilometers
- `fuel_consumption` (numerical) - Fuel consumed in liters

**Target:** `CO2_emissions` (Kg)

**Training:**
- 80/20 train-test split
- No feature scaling (linear relationships preserved)
- Model coefficients show ~2.73 Kg CO2 per liter fuel (physically accurate)

### 2. GHG Intensity Calculation (compliance.py)

```python
GHG Intensity = CO2 Emission (Kg) / Distance (km)
```

**Units:** kg CO2 per km

**Interpretation:** Lower values indicate better emissions efficiency

**Example:**
- Vessel emits 10,625 Kg CO2 over 132 km
- GHG Intensity = 10,625 / 132 = 80.34 kg/km

### 3. Regulatory Benchmark (2026 Target)

```python
Target Intensity = Fleet Average Intensity × 0.95
```

**Calculation:**
- Fleet Average: 78.85 kg/km (calculated from all 1440 records)
- Reduction Factor: 0.95 (5% reduction required)
- **Target Intensity: 74.91 kg/km**

### 4. Compliance Balance & Classification

```python
Compliance Balance (CB) = Target Intensity - Vessel Intensity
```

**Classification:**
- **CB > 0** → **Surplus** (vessel is compliant, can offset others)
- **CB < 0** → **Deficit** (vessel is non-compliant, needs offsetting)
- **CB = 0** → **Compliant** (exactly at target)

**Example - Surplus:**
- Vessel Intensity: 52.10 kg/km (efficient)
- Target: 74.91 kg/km
- CB = 74.91 - 52.10 = **+22.81 kg/km (Surplus)**

**Example - Deficit:**
- Vessel Intensity: 99.44 kg/km (inefficient)
- Target: 74.91 kg/km
- CB = 74.91 - 99.44 = **-24.53 kg/km (Deficit)**

## Model Performance Metrics

### ✅ Achieved Results

| Metric | Train | Test | Status |
|--------|-------|------|--------|
| **RMSE** | 1,005.62 Kg | 1,010.14 Kg | ✅ Excellent |
| **MAE** | 617.64 Kg | 625.43 Kg | ✅ Excellent |
| **R² Score** | 0.9943 | **0.9951** | ✅ Outstanding |

**Interpretation:**
- **R² = 0.9951** → Model explains 99.51% of variance in CO2 emissions
- Very low overfitting (train ≈ test metrics)
- Average prediction error ~625 Kg on test set
- Fuel consumption coefficient ~2.73 Kg CO2/L (physically accurate)

### Fleet Compliance Results

| Status | Count | Percentage | Total Balance |
|--------|-------|------------|---------------|
| **Surplus** | 617 | 42.8% | +13,358 kg/km |
| **Deficit** | 823 | 57.2% | -19,036 kg/km |
| **Net Position** | - | - | **-5,677 kg/km** |

**Key Findings:**
- 57% of fleet is non-compliant (realistic scenario)
- Fleet has net deficit requiring efficiency improvements
- Pooling can offset some deficits but not all
- Creates business case for Task B (arbitrage dashboard)

## Key Assumptions

### Data Assumptions
- Dataset represents typical Nigerian maritime fleet operations
- Each row = one vessel operation for one month on one route
- All measurements are accurate operational data
- No manual alterations to dataset

### Units & Measurements
- **Distance:** Kilometers (km)
- **Fuel Consumption:** Liters (L)
- **CO2 Emissions:** Kilograms (Kg)
- **Engine Efficiency:** Percentage (%)
- **GHG Intensity:** kg CO2 per km

### Regulatory Assumptions
- **Target Year:** 2026
- **Compliance Benchmark:** 95% of fleet average (5% reduction)
- All vessels subject to same regulatory target
- Linear relationship between features and CO2 emissions

### Model Assumptions
- Ship type significantly affects emissions (categorical encoding needed)
- Fuel consumption is strongest predictor of CO2
- Distance moderates the relationship
- No time-series dependencies assumed

## Files Generated

After running the pipeline:

```
TaskA_Compliance_Engine/
├── model_artifacts.pkl          # Trained model (can be reloaded)
├── output/
│   ├── compliance_results.json  # Main output (for Task B)
│   └── compliance_summary.txt   # Executive summary
```

## Troubleshooting

**Issue:** ModuleNotFoundError
- **Solution:** Run `pip install -r requirements.txt`

**Issue:** FileNotFoundError for dataset
- **Solution:** Ensure you're running from TaskA_Compliance_Engine directory
- Dataset should be at `../data/mindx test dataset.csv`

**Issue:** Model takes long to train
- **Solution:** Normal for 1440 records. Should complete in < 1 minute.

**Issue:** JSON file not generated
- **Solution:** Check terminal for error messages. Ensure `output/` directory exists.

## Next Steps

1. ✅ Task A Complete - ML model and compliance engine operational
2. 🔜 Task B - Use `compliance_results.json` as input for React dashboard
3. 🔜 Task C - Analyze outliers detected during exploration for technical memo

## Technical Notes

- Model uses scikit-learn's LinearRegression (no hyperparameters to tune)
- OneHotEncoding handles 4 ship types automatically
- Handles edge cases (zero distance → NaN GHG intensity)
- JSON output includes both actual and predicted CO2 for transparency
- Pipeline is idempotent (can be run multiple times safely)

