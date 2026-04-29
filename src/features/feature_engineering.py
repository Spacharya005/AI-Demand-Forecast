import pandas as pd

def preprocess_data(df):
    df = df.copy()

    # Convert to datetime
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Extract time-based features
    df['hour'] = df['datetime'].dt.hour
    df['day'] = df['datetime'].dt.day
    df['month'] = df['datetime'].dt.month
    df['day_of_week'] = df['datetime'].dt.dayofweek

    # Sort data (important for time series)
    df = df.sort_values('datetime')

    return df