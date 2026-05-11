import pandas as pd
import mysql.connector
import glob

#  MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="keerthi",
    password="1234",   # put password if you set one
    database="telecom_db"
)

cursor = conn.cursor()


files = glob.glob("../data/processed/usage_data/**/*.parquet", recursive=True)

print(" Found parquet files:", len(files))

dfs = []

for f in files:
    df = pd.read_parquet(f)
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)

print("Data loaded:", data.shape)

# Insert into MySQL
batch_size = 10000
rows = []

for _, row in data.iterrows():
    rows.append((
        int(row['cell_id']),
        str(row['datetime']),
        float(row['smsin']),
        float(row['smsout']),
        float(row['callin']),
        float(row['callout']),
        float(row['internet']),
        str(row.get('region_name', 'Unknown')),
        str(row.get('city', 'Unknown'))
    ))

    if len(rows) >= batch_size:
        cursor.executemany("""
            INSERT INTO usage_data (
                cell_id, datetime, smsin, smsout,
                callin, callout, internet,
                region_name, city
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, rows)

        conn.commit()
        rows = []
        print("✅ Inserted batch")

# insert remaining
if rows:
    cursor.executemany(""" 
        INSERT INTO usage_data (
            cell_id, datetime, smsin, smsout,
            callin, callout, internet,
            region_name, city
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, rows)
    conn.commit()

print("✅ Data inserted into MySQL")

conn.commit()

print(" Data inserted into MySQL")

cursor.close()
conn.close()