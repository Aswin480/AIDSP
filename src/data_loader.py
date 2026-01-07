import pandas as pd
from pathlib import Path

# Base project path
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PROCESSED = BASE_DIR / "data" / "processed"


def load_enrolment_data():
    """
    Load cleaned Aadhaar enrolment data
    """
    path = DATA_PROCESSED / "enrolment_clean.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def load_demographic_data():
    """
    Load cleaned Aadhaar demographic update data
    """
    path = DATA_PROCESSED / "demographic_clean.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def load_biometric_data():
    """
    Load cleaned Aadhaar biometric update data
    """
    path = DATA_PROCESSED / "biometric_clean.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def load_feature_dataset():
    """
    Load final engineered feature dataset
    """
    path = DATA_PROCESSED / "feature_dataset.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    return df
