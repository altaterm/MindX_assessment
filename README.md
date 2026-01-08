# MindX Strategic Navigator Challenge

> A comprehensive maritime compliance and fleet optimization system developed for the MindX AI Intern Technical Assessment.

---

## 📋 Project Overview

This project implements a three-part solution for maritime fleet compliance management:

1. **Task A: Compliance Engine** - ML-powered CO2 emissions prediction and GHG compliance analysis
2. **Task B: Fleet Arbitrage Dashboard** - Interactive React dashboard for fleet compliance visualization and pooling simulation
3. **Task C: Technical Memo** - Deep analysis of dataset anomalies with maritime engineering insights

---

## 🏗️ Repository Structure

```
MindX_assessment/
│
├── data/
│   └── mindx test dataset.csv        # Source dataset
│
├── TaskA_Compliance_Engine/
│   ├── exploratory.ipynb              # Data exploration and analysis
│   ├── model.py                       # ML model implementation
│   ├── compliance.py                  # Compliance calculation logic
│   ├── run_pipeline.py                # End-to-end pipeline orchestration
│   ├── output/
│   │   └── compliance_results.json    # Generated compliance results
│   └── requirements.txt               # Python dependencies
│
├── TaskB_Fleet_Dashboard/
│   ├── src/                          # React source code
│   ├── public/                       # Static assets
│   ├── package.json                  # Node dependencies
│   └── README.md                     # Dashboard documentation
│
├── TaskC_Technical_Memo/
│   └── MindX_Technical_Memo.pdf      # Technical analysis memo
│
└── README.md                         # This file
```

---

## 🚀 Quick Start

### Task A: Compliance Engine

```bash
cd TaskA_Compliance_Engine
pip install -r requirements.txt
python run_pipeline.py
```

### Task B: Fleet Dashboard

```bash
cd TaskB_Fleet_Dashboard
npm install
npm start
```

### Task C: Technical Memo

See `TaskC_Technical_Memo/MindX_Technical_Memo.pdf`

---

## 📊 Task A: Compliance Engine

### Overview
Machine learning system that predicts CO2 emissions and calculates vessel compliance with 2026 GHG intensity regulations.

### Key Features
- Linear Regression model for CO2 prediction
- GHG intensity calculation per vessel
- Regulatory benchmark computation (95% of fleet average)
- Compliance balance classification (Surplus/Deficit)

### Assumptions
- GHG Intensity Formula: `CO2 Emission (Kg) / Distance (km)`
- 2026 Target: `Fleet Average Intensity × 0.95`
- Compliance Balance: `Target Intensity - Vessel Intensity`

### ML Performance Metrics
*Will be updated after model training*

---

## 🎨 Task B: Fleet Arbitrage Dashboard

### Overview
Interactive React-based dashboard for visualizing fleet compliance and simulating pooling strategies.

### Features
1. **Fleet Overview**: Total vessels, surplus count, deficit count
2. **Liability Map**: Color-coded vessel compliance status
3. **Pooling Simulator**: Interactive tool to offset deficits with surplus vessels

### Pooling Logic
```
Net Balance = CB_surplus + CB_deficit

If Net Balance ≥ 0: Compliance achieved
If Net Balance < 0: Remaining deficit shown
```

---

## 📝 Task C: Technical Memo

Deep analysis of one dataset anomaly with:
- Statistical anomaly detection
- Physical maritime engineering explanation
- Compliance impact assessment
- Actionable recommendations

---

## 🔧 Technologies Used

**Task A:**
- Python 3.x
- pandas, numpy
- scikit-learn
- jupyter

**Task B:**
- React 18+
- Modern CSS (responsive design)
- Chart.js / D3.js (for visualizations)

---

## 📖 Key Assumptions

1. All calculations use the same unmodified dataset
2. Distance is measured in kilometers
3. CO2 emissions are in kilograms
4. Fuel consumption is in liters
5. Target year for compliance: 2026
6. Regulatory reduction target: 5% below fleet average

---

## 👨‍💻 Development Notes

- Tasks are implemented independently but may share computed outputs
- Code prioritizes clarity and explainability
- All assumptions documented in code comments
- Deterministic results - no random seeds without documentation

---

## 📦 Deliverables

- ✅ Complete source code for all three tasks
- ✅ Generated `compliance_results.json`
- ✅ Interactive dashboard
- ✅ Technical memo PDF
- ✅ Comprehensive documentation

---

## 🎥 Project Walkthrough

*Link to 3-minute video walkthrough will be added here*

---

## 📄 License

This project is submitted as part of the MindX AI Intern Technical Assessment.

---


