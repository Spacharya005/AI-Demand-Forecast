import pandas as pd
from sqlalchemy import create_engine
import os

def load_csv_to_db():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    file_path = os.path.join(base_dir, 'data', 'coffee_sales.csv')

    print("Loading file from:", file_path)

    df = pd.read_csv(file_path)

    print("Data shape:", df.shape)
    print(df.head())

    engine = create_engine(
        "postgresql://ml_user:password123@localhost:5432/demand_forecasting"
    )

    if not engine.dialect.has_table(engine.connect(), "coffee_sales"):
        df.to_sql("coffee_sales", engine, if_exists="fail", index=False)
    else:
        df.to_sql("coffee_sales", engine, if_exists="append", index=False)

    print("✅ Data loaded into PostgreSQL successfully!")

if __name__ == "__main__":
    load_csv_to_db()