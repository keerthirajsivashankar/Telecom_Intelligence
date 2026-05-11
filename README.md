# 📡 Telecom Network Intelligence System

An end-to-end Data Engineering + Machine Learning pipeline to analyze telecom usage data, detect congestion risk, and visualize insights through a web dashboard.

---

## 🚀 📌 Project Overview

This project processes telecom usage data (calls, SMS, internet), stores it in a structured data warehouse, exposes APIs for analysis, and applies machine learning to predict network congestion risk.

---

## 🧠 System Architecture

Raw Data → Spark Processing → Parquet → MySQL Warehouse → FastAPI → ML Model → React Dashboard

### Components:

- ✅ Data Processing: Apache Spark
- ✅ Orchestration: Airflow
- ✅ Storage: MySQL (Star Schema)
- ✅ Backend: FastAPI
- ✅ Frontend: React (Vite)
- ✅ ML: Scikit-learn

---

## 🔄 End-to-End Flow

1. Raw telecom data is ingested (CSV/Parquet).
2. Spark processes and cleans the data.
3. Clean data is stored as Parquet files.
4. Airflow orchestrates the pipeline.
5. Data is loaded into MySQL warehouse (fact + dimension tables).
6. FastAPI exposes endpoints for analytics.
7. ML model predicts congestion risk.
8. React dashboard displays insights and predictions.

---

## 📊 Features

✔ Usage Summary Dashboard  
✔ Region-based analysis  
✔ Peak traffic identification  
✔ ML-based congestion prediction  
✔ Batch prediction generation

---

## 🔗 API Endpoints

### ✅ GET /usage/summary

Returns overall usage statistics.

### ✅ GET /usage/region/{region}

Returns hourly usage for a region.

### ✅ GET /usage/peak

Returns peak hours and busiest regions.

### ✅ POST /predict-usage-risk

Predicts congestion risk using ML model.

---

## 🤖 Machine Learning

- Model: Random Forest Classifier
- Features:
  - Average usage
  - Growth rate
  - Peak ratio
  - Variability

### 🎯 Output:

- LOW / MEDIUM / HIGH congestion risk
- Anomaly flag
- Confidence score

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

cd telecom-intelligence

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Backend
uvicorn api.app:app --reload

5️⃣ Run Frontend
cd frontend
npm install
npm run dev

🗂️ Project Structure
telecom-intelligence/
│
├── api/ # FastAPI backend
├── ml/ # ML scripts and model
├── data/ # Raw and processed data
├── airflow/ # DAGs
├── frontend/ # React app
├── requirements.txt
└── README.md

📦 Requirements
Key libraries:
pandas
numpy
fastapi
uvicorn
scikit-learn
joblib
mysql-connector-python

Install using:
Shellpip install -r requirements.txtShow more lines

📈 Batch Scoring
Run batch predictions:
Shellpython ml/batch_score.py``Show more lines
Output:
ml/batch_predictions.csv

⚠️ Notes

Dataset limited to ~200K rows for performance during development.
In production, this can be scaled using distributed infrastructure.

🏁 Conclusion
This project demonstrates a complete data engineering pipeline with:

scalable data processing
structured warehousing
API-based data serving
machine learning integration
interactive visualization

👨‍💻 Author
Keerthi Raj S
