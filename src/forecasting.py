import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_state_risk(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Forecast next-period Aadhaar risk score for each state
    using explainable linear regression
    """

    df = features_df.copy()
    df = df.sort_values(['state', 'date'])

    # Create time index per state
    df['time_index'] = (
        df
        .groupby('state')
        .cumcount()
    )

    predictions = []

    for state, state_df in df.groupby('state'):
        # Require minimum history
        if len(state_df) < 6:
            continue

        X = state_df[['time_index']]
        y = state_df['risk_score']

        model = LinearRegression()
        model.fit(X, y)

        # Predict next time step
        next_time = state_df['time_index'].max() + 1
        predicted_risk = model.predict(
    pd.DataFrame({'time_index': [next_time]})
)[0]


        predictions.append({
            'state': state,
            'predicted_risk_score': predicted_risk
        })

    forecast_df = pd.DataFrame(predictions)

    forecast_df = forecast_df.sort_values(
        'predicted_risk_score',
        ascending=False
    )

    return forecast_df
