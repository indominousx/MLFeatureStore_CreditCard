import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="featurestore",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS transaction_features (

    id SERIAL PRIMARY KEY,

    user_id INT,

    amount FLOAT,

    avg_amount FLOAT,

    max_amount FLOAT,

    txn_count INT,

    spike_ratio FLOAT,

    time_gap FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()

cur.close()
conn.close()

print("PostgreSQL table created successfully.")