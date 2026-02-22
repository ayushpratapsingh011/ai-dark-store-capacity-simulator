import streamlit as st
import numpy as np

st.set_page_config(page_title="AI Dark Store Capacity Simulator", layout="wide")

st.title("AI-Assisted Capacity Planning Simulator")
st.markdown("Simulate service levels under staffing and forecast uncertainty.")

# -----------------------------
# Sidebar Inputs
# -----------------------------

st.sidebar.header("Decision Inputs")

surge_riders = st.sidebar.slider("Surge Riders", 5, 20, 12)
forecast_error = st.sidebar.selectbox("Forecast Error", [0.20, 0.08])

# -----------------------------
# Model Parameters
# -----------------------------

BASE_DEMAND = 3
PEAK_MULTIPLIER = 2
SERVICE_RATE = 4
HOURS = 12
RIDER_WAGE = 100
PICKER_WAGE = 120
BASE_PICKERS = 14
BASE_RIDERS = 20

# -----------------------------
# Simulation
# -----------------------------

np.random.seed(42)

minutes = 720
completed = 0
breaches = 0

riders = BASE_RIDERS + surge_riders
pickers = BASE_PICKERS

for minute in range(minutes):

    demand = np.random.poisson(BASE_DEMAND)

    if 300 <= minute <= 540:
        demand = np.random.poisson(BASE_DEMAND * PEAK_MULTIPLIER)

    demand = int(demand * (1 + np.random.uniform(-forecast_error, forecast_error)))

    capacity = riders * SERVICE_RATE

    served = min(demand, capacity)
    completed += served

    if demand > capacity:
        breaches += (demand - capacity)

total_orders = completed + breaches
service_level = 1 - (breaches / total_orders)

staffing_cost = (pickers * PICKER_WAGE * HOURS) + (riders * RIDER_WAGE * HOURS)

AOV = 500
MARGIN = 0.20
revenue = completed * AOV * MARGIN
profit = revenue - staffing_cost

# -----------------------------
# Output Section
# -----------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Service Level", f"{round(service_level * 100, 2)} %")
col2.metric("Staffing Cost", f"₹ {round(staffing_cost, 0)}")
col3.metric("Profit", f"₹ {round(profit, 0)}")

if service_level >= 0.95:
    st.success("SLA Achieved")
else:
    st.error("SLA Breach Risk")