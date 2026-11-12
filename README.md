# Shipment Route Optimization Under Cost, Time, and Risk Constraints

## Project Overview

This project develops a shipment route optimization system that evaluates multiple candidate routes and recommends the most suitable route based on shipping cost, transit time, delay probability, congestion risk, and geopolitical risk.

The system uses a weighted multi-criteria scoring algorithm to rank candidate routes under different business priorities. An interactive Streamlit dashboard allows users to compare Balanced, Cost-focused, and Time-focused scenarios.

## Objectives

- Generate and analyze shipment route data.
- Evaluate multiple route alternatives for each shipment.
- Optimize route selection based on cost, time, and risk.
- Compare recommendations under different business scenarios.
- Perform sensitivity analysis to understand changes in route selection.
- Display results through an interactive dashboard.

## Technology Stack

- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn
- **Optimization:** Weighted Multi-Criteria Scoring
- **Dashboard:** Streamlit

## Dataset

The project uses a synthetic dataset containing:

- 30 shipments
- 4 candidate routes per shipment
- 120 route records in total

Each route includes:
- Shipment ID
- Origin and destination
- Route ID and route profile
- Intermediate hub
- Shipping cost
- Transit time
- Delay probability
- Congestion risk
- Geopolitical risk

Four route profiles are simulated: Economy, Express, Balanced, and Risky.

## Methodology

### 1. Data Generation
Generated synthetic shipment and route records using Python with predefined route-profile characteristics.

### 2. Exploratory Data Analysis
Analyzed distributions, missing values, duplicate records, and relationships between numerical features.

### 3. Data Preprocessing
Applied Min-Max normalization separately within each shipment to scale the five optimization criteria between 0 and 1.

### 4. Route Optimization

Used a weighted scoring algorithm to calculate a score for each candidate route.

**Balanced scenario weights:**

| Criterion | Weight |
|---|---:|
| Cost | 0.35 |
| Transit Time | 0.25 |
| Delay Probability | 0.20 |
| Congestion Risk | 0.10 |
| Geopolitical Risk | 0.10 |

The route with the lowest weighted score is selected as the recommended route for each shipment.

### 5. Scenario Evaluation

Three optimization scenarios are implemented:

- **Balanced:** Considers all five criteria with balanced priorities.
- **Cost-focused:** Gives greater importance to minimizing shipping costs.
- **Time-focused:** Gives greater importance to minimizing transit time.

### 6. Sensitivity Analysis

Evaluates how changing criterion weights affects route recommendations.

## Results

| Scenario | Average Cost | Average Transit Time |
|---|---:|---:|
| Balanced | ₹64,647.57 | 20.13 days |
| Cost-focused | ₹47,814.93 | 29.30 days |
| Time-focused | ₹76,985.70 | 15.17 days |

Sensitivity analysis showed:
- Cost-focused recommendations changed for 23 out of 30 shipments.
- Time-focused recommendations changed for 17 out of 30 shipments.

## Interactive Dashboard

The Streamlit dashboard provides:
- Scenario selection
- Average shipping cost and transit time
- Recommended routes for each shipment
- Route profile distribution charts
- Scenario comparison

## Project Structure

```text
shipment-route-optimization/
│
├── data/
│   ├── shipments.csv
│   └── processed_shipments.csv
│
├── src/
│   ├── data_generator.py
│   ├── eda.py
│   ├── preprocessing.py
│   ├── route_optimizer.py
│   └── evaluation.py
│
├── outputs/
│   ├── route_recommendations.csv
│   ├── route_scores.csv
│   ├── scenario_recommendations.csv
│   ├── profile_comparison.csv
│   └── visualizations
│
├── reports/
│   └── technical_report.pdf
│
├── notebooks/
├── app.py
├── requirements.txt
└── README.md
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd shipment-route-optimization
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Streamlit dashboard

```bash
python -m streamlit run app.py
```

## Assumptions and Limitations

- The project uses synthetic data generated for demonstration and evaluation.
- Intermediate hubs have not been validated against actual logistics networks or geographical connectivity.
- Cost, transit time, and risk values are simulated rather than real-world operational measurements.
- Route recommendations depend on the selected optimization weights.

## Future Enhancements

- Integrate real logistics and carrier data.
- Use geographical routing and verified transport connections.
- Incorporate live traffic and geopolitical risk information.
- Apply machine learning to predict transit times and delay probabilities using historical data.
- Add operational constraints such as delivery deadlines and transport capacity.

## Technical Report

The detailed technical report is available in the `reports/technical_report.pdf` folder.

---

**Project:** Shipment Route Optimization Under Cost, Time, and Risk Constraints  
**Assignment:** Aiqon AI Internship Take-Home Technical Assignment