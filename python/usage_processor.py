import pandas as pd

class UsageProcessor:
    def __init__(self):
        self.df = None

    def load_data(self, path):
        self.df = pd.read_csv(path)

        # convert datetime
        self.df['datetime'] = pd.to_datetime(self.df['datetime'], errors='coerce')

        # fill NaNs
        cols = ['smsin', 'smsout', 'callin', 'callout', 'internet']
        self.df[cols] = self.df[cols].fillna(0)

        return self.df

    def clean_data(self):
        df = self.df.copy()

        # extract time features
        df['hour'] = df['datetime'].dt.hour
        df['day'] = df['datetime'].dt.day

        # remove negative usage
        cols = ['smsin', 'smsout', 'callin', 'callout', 'internet']
        for col in cols:
            df = df[df[col] >= 0]

        # (optional safety)
        df = df.dropna(subset=['datetime'])

        self.df = df
        return df
    
    def compute_daily_usage(self):

        df = self.df

        daily = df.groupby('day')[[
            'smsin', 'smsout', 'callin', 'callout', 'internet'
        ]].sum()

        return daily
    
    def compute_kpis(self):

        df = self.df

        # total usage column
        df['total_usage'] = (
            df['smsin'] + df['smsout'] +
            df['callin'] + df['callout'] +
            df['internet']
        )

        kpis = {}

        # usage per region
        kpis['usage_per_region'] = df.groupby('CellID')['total_usage'].sum()

        # avg per hour
        kpis['avg_usage_per_hour'] = df.groupby('hour')['total_usage'].mean()

        # peak hour
        kpis['peak_hour'] = df.groupby('hour')['total_usage'].sum().idxmax()

        return kpis
    
    def call_plan_api(customer_id):
        return {
        "customer_id": customer_id,
        "plan": "Premium",
        "data_limit": "100GB"
        }