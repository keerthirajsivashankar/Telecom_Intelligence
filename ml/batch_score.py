import pandas as pd
import mysql.connector
from feature_engineering import build_features
from predict import predict_usage_risk

# -------------------
# DB CONNECTION
# -------------------
conn = mysql.connector.connect(
    host="localhost",
    user="keerthi",
    password="1234",
    database="telecom_db"
)

# -------------------
# LOAD DATA
# -------------------
print("Loading data from DB...")
df = pd.read_sql("SELECT * FROM fact_usage", conn)

# -------------------
# BUILD FEATURES
# -------------------
features = build_features(df)

print(f" Total regions: {len(features)}")

# -------------------
# PREDICTIONS
# -------------------
results = []

print("Running batch predictions...")

for _, row in features.iterrows():

    feature_input = {
        "avg_usage": float(row["avg_usage"]),
        "growth_rate": float(row["growth_rate"]),
        "variability": float(row["variability"]),
        "peak_ratio": float(row["peak_ratio"])
    }

    pred = predict_usage_risk(feature_input)

    results.append({
        "region_id": row["region_id"],
        "congestion_risk": pred["congestion_risk"],
        "anomaly_flag": pred["anomaly_flag"],
        "score": pred["score"]
    })

# -------------------
# SAVE OUTPUT
# -------------------
output = pd.DataFrame(results)

output.to_csv("ml/batch_predictions.csv", index=False)

print("\nBatch predictions saved to ml/batch_predictions.csv")
