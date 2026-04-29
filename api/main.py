from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
from src.models.insights import generate_insights
from src.features.feature_engineering import preprocess_data
from src.models.predict import load_model, predict
from src.models.anomaly import detect_anomalies

app = FastAPI()

# DB connection
engine = create_engine(
    "postgresql://ml_user:password123@localhost:5432/demand_forecasting"
)

@app.get("/")
def home():
    return {"message": "AI Demand Forecasting API is running"}

# 🔹 Get data from DB
@app.get("/data")
def get_data():
    query = "SELECT * FROM coffee_sales LIMIT 100"
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# 🔹 Forecast endpoint
@app.get("/forecast")
def forecast():
    query = "SELECT * FROM coffee_sales"
    df = pd.read_sql(query, engine)

    df = preprocess_data(df)

    model = load_model()

    preds = predict(model, df)

    df['prediction'] = preds

    return df[['datetime', 'prediction']].tail(20).to_dict(orient="records")

# 🔹 Health check
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/insights")
def insights():
    query = "SELECT * FROM coffee_sales"
    df = pd.read_sql(query, engine)

    df = preprocess_data(df)

    insights = generate_insights(df)

    return {"insights": insights}

@app.get("/anomalies")
def anomalies():
    query = "SELECT * FROM coffee_sales"
    df = pd.read_sql(query, engine)

    df = preprocess_data(df)

    anomalies_df = detect_anomalies(df)

    return anomalies_df[['datetime', 'transaction_qty']].to_dict(orient="records")