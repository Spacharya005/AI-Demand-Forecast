from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    df = df.copy()

    # Use transaction quantity for anomaly detection
    model = IsolationForest(contamination=0.01, random_state=42)

    df['anomaly'] = model.fit_predict(df[['transaction_qty']])

    # -1 = anomaly, 1 = normal
    anomalies = df[df['anomaly'] == -1]

    return anomalies