from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error
import pandas as pd
import joblib
import numpy as np
import os

def train_model(df):
    df = df.copy()

    # Target variable (adjust if needed)
    target = 'transaction_qty'

    # Features
    features = ['hour', 'day', 'month', 'day_of_week']

    X = df[features]
    y = df[target]

    # Train-test split (time-based split is better, but keep simple now)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    # BEFORE (likely)
    model.fit(df['sales'])

    # AFTER (correct)
    split_date = "2023-01-01"

    train = df[df['date'] < split_date]
    test = df[df['date'] >= split_date]
    save_model(model)
    
    # Predictions
    predictions = model.predict(len(test))

    mae = mean_absolute_error(test['sales'], predictions)
    rmse = np.sqrt(mean_squared_error(test['sales'], predictions))

    print("MAE:", mae)
    print("RMSE:", rmse)

    return model, mae, X_test, y_test

def save_model(model):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    model_path = os.path.join(base_dir, 'models', 'model.pkl')

    joblib.dump(model, model_path)