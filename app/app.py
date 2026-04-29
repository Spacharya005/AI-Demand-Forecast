
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 🌈 Page config
st.set_page_config(page_title="AI Demand Forecasting", page_icon="☕", layout="wide")
# 🎨 Coffee Theme Styling
st.markdown("""
    <style>

    /* 🌍 App Background */
    .stApp {
        background: linear-gradient(135deg, #f7f3ef, #efe6dd);
        font-family: 'Segoe UI', sans-serif;
    }

    /* ☕ Headings */
    h1, h2, h3 {
        color: #3E2723;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* 📦 Card-style containers */
    .block-container {
        padding: 2rem 2rem;
        border-radius: 15px;
    }

    /* 🎛 Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4B2E2E, #6F4E37);
        color: white;
        padding: 1.5rem 1rem;
        backdrop-filter: blur(10px);
    }
                
    /* 🔘 Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6F4E37, #A67B5B);
        color: white;
        border-radius: 10px;
        padding: 0.6em 1em;
        font-weight: 700;
        border: none;
        transition: all 0.3s ease-in-out;
    }
    /* Sidebar text color */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Keep buttons styled */
    .stButton>button {
        background-color: #6F4E37;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, #A67B5B, #D2B48C);
    }

    /* 📊 Tables */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    }

    /* 📈 Charts spacing */
    .stPlotlyChart {
        border-radius: 12px;
        padding: 10px;
        background-color: #fff;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
    }

    /* 📢 Info / Alerts */
    .stAlert {
        border-radius: 10px;
    }

    /* 🔚 Footer */
    footer {
        visibility: hidden;
    }
    /* 🔠 Global font size */
    html, body, [class*="css"] {
        font-size: 16px;
    }

    /* Sidebar title */
    section[data-testid="stSidebar"] h1 {
        font-size: 24px !important;
    }

    /* Sidebar labels (Navigate, Filters, etc.) */
    section[data-testid="stSidebar"] label {
        font-size: 16px !important;
        font-weight: 600;
    }

    /* Radio buttons text */
    .stRadio label {
        font-size: 15px !important;
    }

    /* Selectbox text */
    .stSelectbox label {
        font-size: 15px !important;
    }

    /* Slider label */
    .stSlider label {
        font-size: 15px !important;
    }

    /* Main headings */
    h1 {
        font-size: 34px !important;
    }
    h2 {
        font-size: 26px !important;
    }
    h3 {
        font-size: 20px !important;
    }
            
    /* Fix text color inside white input boxes */
    .stSelectbox div[data-baseweb="select"] * {
        color: black !important;
    }

    .stSlider * {
        color: black !important;
    }

    .stTextInput input,
    .stNumberInput input {
        color: black !important;
    }

    /* Dropdown selected value */
    div[data-baseweb="select"] span {
        color: black !important;
    }

    </style>
""", unsafe_allow_html=True)

# ☕ Title
st.title("☕ AI Demand Forecasting Dashboard")
st.markdown("### ☕ Smart • Data-Driven • Predictive Analytics")

API_URL = "http://127.0.0.1:8000"

# =========================================================
# 🎛️ SIDEBAR (Navigation + Filters)
# =========================================================
st.sidebar.title("⚙️ Control Panel")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview", "📈 Forecast", "🧠 Insights", "🚨 Anomalies"]
)

st.sidebar.markdown("---")

# 🎯 Filters (will apply where needed)
st.sidebar.subheader("🔍 Filters")

selected_hour = st.sidebar.slider("Select Hour", 0, 23, (6, 18))
selected_day = st.sidebar.selectbox(
    "Day of Week",
    ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

beverage_type = st.sidebar.selectbox(
    "Beverage Type",
    ["All", "Coffee", "Tea", "Other"]
)

# =========================================================
# 🏠 HOME and 📊 DATA TAB
# =========================================================
if page == "🏠 Overview":
    st.markdown("## 🟢 System Overview")

    # 🔹 API Status
    if st.button("Check API Status"):
        try:
            res = requests.get(f"{API_URL}/health")
            st.success(res.json())
        except:
            st.error("API not running. Start FastAPI server.")

    st.markdown("---")

    # 🔹 Load Data
    st.markdown("## 📂 Data Overview")

    if st.button("Load Data"):
        try:
            res = requests.get(f"{API_URL}/data")
            df = pd.DataFrame(res.json())

            # Save in session
            st.session_state.df = df

            st.dataframe(df.head(100), use_container_width=True)

            # 📊 Advanced Chart
            if 'hour' in df.columns:
                
                hourly = df.groupby('hour')['transaction_qty'].sum().reset_index()

                fig = px.bar(
                    hourly,
                    x='hour',
                    y='transaction_qty',
                    title="☕ Hourly Demand Distribution"
                )

                fig.update_traces(marker_color="#A67B5B")

                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")

# =========================================================
# 📈 FORECAST TAB
# =========================================================
elif page == "📈 Forecast":
    st.markdown("## 📈 Demand Forecasting")

    if st.button("Run Forecast"):
        try:
            with st.spinner("Running forecast..."):
                res = requests.get(f"{API_URL}/forecast")
                res.raise_for_status()
                df = pd.DataFrame(res.json())

                if df.empty:
                    st.warning("No forecast data available")
                    st.stop()

                # ✅ Convert datetime properly
                df['datetime'] = pd.to_datetime(df['datetime'])

                # ✅ Better rolling mean (no data loss)
                df['rolling_mean'] = df['prediction'].rolling(window=5, min_periods=1).mean()

                # ✅ Remove duplicates
                df = df.drop_duplicates(subset='datetime')
                
        except Exception as e:
            st.error(f"Error fetching forecast: {e}")
            st.stop()
        fig = px.line(df, x='datetime', y=['prediction', 'rolling_mean'],
                    title="📊 Forecast vs Trend")

        fig.update_traces(line=dict(width=3))

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📉 Prediction Trend")
        fig = px.line(
            df,
            x='datetime',
            y='prediction',
            title="📈 Demand Forecast Trend",
        )

        fig.update_traces(line=dict(color="#6F4E37", width=3))  # coffee color

        fig.update_layout(
            plot_bgcolor="#f7f3ef",
            paper_bgcolor="#f7f3ef",
            font=dict(color="#4B2E2E"),
            xaxis_title="Datetime",
            yaxis_title="Demand",
            legend_title="Legend"
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 🧠 INSIGHTS TAB
# =========================================================
elif page == "🧠 Insights":
    st.markdown("## 🧠 Business Insights")

    if st.button("Get Insights"):
        res = requests.get(f"{API_URL}/insights")
        insights = res.json()["insights"]

        for i in insights:
            st.info(i)

# =========================================================
# 🚨 ANOMALY TAB
# =========================================================
elif page == "🚨 Anomalies":
    st.markdown("## 🚨 Anomaly Detection")

    if st.button("Detect Anomalies"):
        res = requests.get(f"{API_URL}/anomalies")
        df = pd.DataFrame(res.json())

        if not df.empty:
            st.dataframe(df, use_container_width=True)

            st.markdown("### 📉 Anomaly Trend")
            st.line_chart(df['transaction_qty'])

            fig = px.scatter(
                df,
                y='transaction_qty',
                title="🚨 Anomaly Detection",
            )

            fig.update_traces(marker=dict(color="red", size=8))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No anomalies detected 🎉")

        fig.update_traces(marker=dict(color="red", size=8))

        st.plotly_chart(fig, use_container_width=True)
# =========================================================
# ☕ Footer
# =========================================================
st.markdown("---")
st.markdown(
    "<center>☕ Built with AI • ML • SQL • FastAPI • Streamlit</center>",
    unsafe_allow_html=True
)