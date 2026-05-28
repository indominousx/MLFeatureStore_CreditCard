
# Start Infrastructure

Open terminal in project directory:

```bash
docker compose up -d
```

This starts:

* Kafka
* Redis
* PostgreSQL
* Prometheus
* Grafana

---

# Verify Containers

```bash
docker ps
```

Expected containers:

* kafka
* redis
* postgres
* prometheus
* grafana

---

# Create PostgreSQL Table

Run once:

```bash
python setup_postgres.py
```

---

# Train Model

Run once:

```bash
python train_model.py
```

This generates:

```text
fraud_model.pkl
```

---

# Start Consumer

Open a new terminal:

```bash
python consumer.py
```

---

# Start Producer

Open another terminal:

```bash
python producer.py
```

---

# Start FastAPI

Open another terminal:

```bash
uvicorn app:app --reload
```

---

# Access FastAPI

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

Prediction API:

```text
http://127.0.0.1:8000/predict/1
```

---

# Access Prometheus

```text
http://localhost:9090
```

---

# Access Grafana

```text
http://localhost:3000
```

Default Credentials:

| Username | Password |
| -------- | -------- |
| admin    | admin    |

---

# Grafana Dashboard Setup

## Add Prometheus Data Source

Connections → Data Sources → Add Data Source → Prometheus

Set URL:

```text
http://prometheus:9090
```

---

# Suggested Queries

## API Requests

```promql
api_requests_total
```

---

## Fraud Predictions

```promql
fraud_predictions_total
```

---

## Prediction Latency

```promql
prediction_latency_seconds_sum
```

---

## Request Rate

```promql
rate(api_requests_total[1m])
```

---

# Auto Refresh Recommendation

Set Grafana refresh interval:

```text
5s
```

---

# How To Stop Everything

---

# Stop Producer

Close terminal or press:

```text
CTRL + C
```

---

# Stop Consumer

Close terminal or press:

```text
CTRL + C
```

---

# Stop FastAPI

Close terminal or press:

```text
CTRL + C
```

---

# Stop Docker Infrastructure

```bash
docker compose down
```

---

# IMPORTANT

Do NOT use:

```bash
docker compose down -v
```

unless you want to delete:

* Grafana dashboards
* PostgreSQL data
* Prometheus history

---

# Persistent Docker Volumes

The project uses persistent volumes for:

* PostgreSQL
* Prometheus
* Grafana

This ensures:

* dashboards survive restarts
* metrics remain stored
* database persists