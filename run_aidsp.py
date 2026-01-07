from pathlib import Path
import pandas as pd

from src.data_loader import (
    load_enrolment_data,
    load_demographic_data,
    load_biometric_data
)

from src.features import (
    build_enrolment_features,
    build_demographic_features,
    build_biometric_features
)

from src.risk_engine import compute_risk_score
from src.forecasting import forecast_state_risk
from src.policy_simulator import apply_policy_scenarios
from src.stress_genome import compute_stress_genome, assign_archetypes


BASE_DIR = Path(__file__).resolve().parent


def main():
    print(" Starting AIDSP Pipeline")

    # ==================================================
    # 1️ LOAD RAW DATA
    # ==================================================
    enrol = load_enrolment_data()
    demo = load_demographic_data()
    bio = load_biometric_data()

    # Ensure date is datetime everywhere
    enrol["date"] = pd.to_datetime(enrol["date"], errors="coerce")
    demo["date"] = pd.to_datetime(demo["date"], errors="coerce")
    bio["date"] = pd.to_datetime(bio["date"], errors="coerce")

    # ==================================================
    # 2️ CREATE GRANULAR DATASET (GUARANTEED)
    # ==================================================
    print(" Creating granular UIDAI dataset")

    granular = enrol.merge(
        demo,
        on=["state", "district", "pincode", "date"],
        how="left",
        suffixes=("", "_demo")
    )

    granular = granular.merge(
        bio,
        on=["state", "district", "pincode", "date"],
        how="left",
        suffixes=("", "_bio")
    )

    # Normalize column names (VERY IMPORTANT)
    granular = granular.rename(columns={
        "enrolment_count": "enrolment",
        "biometric_count": "biometric",
        "demographic_count": "demographic"
    })

    # If columns already exist, keep them
    required_cols = [
        "state", "district", "pincode", "date",
        "enrolment", "biometric", "demographic"
    ]

    for col in ["enrolment", "biometric", "demographic"]:
        if col not in granular.columns:
            granular[col] = 0

    granular = granular[required_cols]

    # Clean invalid states
    granular["state"] = granular["state"].astype(str).str.strip()
    granular = granular[~granular["state"].str.isnumeric()]
    granular = granular[granular["state"].str.len() > 3]

    processed_dir = BASE_DIR / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    granular_path = processed_dir / "granular_uidai.csv"
    granular.to_csv(granular_path, index=False)

    print(f" Granular UIDAI saved → {granular_path}")

    # ==================================================
    # 3️ FEATURE ENGINEERING (STATE LEVEL)
    # ==================================================
    enrol_f = build_enrolment_features(enrol)
    demo_f = build_demographic_features(demo)
    bio_f = build_biometric_features(bio)

    # ==================================================
    # 4️ MERGE FEATURES
    # ==================================================
    features = enrol_f.merge(demo_f, on=["state", "date"], how="left")
    features = features.merge(bio_f, on=["state", "date"], how="left")

    features["state"] = features["state"].astype(str).str.strip()
    features = features[~features["state"].str.isnumeric()]
    features = features[features["state"].str.len() > 3]

    # ==================================================
    #  AGGREGATE TO STATE–DATE LEVEL
    # ==================================================
    numeric_cols = features.select_dtypes(include="number").columns

    features = (
        features
        .groupby(["state", "date"], as_index=False)[numeric_cols]
        .sum()
    )

    print(f" Valid states after cleaning: {features['state'].nunique()}")

    features.to_csv(
        processed_dir / "feature_dataset.csv",
        index=False
    )

    # ==================================================
    # 5️ RISK SCORING
    # ==================================================
    # Save feature dataset WITH risk for trend analysis
    # Save date-wise risk for trend analysis (REAL DATA)
    features.to_csv(
    processed_dir / "feature_dataset.csv",
    index=False
)


    # ==================================================
    # 6️ FORECASTING
    # ==================================================
    forecast = forecast_state_risk(features)

    # ==================================================
    # 7️ POLICY SIMULATION
    # ==================================================
    policy_output = apply_policy_scenarios(forecast)

    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)

    policy_output.to_csv(
        results_dir / "final_policy_output.csv",
        index=False
    )

    # ==================================================
    # 8️ STRESS GENOME
    # ==================================================
    genome = compute_stress_genome(features)
    genome = assign_archetypes(genome)

    genome.to_csv(
        results_dir / "stress_genome_output.csv",
        index=False
    )

    print( Stress Genome saved")
    print(" AIDSP Pipeline Completed Successfully")


if __name__ == "__main__":
    main()
