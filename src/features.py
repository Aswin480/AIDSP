import pandas as pd


def build_enrolment_features(enrol_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create enrolment-based features and aggregate to state-date level
    """

    # Total enrolment
    enrol_df['total_enrolment'] = (
        enrol_df['age_0_5'] +
        enrol_df['age_5_17'] +
        enrol_df['age_18_greater']
    )

    # Monthly growth (state-wise)
    enrol_df = enrol_df.sort_values(['state', 'date'])
    enrol_df['monthly_growth'] = (
        enrol_df
        .groupby('state')['total_enrolment']
        .pct_change()
    )

    # Age ratios
    enrol_df['child_ratio'] = enrol_df['age_0_5'] / enrol_df['total_enrolment']
    enrol_df['youth_ratio'] = enrol_df['age_5_17'] / enrol_df['total_enrolment']
    enrol_df['adult_ratio'] = enrol_df['age_18_greater'] / enrol_df['total_enrolment']

    # Aggregate to state + date
    enrol_state = (
        enrol_df
        .groupby(['state', 'date'], as_index=False)
        .agg({
            'total_enrolment': 'sum',
            'monthly_growth': 'mean',
            'child_ratio': 'mean',
            'youth_ratio': 'mean',
            'adult_ratio': 'mean'
        })
    )

    return enrol_state


def build_demographic_features(demo_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate demographic update pressure to state-date level
    """

    demo_df['demo_update_pressure'] = (
        demo_df['demo_age_5_17'] +
        demo_df['demo_age_17_']
    )

    demo_state = (
        demo_df
        .groupby(['state', 'date'], as_index=False)
        .agg({
            'demo_update_pressure': 'sum'
        })
    )

    return demo_state


def build_biometric_features(bio_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate biometric update pressure to state-date level
    """

    bio_df['biometric_update_pressure'] = (
        bio_df['bio_age_5_17'] +
        bio_df['bio_age_17_']
    )

    bio_state = (
        bio_df
        .groupby(['state', 'date'], as_index=False)
        .agg({
            'biometric_update_pressure': 'sum'
        })
    )

    return bio_state
