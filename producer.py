import pandas as pd
import json
import time
import random
from kafka import KafkaProducer

# -------------------------------
# Load Dataset
# -------------------------------
df = pd.read_csv("creditcard.csv")

# -------------------------------
# Kafka Producer
# -------------------------------
producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("\nStarting Real-Time Transaction Stream...\n")

# -------------------------------
# Stream Transactions
# -------------------------------
for index, row in df.iterrows():

    transaction = row.to_dict()

    # Create synthetic user IDs
    transaction["user_id"] = random.randint(1, 100)

    # Send to Kafka
    producer.send(
        topic="transactions",
        value=transaction
    )

    print(
        f"Sent Transaction {index} | "
        f"User: {transaction['user_id']} | "
        f"Amount: {transaction['Amount']}"
    )

    # Simulate real-time stream
    time.sleep(0.1)

producer.flush()

print("\nStreaming Completed.")