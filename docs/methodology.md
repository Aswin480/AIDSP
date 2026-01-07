# Methodology

## Objective

The objective of AIDSP is to transform Aadhaar operational activity data into actionable, explainable, and policy‑relevant intelligence that supports administrative decision‑making.

---

## Data Preparation

### Data Normalization
- All activity metrics are converted to numeric values  
- Missing or invalid entries are handled using defensive defaults  
- Dates are normalized to monthly timestamps  

### Granular Dataset Creation
Data is merged on:
- State
- District
- PIN Code
- Date  

Resulting dataset enables multi‑level drill‑down analysis.

---

## Feature Engineering

At the state‑date level, the following indicators are derived:
- Total enrolments  
- Total biometric corrections  
- Total demographic modifications  

These indicators form the core signals used for risk assessment.

---

## Risk Scoring Approach

### Risk Definition
Operational risk represents the likelihood of administrative stress caused by unusually high or sustained Aadhaar activity.

### Risk Computation
- Historical activity patterns are analyzed  
- Sudden surges and sustained trends increase risk scores  
- Scores are normalized to a 0–1 scale  

---

## Risk Categorization

Risk scores are translated into operational categories:

- Low Risk: Normal operational behavior  
- Moderate Risk: Sustained increase in activity  
- High Risk: Sharp or abnormal operational surges  

This translation ensures interpretability for administrators.

---

## Policy Intervention Simulation

For each state, the system estimates the impact of:
- Low intervention
- Medium intervention
- High intervention  

These estimates allow administrators to compare response strategies before implementation.

---

## Explainability Mechanism

To avoid black‑box decisions:
- Contribution of enrolment, biometric, and demographic activity is calculated  
- Contributions are expressed as percentages  
- The dominant drivers behind each recommendation are clearly displayed  

---

## Confidence Assessment

A confidence indicator is generated based on:
- Volume of data points  
- Coverage across the selected time range  

This prevents over‑interpretation of predictions with limited data.

---

## Methodological Strengths

- Uses real data only  
- Prioritizes interpretability over algorithmic complexity  
- Aligns with administrative decision workflows  
- Avoids overfitting or opaque modeling  

---

## Summary

The methodology balances analytical rigor with administrative clarity, ensuring that predictions, recommendations, and explanations remain trustworthy, understandable, and actionable.
