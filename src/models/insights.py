import pandas as pd

def generate_insights(df):
    insights = []

    peak_hour = df.groupby('hour')['transaction_qty'].sum().idxmax()
    low_hour = df.groupby('hour')['transaction_qty'].sum().idxmin()

    peak_value = df.groupby('hour')['transaction_qty'].sum().max()

    insights.append(f"📈 Peak demand at {peak_hour}:00 with {peak_value} transactions")
    insights.append(f"📉 Lowest demand at {low_hour}:00")

    # Weekend vs weekday
    weekend_sales = df[df['day_of_week'] >= 5]['transaction_qty'].sum()
    weekday_sales = df[df['day_of_week'] < 5]['transaction_qty'].sum()

    if weekend_sales > weekday_sales:
        insights.append("🛒 Weekend sales are higher than weekdays")
    else:
        insights.append("🏢 Weekday sales dominate")

    insights.append(f"💡 Recommendation: Increase staff and stock around {peak_hour}:00")

    return insights