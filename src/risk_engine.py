import pandas as pd


def compute_risk_score(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute final Aadhaar operational risk score
    """

    df = features_df.copy()

    # Normalize pressures
    df['demo_pressure_ratio'] = (
        df['demo_update_pressure'] / df['total_enrolment']
    )

    df['biometric_pressure_ratio'] = (
        df['biometric_update_pressure'] / df['total_enrolment']
    )

    # Replace NaN with safe defaults
    df['monthly_growth'] = df['monthly_growth'].fillna(0)
    df['demo_pressure_ratio'] = df['demo_pressure_ratio'].fillna(0)
    df['biometric_pressure_ratio'] = df['biometric_pressure_ratio'].fillna(0)

    # Composite risk score (weighted & explainable)
    df['risk_score'] = (
        df['monthly_growth'].abs() * 0.4 +
        df['demo_pressure_ratio'] * 0.3 +
        df['biometric_pressure_ratio'] * 0.3
    )

    return df
