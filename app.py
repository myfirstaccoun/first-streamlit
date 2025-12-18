import streamlit as st
import matplotlib.pyplot as plt
from appa import (
    load_demand_data, naive_forecast, three_weeks_moving_average, exponential_smoothing,
    get_actual_demand, get_all_forecasts, get_error_table, get_best_methods, forecast_next_week, export_to_excel
)

# ================== Page Config ==================
st.set_page_config(
    page_title="Demand Forecasting Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Demand Forecasting Dashboard")
st.markdown("This app shows demand forecasts, error metrics, and predictions for next week.")

# ================== Load Data ==================
file_path = "Demand-History.xlsx"
df = load_demand_data(file_path)

# Apply Forecasts
df = naive_forecast(df)
df = three_weeks_moving_average(df)
df = exponential_smoothing(df, alpha=0.1)

# ================== Sidebar Controls ==================
st.sidebar.header("Controls")

show_actual = st.sidebar.checkbox("Show Actual Demand", value=True)
show_all_forecasts = st.sidebar.checkbox("Show All Forecasts", value=True)
show_errors = st.sidebar.checkbox("Show Error Metrics")
show_best = st.sidebar.checkbox("Show Best Forecast")
show_next_week = st.sidebar.checkbox("Forecast Next Week")
export_excel = st.sidebar.button("Export Current Table to Excel")

# ================== Display Actual Demand ==================
if show_actual:
    st.subheader("📋 Actual Demand")
    actual_df = get_actual_demand(df)
    st.dataframe(actual_df)

    if export_excel:
        export_to_excel(actual_df, "Actual_Demand.xlsx")
        st.success("Actual Demand exported to Actual_Demand.xlsx")

# ================== Display All Forecasts ==================
if show_all_forecasts:
    st.subheader("📋 All Forecasts")
    all_df = get_all_forecasts(df)
    st.dataframe(all_df)

    if export_excel:
        export_to_excel(all_df, "All_Forecasts.xlsx")
        st.success("All Forecasts exported to All_Forecasts.xlsx")

# ================== Display Error Metrics ==================
if show_errors:
    st.subheader("📊 Error Metrics (MAD, MSE, TS)")
    error_df = get_error_table(df)
    st.dataframe(error_df)

    if export_excel:
        export_to_excel(error_df, "Error_Metrics.xlsx")
        st.success("Error Metrics exported to Error_Metrics.xlsx")

# ================== Display Best Methods ==================
if show_best:
    st.subheader("🏆 Best Forecast Methods")
    best_methods = get_best_methods(df)
    st.write(best_methods)

# ================== Forecast Next Week ==================
if show_next_week:
    st.subheader("🔮 Forecast for Next Week")
    next_week_df = forecast_next_week(df, alpha=0.1)
    st.dataframe(next_week_df)

    if export_excel:
        export_to_excel(next_week_df, "Next_Week_Forecast.xlsx")
        st.success("Next Week Forecast exported to Next_Week_Forecast.xlsx")

# ================== Forecast Plots ==================
st.subheader("📈 Forecast Plots")
forecast_cols = ['Naive', 'ThreeWeeksMA', 'ExponentialSmoothing']

for col in forecast_cols:
    st.markdown(f"**{col} Forecast**")
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df['Week'], df['Demand'], marker='o', label='Actual Demand')
    ax.plot(df['Week'], df[col], marker='o', label=col)
    ax.set_xlabel("Week")
    ax.set_ylabel("Quantity")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
