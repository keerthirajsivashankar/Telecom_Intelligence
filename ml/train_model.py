import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

from feature_engineering import build_features

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
print("Loading data...")
df = pd.read_sql("SELECT * FROM fact_usage", conn)

# -------------------
# FEATURE ENGINEERING
# -------------------
features = build_features(df)

# -------------------
# LABEL CREATION
# -------------------
threshold_high = features['avg_usage'].quantile(0.75)
threshold_med = features['avg_usage'].quantile(0.5)

def label(x):
    if x > threshold_high:
        return 2
    elif x > threshold_med:
        return 1
    else:
        return 0

features['label'] = features['avg_usage'].apply(label)

# -------------------
# MODEL INPUT
# -------------------
X = features[['avg_usage', 'growth_rate', 'peak_ratio', 'variability']]
y = features['label']

# -------------------
# SPLIT
# -------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------
# TRAIN
# -------------------
model = RandomForestClassifier()
model.fit(X_train, y_train)

# -------------------
# EVALUATION
# -------------------
y_pred = model.predict(X_test)

print("\n Accuracy:", accuracy_score(y_test, y_pred))
print(" Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -------------------
# SAVE MODEL
# -------------------
joblib.dump(model, "ml/model.pkl")

print("\n Model saved successfully!")
