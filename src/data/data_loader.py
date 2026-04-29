import pandas as pd
import os

def load_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    file_path = os.path.join(base_dir, 'data', 'coffee_sales.csv')

    df = pd.read_csv(file_path)
    return df