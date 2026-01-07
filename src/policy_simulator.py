import pandas as pd


def apply_policy_scenarios(
    forecast_df: pd.DataFrame,
    low_factor: float = 0.90,
    medium_factor: float = 0.70,
    high_factor: float = 0.50
) -> pd.DataFrame:
    """
    Simulate government policy interventions on predicted risk scores
    """

    df = forecast_df.copy()

    # Policy scenarios
    df['low_intervention'] = df['predicted_risk_score'] * low_factor
    df['medium_intervention'] = df['predicted_risk_score'] * medium_factor
    df['high_intervention'] = df['predicted_risk_score'] * high_factor

    return df
