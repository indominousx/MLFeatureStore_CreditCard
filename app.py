from fastapi import FastAPI
import redis
import joblib
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import time

# Load trained model
model = joblib.load("fraud_model.pkl")

# Redis connection
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

# FastAPI app
app = FastAPI()

# --------------------------------
# Prometheus Metrics
# --------------------------------

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API Requests"
)

PREDICTION_COUNT = Counter(
    "fraud_predictions_total",
    "Total Fraud Predictions"
)

PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction Latency"
)



@app.get("/")
def home():
    return {"message": "Fraud Detection API Running"}

# --------------------------------
# Metrics Endpoint
# --------------------------------
@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )

@app.get("/predict/{user_id}")
def predict(user_id: int):
    REQUEST_COUNT.inc()
    # Fetch features from Redis
    features = redis_client.hgetall(f"user:{user_id}")

    if not features:
        return {"error": "User features not found"}

    # Convert features into model input
    input_features = np.array([[
        float(features["amount"]),
        float(features["avg_amount"]),
        float(features["spike_ratio"]),
        float(features["time_gap"])
    ]])
    
    start_time = time.time()

    # Predict probability
    prediction = model.predict_proba(input_features)[0][1]
    
    PREDICTION_COUNT.inc()

    PREDICTION_LATENCY.observe(
        time.time() - start_time
    )

    return {
        "user_id": user_id,
        "fraud_probability": round(float(prediction), 4)
    }