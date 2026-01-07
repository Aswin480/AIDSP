# System Architecture

## Overview

The Aadhaar Intelligence & Decision Support Platform (AIDSP) follows a modular, pipeline‑driven architecture designed for scalability, transparency, and administrative reliability.  
The system separates data ingestion, analytics, risk intelligence, and presentation layers to ensure maintainability and auditability.

---

## High‑Level Architecture

The platform consists of four logical layers:

1. Data Layer  
2. Analytics & Intelligence Layer  
3. Decision & Policy Layer  
4. Presentation Layer  

Each layer operates independently while exchanging clearly defined outputs.

---

## 1. Data Layer

### Input Sources
- Aadhaar enrolment activity data  
- Biometric update records  
- Demographic modification records  

### Granularity
- State  
- District  
- PIN Code  
- Time (monthly aggregation)

### Output
- `granular_uidai.csv`  
A normalized dataset used for drill‑down analysis and dashboards.

---

## 2. Analytics & Intelligence Layer

### Feature Engineering
- Aggregation of enrolment, biometric, and demographic activity  
- State‑date level feature construction  
- Data validation and cleansing  

### Risk Scoring Engine
- Computes predicted operational risk at the state level  
- Uses historical activity trends and feature interactions  
- Outputs a continuous risk score between 0 and 1  

### Output
- `feature_dataset.csv`  
- State‑level risk indicators

---

## 3. Decision & Policy Layer

### Risk Interpretation
- Converts numeric risk scores into interpretable risk categories:
  - Low
  - Moderate
  - High  

### Policy Simulation
- Simulates the impact of:
  - Low Intervention
  - Medium Intervention
  - High Intervention  

### Output
- `final_policy_output.csv`  
Contains predicted risk scores and intervention impact estimates.

---

## 4. Presentation Layer

### Dashboard
- Built using Streamlit  
- Administrative control panel for:
  - State selection
  - Date range filtering
  - View selection  

### Intelligence Views
- State Intelligence (strategic)
- District Drill‑Down (diagnostic)
- PIN‑level Analysis (operational)

### Explainability
- “Why this recommendation?” driver analysis  
- Confidence indicator based on data volume  

---

## Design Principles

- Modular separation of concerns  
- Explainable, non‑black‑box decisions  
- Defensive handling of missing or sparse data  
- Government‑appropriate simplicity  

---

## Scalability Considerations

- Can be extended to real‑time or near‑real‑time ingestion  
- Compatible with API‑based data sources  
- Architecture supports integration with official monitoring systems  

---

## Summary

The AIDSP architecture ensures that predictive analytics, decision logic, and visualization remain clearly separated, enabling transparent, auditable, and scalable administrative decision support.
