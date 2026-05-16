import pandas as pd
import mysql.connector
import glob

# -----------------------------
# CONNECT DB
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="keerthi",
    password="1234",
    database="telecom_db"  
)

cursor = conn.cursor()

# -----------------------------
# LOAD PARQUET
# -----------------------------
files = glob.glob("data/processed/usage_data/**/*.parquet", recursive=True)

dfs = [pd.read_parquet(f) for f in files]
data = pd.concat(dfs, ignore_index=True)

print("========== ORIGINAL DATA ==========")
print(f"Total rows read: {len(data)}")

# -----------------------------
#  CHECK REGION DISTRIBUTION (BEFORE SAMPLING)
# -----------------------------
print("\n========== REGION DISTRIBUTION (BEFORE) ==========")
print(data['region_name'].value_counts())

# -----------------------------
#  CLEAN DATA
# -----------------------------
data['region_name'] = data['region_name'].astype(str).str.strip()
data['city'] = data['city'].astype(str).str.strip()

data['datetime'] = pd.to_datetime(data['datetime'])
data['date'] = data['datetime'].dt.date
data['hour'] = data['datetime'].dt.hour

# -----------------------------
#  BALANCED SAMPLING (IMPORTANT)
# -----------------------------
print("\n========== SAMPLING ==========")

sample_per_region = 200000   # 200k × 4 = 800k total

samples = []

for region in ["North", "South", "East", "West"]:
    region_df = data[data['region_name'] == region]

    region_sample = region_df.sample(
        n=min(sample_per_region, len(region_df)),
        random_state=42
    )

    samples.append(region_sample)

# Combine all regions
data = pd.concat(samples, ignore_index=True)

print(f" Final sampled rows: {len(data)}")

# -----------------------------
#  CHECK AFTER SAMPLING
# -----------------------------
print("\n========== REGION DISTRIBUTION (AFTER) ==========")
print(data['region_name'].value_counts())

# -----------------------------
# DIM_TIME
# -----------------------------
print("\n========== DIM_TIME LOAD ==========")

dim_time = data[['date', 'hour']].drop_duplicates().copy()

dim_time['day'] = pd.to_datetime(dim_time['date']).dt.day
dim_time['month'] = pd.to_datetime(dim_time['date']).dt.month
dim_time['weekday'] = pd.to_datetime(dim_time['date']).dt.day_name()

time_map = {}

for _, row in dim_time.iterrows():
    cursor.execute("""
        INSERT INTO dim_time (date, hour, day, month, weekday)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE time_id=LAST_INSERT_ID(time_id)
    """, tuple(row))

    time_id = cursor.lastrowid
    time_map[(row['date'], row['hour'])] = time_id

conn.commit()
print(f" dim_time loaded: {len(time_map)} rows")

# -----------------------------
# DIM_REGION
# -----------------------------
print("\n========== DIM_REGION LOAD ==========")

dim_region = data[['region_name', 'city']].drop_duplicates()

region_map = {}

for _, row in dim_region.iterrows():
    cursor.execute("""
        INSERT INTO dim_region (region_name, city)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE region_id=LAST_INSERT_ID(region_id)
    """, tuple(row))

    region_id = cursor.lastrowid
    region_map[(row['region_name'], row['city'])] = region_id

conn.commit()
print(f" dim_region loaded: {len(region_map)} rows")

# -----------------------------
# FACT TABLE
# -----------------------------
print("\n========== FACT LOAD START ==========")

batch_size = 50000
rows = []
inserted = 0
skipped = 0

for i, row in enumerate(data.itertuples(index=False), start=1):

    time_id = time_map.get((row.date, row.hour))
    region_id = region_map.get((row.region_name, row.city))

    if time_id is None or region_id is None:
        skipped += 1
        continue

    rows.append((
        time_id,
        region_id,
        int((row.callin or 0) + (row.callout or 0)),
        int((row.smsin or 0) + (row.smsout or 0)),
        float(row.internet or 0)
    ))

    if len(rows) >= batch_size:
        cursor.executemany("""
            INSERT INTO fact_usage
            (time_id, region_id, call_count, sms_count, internet_mb)
            VALUES (%s, %s, %s, %s, %s)
        """, rows)

        conn.commit()

        inserted += len(rows)
        print(f" Inserted: {inserted}")
        rows.clear()

    if i % 50000 == 0:
        print(f"Processed: {i}")

#  FINAL INSERT
if rows:
    cursor.executemany("""
        INSERT INTO fact_usage
        (time_id, region_id, call_count, sms_count, internet_mb)
        VALUES (%s, %s, %s, %s, %s)
    """, rows)

    conn.commit()
    inserted += len(rows)

# -----------------------------
# FINAL LOG
# -----------------------------
print("\n========== FINAL SUMMARY ==========")
print(f"Total rows loaded : {len(data)}")
print(f"Inserted rows     : {inserted}")
print(f"Skipped rows      : {skipped}")

cursor.close()
conn.close()