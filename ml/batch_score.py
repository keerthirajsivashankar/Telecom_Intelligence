import pandas as pd
import mysql.connector
from feature_engineering import build_features
from predict import predict_usage_risk

#  DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="keerthi",
    password="1234",
    database="telecom_db"
)

# Load fact data
df = pd.read_sql("SELECT * FROM fact_usage", conn)

# Build features (same as training)
features = build_features(df)

results = []

print(" Running batch predictions...")

#  Loop through each row (region + time level now)
for _, row in features.iterrows():

    feature_input = {
        "avg_usage": float(row["avg_usage"]),
        "growth_rate": float(row["growth_rate"]),
        "variability": float(row["variability"]),
        # ❗ peak_ratio is NOT passed (computed in predict.py)
    }

    pred = predict_usage_risk(feature_input)

    results.append({
        "region_id": row["region_id"],
        "time_id": row["time_id"],
        "congestion_risk": pred["congestion_risk"],
        "anomaly_flag": pred["anomaly_flag"],
        "score": pred["score"]
    })

#  Convert to dataframe
output = pd.DataFrame(results)

#  Save output
output.to_csv("ml/batch_predictions.csv", index=False)

print(" Batch predictions saved to ml/batch_predictions.csv")
