import joblib
import numpy as np

# Load model once
model = joblib.load("ml/model.pkl")

def predict_usage_risk(features: dict):

    try:
        X = np.array([[ 
            features["avg_usage"],
            features["growth_rate"],
            features["peak_ratio"],  
            features["variability"]
        ]])

        pred = model.predict(X)[0]
        prob = model.predict_proba(X).max()

        label_map = {
            0: "LOW",
            1: "MEDIUM",
            2: "HIGH"
        }

        return {
            "congestion_risk": label_map[pred],
            "anomaly_flag": prob > 0.8,
            "score": float(prob)
        }

    except Exception as e:
        return {
            "error": str(e)
        }