import pandas as pd
from usage_processor import UsageProcessor

processor = UsageProcessor()
pd.options.display.float_format = '{:,.2f}'.format


# Load multiple files manually
files = [
    "../data/landing/sms-call-internet-mi-2013-11-01.csv",
    "../data/landing/sms-call-internet-mi-2013-11-02.csv",
    "../data/landing/sms-call-internet-mi-2013-11-03.csv"
]

dfs = []

for f in files:
    df = processor.load_data(f)
    dfs.append(df)

# Combine
combined_df = pd.concat(dfs, ignore_index=True)

# Set it back
processor.df = combined_df

processor.clean_data()

print(processor.compute_daily_usage())