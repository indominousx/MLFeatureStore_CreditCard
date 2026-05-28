from fastapi import FastAPI
import redis
import joblib
import numpy as np

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

@app.get("/")
def home():
    return {"message": "Fraud Detection API Running"}

@app.get("/predict/{user_id}")
def predict(user_id: int):

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

    # Predict probability
    prediction = model.predict_proba(input_features)[0][1]

    return {
        "user_id": user_id,
        "fraud_probability": round(float(prediction), 4)
    }