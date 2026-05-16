import pandas as pd

def build_features(df):

    # total usage
    df['total_usage'] = (
        df['call_count'] +
        df['sms_count'] +
        df['internet_mb']
    )

    # GROUP BY REGION + HOUR (BALANCE FIX)
    features = df.groupby(['region_id', 'time_id']).agg({
        'total_usage': 'sum'
    }).reset_index()

    #  region level stats (applied to each row)
    features['avg_usage'] = features.groupby('region_id')['total_usage'].transform('mean')

    features['variability'] = features.groupby('region_id')['total_usage'].transform('std')

    features['peak_usage'] = features.groupby('region_id')['total_usage'].transform('max')

    #  peak ratio
    features['peak_ratio'] = features['total_usage'] / features['avg_usage']

    #  growth rate (time-based now meaningful)
    features['growth_rate'] = (
        features.groupby('region_id')['total_usage']
        .pct_change()
        .fillna(0)
    )

    return features