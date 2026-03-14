import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Spacecraft Telemetry Dashboard",
    layout="wide"
)

# -------------------------------
# LOAD DATA
# -------------------------------

df = pd.read_csv("telemetry_results.csv")

# -------------------------------
# SIDEBAR CONTROLS
# -------------------------------
decision_colors = {
    "Normal Operation": "green",
    "CRITICAL - Maintenance Required": "red",
    "WARNING - Abnormal Sensor Behaviour": "orange",
    "WARNING - Sensor Fault Detected": "purple"
}
st.sidebar.title("Mission Control")

engine_list = sorted(df["engine_id"].unique())

engine = st.sidebar.selectbox(
    "Select Engine",
    engine_list
)

sensor = st.sidebar.selectbox(
    "Select Sensor",
    [
        "sensor2","sensor3","sensor4","sensor6","sensor7",
        "sensor8","sensor9","sensor11","sensor12",
        "sensor13","sensor14","sensor15","sensor17",
        "sensor20","sensor21"
    ]
)

engine_data = df[df["engine_id"] == engine]
total_cycles = len(engine_data)

abnormal_cycles = engine_data[
    engine_data["decision"] != "Normal Operation"
].shape[0]

abnormal_percent = (abnormal_cycles / total_cycles) * 100
# -------------------------------
# HEADER
# -------------------------------

st.title("🚀 AI-Based Spacecraft Telemetry Monitoring System")

st.markdown(
"""
Mission Control Dashboard for Real-Time Engine Health Monitoring  
Combines **RUL prediction**, **anomaly detection**, and **AI decision logic**
"""
)

# -------------------------------
# METRIC CARDS
# -------------------------------
cycle = st.sidebar.slider(
    "Select Cycle",
    int(engine_data["cycle"].min()),
    int(engine_data["cycle"].max()),
    int(engine_data["cycle"].min())
)
current_state = engine_data[engine_data["cycle"] == cycle].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Predicted Remaining Useful Life",
    f"{current_state['predicted_RUL']:.2f} cycles"
)

col2.metric(
    "Anomaly Status",
    "Anomaly" if current_state["anomaly"] == -1 else "Normal"
)

col3.metric(
    "System Decision",
    current_state["decision"]
)
st.metric(
    "Abnormal Behaviour %",
    f"{abnormal_percent:.2f}%"
)
if abnormal_percent > 20:
    st.error("🚨 High abnormal behaviour detected")

elif abnormal_percent > 5:
    st.warning("⚠ Moderate abnormal activity")

else:
    st.success("✅ Engine operating normally")
# -------------------------------
# SENSOR TELEMETRY PLOT
# -------------------------------

st.subheader("Sensor Telemetry Over Time")

fig_sensor = px.line(
    engine_data,
    x="cycle",
    y=sensor,
    title=f"{sensor} behaviour over engine lifecycle",
)

st.plotly_chart(fig_sensor, use_container_width=True)

# -------------------------------
# RUL PREDICTION GRAPH
# -------------------------------

st.subheader("Remaining Useful Life Prediction")

fig_rul = px.line(
    engine_data,
    x="cycle",
    y="predicted_RUL",
    title="Remaining Useful Life Prediction"
)

abnormal_points = engine_data[
    engine_data["decision"] != "Normal Operation"
]

fig_rul.add_scatter(
    x=abnormal_points["cycle"],
    y=abnormal_points["predicted_RUL"],
    mode="markers",
    marker=dict(color="red", size=8),
    name="Abnormal Events"
)

st.plotly_chart(fig_rul, width='stretch')

# -------------------------------
# ANOMALY DETECTION GRAPH
# -------------------------------

st.subheader("Anomaly Detection")

fig_anomaly = px.scatter(
    engine_data,
    x="cycle",
    y=sensor,
    color="decision",
    color_discrete_map=decision_colors,
    title="Telemetry Anomaly Detection"
)

st.plotly_chart(fig_anomaly, width='stretch')
# -------------------------------
# ALERT PANEL
# -------------------------------

st.subheader("Maintenance Alert System")

if current_state["decision"].startswith("CRITICAL"):
    st.error("🚨 CRITICAL: Immediate Maintenance Required")

elif current_state["decision"].startswith("WARNING"):
    st.warning("⚠️ WARNING: Abnormal Sensor Behaviour Detected")

else:
    st.success("✅ System Operating Normally")