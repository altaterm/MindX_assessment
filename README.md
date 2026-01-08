# MindX Strategic Navigator Challenge

Maritime fleet compliance management system with ML-powered CO2 prediction, interactive dashboard, and technical analysis.

## Project Overview

**Three integrated tasks:**
1. **Task A:** ML Compliance Engine (Python)
2. **Task B:** Fleet Dashboard (React)
3. **Task C:** Technical Memo (PDF)

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Task A: Compliance Engine (Python)

```bash
cd TaskA_Compliance_Engine
pip install -r requirements.txt
python run_pipeline.py
```

**Output:** `output/compliance_results.json` (1440 vessel records with compliance metrics)

### Task B: Fleet Dashboard (React)

```bash
cd TaskB_Fleet_Dashboard
cp ../TaskA_Compliance_Engine/output/compliance_results.json public/
npm install
npm start
```

**Access:** http://localhost:3000

### Task C: Technical Memo

See `TaskC_Technical_Memo/MindX_Technical_Memo.pdf`

---

## ML Model Performance Summary

**Algorithm:** Linear Regression with OneHotEncoding  
**Dataset:** 1,440 vessel operations (Nigerian maritime fleet)  
**Features:** Ship type (categorical), distance, fuel consumption  
**Target:** CO2 emissions (kg)

### Performance Metrics

| Metric | Train | Test | Status |
|--------|-------|------|--------|
| **RMSE** | 1,006 kg | 1,010 kg | ✅ Excellent |
| **MAE** | 618 kg | 625 kg | ✅ Excellent |
| **R²** | 0.9943 | **0.9951** | ✅ Outstanding |

**Key Insight:** Model explains 99.51% of variance in CO2 emissions. Fuel consumption coefficient ~2.73 kg CO2/L (physically accurate).

### Fleet Compliance Results

| Status | Count | % | Balance |
|--------|-------|---|---------|
| Surplus | 617 | 42.8% | +13,358 kg/km |
| Deficit | 823 | 57.2% | -19,036 kg/km |
| **Net** | 1,440 | 100% | **-5,677 kg/km** |

**Target:** 74.91 kg/km (5% reduction from fleet average of 78.85 kg/km)

---

## Task Summaries

### Task A: Compliance Engine
- **Input:** CSV dataset (1,440 records)
- **Process:** ML prediction → GHG calculation → Compliance classification
- **Output:** JSON with vessel-level compliance metrics
- **Key Files:** `model.py`, `compliance.py`, `run_pipeline.py`

### Task B: Fleet Dashboard
- **Technology:** React 18 with responsive CSS
- **Features:** Fleet overview, liability map (filterable/sortable), pooling simulator
- **Pooling Logic:** `Net = Surplus + Deficit` (deterministic)
- **Key Files:** `App.js`, `FleetOverview.js`, `LiabilityMap.js`, `PoolingSimulator.js`

### Task C: Technical Memo
- **Anomaly:** Vessel NG077 (23.8% excess fuel consumption)
- **Root Cause:** Hull biofouling (marine growth)
- **Physics:** Hydrodynamic resistance equation validates 24% fuel increase
- **Recommendation:** Hull cleaning (ROI: 2-3 months)

---

## Key Assumptions

- Distance: kilometers
- CO2 emissions: kilograms
- Fuel consumption: liters
- GHG Intensity = CO2 / Distance
- 2026 Target = Fleet Average × 0.95
- Compliance Balance = Target - Vessel Intensity

---

## Technologies

**Backend:** Python, pandas, numpy, scikit-learn, jupyter  
**Frontend:** React 18, CSS Grid/Flexbox  
**Data:** CSV → JSON pipeline

---

## Deliverables

✅ Task A: ML model + compliance engine  
✅ Task B: Interactive React dashboard  
✅ Task C: Technical memo (PDF)  
✅ Documentation: README files for each task  
✅ Output: `compliance_results.json` (ready for dashboard)

---


