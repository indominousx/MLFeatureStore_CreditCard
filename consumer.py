import json
import statistics
import time
from collections import defaultdict, deque
import psycopg2
from kafka import KafkaConsumer
import redis

# -------------------------------
# Redis Connection
# -------------------------------
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)
    # PostgreSQL Connection
pg_conn = psycopg2.connect(
     host="localhost",
     port=5432,
     database="featurestore",
     user="postgres",
     password="postgres"
    )
    
pg_cursor = pg_conn.cursor()


# -------------------------------
# Kafka Consumer
# -------------------------------
consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers='127.0.0.1:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("\nListening For Transactions...\n")

# -------------------------------
# User-Level Rolling Windows
# -------------------------------
user_windows = defaultdict(
    lambda: deque(maxlen=10)
)

# Store previous transaction time per user
previous_transaction_time = {}

# -------------------------------
# Consume Stream
# -------------------------------
for message in consumer:

    transaction = message.value

    # -------------------------------
    # Extract Transaction Data
    # -------------------------------
    user_id = transaction["user_id"]

    amount = float(transaction["Amount"])

    txn_time = float(transaction["Time"])

    # -------------------------------
    # Update User Window
    # -------------------------------
    user_windows[user_id].append(amount)

    # -------------------------------
    # Feature Engineering
    # -------------------------------

    # Rolling average amount
    avg_amount = statistics.mean(
        user_windows[user_id]
    )

    # Maximum recent amount
    max_amount = max(
        user_windows[user_id]
    )

    # Transaction count
    txn_count = len(
        user_windows[user_id]
    )

    # Spending spike ratio
    spike_ratio = (
        amount / avg_amount
        if avg_amount != 0 else 0
    )

    # Time gap
    if user_id not in previous_transaction_time:
        time_gap = 0
    else:
        time_gap = (
            txn_time -
            previous_transaction_time[user_id]
        )

    previous_transaction_time[user_id] = txn_time

    # -------------------------------
    # Store Features In Redis
    # -------------------------------
    redis_key = f"user:{user_id}"

    redis_client.hset(
        redis_key,
        mapping={
            "amount": amount,
            "avg_amount": avg_amount,
            "max_amount": max_amount,
            "txn_count": txn_count,
            "spike_ratio": spike_ratio,
            "time_gap": time_gap
        }
    )
    # -------------------------------
# Store Features In PostgreSQL
# -------------------------------
    pg_cursor.execute("""
     INSERT INTO transaction_features (

    user_id,
    amount,
    avg_amount,
    max_amount,
    txn_count,
    spike_ratio,
    time_gap

       )
     VALUES (%s, %s, %s, %s, %s, %s, %s)
      """, (

    user_id,
    amount,
    avg_amount,
    max_amount,
    txn_count,
    spike_ratio,
    time_gap

      ))

    pg_conn.commit()


    # -------------------------------
    # Feature TTL (1 Hour)
    # -------------------------------
    redis_client.expire(
        redis_key,
        1800
    )

    # -------------------------------
    # Print Features
    # -------------------------------
    print("=" * 60)

    print(f"User ID           : {user_id}")

    print(f"Transaction Amount: {amount}")

    print(f"Rolling Avg Amount: {avg_amount:.2f}")

    print(f"Max Recent Amount : {max_amount:.2f}")

    print(f"Transaction Count : {txn_count}")

    print(f"Spike Ratio       : {spike_ratio:.2f}")

    print(f"Time Gap          : {time_gap}")

    print("=" * 60)

    # -------------------------------
    # Fraud Heuristic
    # -------------------------------
    if spike_ratio > 5:
        print("POSSIBLE FRAUD DETECTED\n")

    time.sleep(0.05)