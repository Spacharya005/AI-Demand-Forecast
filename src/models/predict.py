import joblib
import os
import pandas as pd

def load_model():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    model_path = os.path.join(base_dir, 'models', 'model.pkl')

    return joblib.load(model_path)


def predict(model, input_df):
    features = ['hour', 'day', 'month', 'day_of_week']
    return model.predict(input_df[features])