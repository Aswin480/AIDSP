import pandas as pd
import numpy as np


def compute_stress_genome(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Aadhaar Stress Genome for each state
    """

    df = features_df.copy()

    genome_rows = []

    for state, sdf in df.groupby("state"):
        # Sort by time
        sdf = sdf.sort_values("date")

        # 1. Growth Volatility (std of growth)
        growth_volatility = sdf["monthly_growth"].std()

        # 2. Update Burden (mean pressure)
        update_burden = (
            sdf["demo_update_pressure"].mean() +
            sdf["biometric_update_pressure"].mean()
        )

        # 3. Age Pressure (youth dominance)
        age_pressure = sdf["youth_ratio"].mean()

        # 4. Recovery Speed (how fast risk drops)
        risk_diff = sdf["risk_score"].diff().abs()
        recovery_speed = 1 / (risk_diff.mean() + 1e-6)

        genome_rows.append({
            "state": state,
            "growth_volatility": growth_volatility,
            "update_burden": update_burden,
            "age_pressure": age_pressure,
            "recovery_speed": recovery_speed
        })

    genome_df = pd.DataFrame(genome_rows)

    # Normalize all genome dimensions (0–1)
    for col in genome_df.columns:
        if col != "state":
            min_v = genome_df[col].min()
            max_v = genome_df[col].max()
            genome_df[col] = (genome_df[col] - min_v) / (max_v - min_v + 1e-6)

    return genome_df
def assign_archetypes(genome_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign behavioral archetypes to states based on stress genome
    """

    df = genome_df.copy()

    def classify(row):
        if row["growth_volatility"] > 0.6 and row["recovery_speed"] < 0.4:
            return "Volatile Grower"
        elif row["update_burden"] > 0.6 and row["recovery_speed"] < 0.4:
            return "Structurally Burdened"
        elif row["update_burden"] > 0.6 and row["recovery_speed"] >= 0.6:
            return "Resilient High-Load"
        else:
            return "Stable Low-Risk"

    df["archetype"] = df.apply(classify, axis=1)

    return df
