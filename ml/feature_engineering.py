import pandas as pd

def build_features(df):

    #  total usage
    df['total_usage'] = (
        df['call_count'] +
        df['sms_count'] +
        df['internet_mb']
    )

    #  GROUP BY REGION + TIME (VERY IMPORTANT FIX)
    features = df.groupby(['region_id', 'time_id']).agg({
        'call_count': 'sum',
        'sms_count': 'sum',
        'internet_mb': 'sum'
    }).reset_index()

    #  recompute total usage after aggregation
    features['total_usage'] = (
        features['call_count'] +
        features['sms_count'] +
        features['internet_mb']
    )

    # FEATURE ENGINEERING
    features['avg_usage'] = features.groupby('region_id')['total_usage'].transform('mean')

    features['variability'] = features.groupby('region_id')['total_usage'].transform('std')

    features['peak_usage'] = features.groupby('region_id')['total_usage'].transform('max')

    # peak ratio
    features['peak_ratio'] = features['total_usage'] / features['avg_usage']

    #  growth rate (simple diff)
    features['growth_rate'] = (
        features.groupby('region_id')['total_usage']
        .pct_change()
        .fillna(0)
    )

    return features
