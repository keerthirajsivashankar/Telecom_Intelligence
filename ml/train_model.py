import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

from feature_engineering import build_features
import mysql.connector

#  DB load
conn = mysql.connector.connect(
    host="localhost",
    user="keerthi",
    password="1234",
    database="telecom_db"
)

df = pd.read_sql("SELECT * FROM fact_usage", conn)

# build features
features = build_features(df)

#  create labels (IMPORTANT)
threshold_high = features['avg_usage'].quantile(0.9)
threshold_med = features['avg_usage'].quantile(0.6)

def label(x):
    if x > threshold_high:
        return 2  # HIGH
    elif x > threshold_med:
        return 1  # MEDIUM
    else:
        return 0  # LOW

features['label'] = features['avg_usage'].apply(label)

#  model data
X = features[['avg_usage', 'growth_rate', 'peak_ratio', 'variability']]
y = features['label']

#  split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#  model
model = RandomForestClassifier()
model.fit(X_train, y_train)

#  evaluation
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

#  save model
joblib.dump(model, "model.pkl")

print(" Model saved")
