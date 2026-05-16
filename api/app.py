from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from ml.predict import predict_usage_risk

app = FastAPI(title="Telecom API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  DB connection
def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="keerthi",
        password="1234",
        database="telecom_db"
    )

# ------------------------------
#  RESPONSE MODELS
# ------------------------------

class SummaryResponse(BaseModel):
    total_calls: int
    total_sms: int
    total_internet_mb: float
    peak_hour: int
    busiest_region: str


class HourlyData(BaseModel):
    hour: int
    calls: int
    sms: int
    internet_mb: float


class RegionResponse(BaseModel):
    region: str
    hourly_distribution: list[HourlyData]
    trend: list


class PeakResponse(BaseModel):
    top_hours: list
    top_regions: list


class FeatureResponse(BaseModel):
    region: str
    avg_usage: float
    growth_rate: float
    variability: float
    peak_ratio: float = 1.2 


class PredictRequest(BaseModel):
    region: str
    avg_usage: float
    growth_rate: float
    variability: float
    peak_ratio: float 


class PredictResponse(BaseModel):
    congestion_risk: str
    anomaly_flag: bool
    score: float


# ------------------------------
# API 1 — SUMMARY
# ------------------------------

@app.get("/usage/summary", response_model=SummaryResponse)
def usage_summary():
    conn = None
    cur = None
    try:
        conn = get_conn()
        cur = conn.cursor()

        #  totals
        cur.execute("""
            SELECT 
                COALESCE(SUM(call_count), 0),
                COALESCE(SUM(sms_count), 0),
                COALESCE(SUM(internet_mb), 0)
            FROM fact_usage
        """)
        result = cur.fetchone()

        total_calls, total_sms, total_internet = result or (0, 0, 0)

        #  peak hour
        cur.execute("""
            SELECT t.hour, SUM(f.call_count)
            FROM fact_usage f
            JOIN dim_time t ON f.time_id = t.time_id
            GROUP BY t.hour
            ORDER BY SUM(f.call_count) DESC
            LIMIT 1
        """)
        peak_row = cur.fetchone()
        peak_hour = peak_row[0] if peak_row else 0

        # busiest region
        cur.execute("""
            SELECT r.region_name, SUM(f.call_count)
            FROM fact_usage f
            JOIN dim_region r ON f.region_id = r.region_id
            GROUP BY r.region_name
            ORDER BY SUM(f.call_count) DESC
            LIMIT 1
        """)
        region_row = cur.fetchone()
        busiest_region = region_row[0] if region_row and region_row[0] else "Unknown"

        return SummaryResponse(
            total_calls=int(total_calls),
            total_sms=int(total_sms),
            total_internet_mb=float(total_internet),
            peak_hour=int(peak_hour),
            busiest_region=str(busiest_region)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal Server Error", "message": str(e)}
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
# ------------------------------
# API 2 — REGION
# ------------------------------

@app.get("/usage/region/{region}", response_model=RegionResponse)
def region_usage(region: str):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT t.hour, 
                   SUM(f.call_count),
                   SUM(f.sms_count),
                   SUM(f.internet_mb)
            FROM fact_usage f
            JOIN dim_time t ON f.time_id = t.time_id
            JOIN dim_region r ON f.region_id = r.region_id
            WHERE r.region_name = %s
            GROUP BY t.hour
            ORDER BY t.hour
        """, (region,))

        rows = cur.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="Region not found")

        hourly = [
            {
                "hour": r[0],
                "calls": r[1],
                "sms": r[2],
                "internet_mb": r[3]
            }
            for r in rows
        ]

        return {
            "region": region,
            "hourly_distribution": hourly,
            "trend": hourly[-10:]  # last 10 points
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# API 3 — PEAK
# ------------------------------

@app.get("/usage/peak", response_model=PeakResponse)
def peak_usage():
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Top hours
        cur.execute("""
            SELECT t.hour, SUM(f.call_count + f.sms_count + f.internet_mb)
            FROM fact_usage f
            JOIN dim_time t ON f.time_id = t.time_id
            GROUP BY t.hour
            ORDER BY 2 DESC
            LIMIT 5
        """)
        top_hours = [{"hour": r[0], "total_usage": r[1]} for r in cur.fetchall()]

        # Top regions
        cur.execute("""
            SELECT r.region_name, SUM(f.call_count + f.sms_count + f.internet_mb)
            FROM fact_usage f
            JOIN dim_region r ON f.region_id = r.region_id
            GROUP BY r.region_name
            ORDER BY 2 DESC
            LIMIT 5
        """)
        top_regions = [{"region": r[0], "total_usage": r[1]} for r in cur.fetchall()]

        return {"top_hours": top_hours, "top_regions": top_regions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# API 4 — FEATURES
# ------------------------------

@app.get("/usage/features/{region}", response_model=FeatureResponse)
def features(region: str):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                AVG(f.call_count + f.sms_count + f.internet_mb),
                STDDEV(f.call_count + f.sms_count + f.internet_mb),
                MAX(f.call_count + f.sms_count + f.internet_mb)
            FROM fact_usage f
            JOIN dim_region r ON f.region_id = r.region_id
            WHERE r.region_name = %s
        """, (region,))

        avg_usage, variability, peak = cur.fetchone()

        growth_rate = 0.1  # simplified
        peak_ratio = peak / avg_usage if avg_usage else 0

        return FeatureResponse(
            region=region,
            avg_usage=float(avg_usage or 0),
            growth_rate=growth_rate,
            variability=float(variability or 0),
            peak_ratio=float(peak_ratio)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------
# API 5 — PREDICTION
# ------------------------------

@app.post("/predict-usage-risk", response_model=PredictResponse)
def predict(data: PredictRequest):
    
    if data.avg_usage <= 0:
        raise HTTPException(status_code=400, detail="Invalid avg_usage")

    result = predict_usage_risk(data.dict())

    return result