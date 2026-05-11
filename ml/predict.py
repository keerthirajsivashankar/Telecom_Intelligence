import joblib
import numpy as np

model = joblib.load("ml/model.pkl")

def predict_usage_risk(features: dict):

    #  compute peak_ratio automatically
    avg = features["avg_usage"]

    # simple assumption (can improve later)
    peak_usage = avg * 1.2  

    peak_ratio = peak_usage / avg

    X = np.array([[
        features["avg_usage"],
        features["growth_rate"],
        peak_ratio,   
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