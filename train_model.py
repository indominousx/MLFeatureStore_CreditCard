import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import joblib

# Load dataset
df = pd.read_csv("creditcard.csv")

# Features and labels
X = df.drop("Class", axis=1)
# Create engineered features
df["avg_amount"] = df["Amount"].rolling(10).mean().fillna(df["Amount"])

df["spike_ratio"] = (
    df["Amount"] / df["avg_amount"]
).fillna(1)

df["time_gap"] = df["Time"].diff().fillna(0)

# Training features
X = df[
    [
        "Amount",
        "avg_amount",
        "spike_ratio",
        "time_gap"
    ]
]

y = df["Class"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Model
model = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    scale_pos_weight=100
)

# Train
model.fit(X_train, y_train)

# Predictions
preds = model.predict(X_test)

# Metrics
print(classification_report(y_test, preds))

# Save model
joblib.dump(model, "fraud_model.pkl")

print("\nModel saved as fraud_model.pkl")