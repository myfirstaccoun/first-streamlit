import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================== Load Data ==================
def load_demand_data(file_path):
    """Load Excel file with columns 'Week' and 'Demand'"""
    return pd.read_excel(file_path)

# ================== Forecast Functions ==================
def naive_forecast(df):
    df['Naive'] = df['Demand'].shift(1)
    return df

def three_weeks_moving_average(df):
    df['ThreeWeeksMA'] = df['Demand'].rolling(window=3).mean().shift(1)
    return df

def exponential_smoothing(df, alpha=0.1):
    forecasts = []
    for i in range(len(df)):
        if i == 0:
            forecasts.append(df.loc[i, 'Demand'])
        else:
            forecast = alpha * df.loc[i-1, 'Demand'] + (1-alpha) * forecasts[i-1]
            forecasts.append(forecast)
    df['ExponentialSmoothing'] = forecasts
    return df

# ================== Plot Functions ==================
def plot_forecast(df, forecast_col, title_suffix=""):
    plt.figure(figsize=(10,5))
    plt.plot(df['Week'], df['Demand'], marker='o', label='Actual Demand')
    if forecast_col in df.columns:
        plt.plot(df['Week'], df[forecast_col], marker='o', label=forecast_col)
    plt.title(f"Weekly Demand vs {forecast_col} {title_suffix}")
    plt.xlabel("Week")
    plt.ylabel("Quantity")
    plt.grid(True)
    plt.legend()
    plt.show()

# ================== Error Metrics ==================
def mean_absolute_deviation(df, forecast_col):
    errors = df['Demand'] - df[forecast_col]
    return errors.abs().mean()

def mean_squared_error(df, forecast_col):
    errors = df['Demand'] - df[forecast_col]
    return (errors ** 2).mean()

def tracking_signal(df, forecast_col):
    errors = df['Demand'] - df[forecast_col]
    mad = errors.abs().mean()
    ts = errors.sum() / mad if mad != 0 else np.nan
    return ts

# ================== Best Forecast ==================
def best_forecast(df, method='MAD'):
    forecast_cols = [col for col in df.columns if col not in ['Week', 'Demand']]
    errors = {}
    
    for col in forecast_cols:
        if method == 'MAD':
            errors[col] = mean_absolute_deviation(df, col)
        elif method == 'MSE':
            errors[col] = mean_squared_error(df, col)
        else:
            raise ValueError("Method must be 'MAD' or 'MSE'")
    
    best_col = min(errors, key=errors.get)
    return best_col, errors[best_col]

def get_best_methods(df):
    best_mad_col, best_mad = best_forecast(df, method='MAD')
    best_mse_col, best_mse = best_forecast(df, method='MSE')
    return {
        'Best by MAD': (best_mad_col, best_mad),
        'Best by MSE': (best_mse_col, best_mse)
    }

# ================== Forecast Next Week ==================
def forecast_next_week(df, alpha=0.1):
    next_week = df['Week'].max() + 1
    
    # Naive
    naive = df['Demand'].iloc[-1]
    
    # Three Weeks Moving Average
    if len(df) >= 3:
        three_weeks_ma = df['Demand'].iloc[-3:].mean()
    else:
        three_weeks_ma = df['Demand'].mean()
    
    # Exponential Smoothing
    last_forecast = df['ExponentialSmoothing'].iloc[-1]
    last_demand = df['Demand'].iloc[-1]
    exp_smoothing = alpha * last_demand + (1-alpha) * last_forecast
    
    return pd.DataFrame([{
        'Week': next_week,
        'Naive': naive,
        'ThreeWeeksMA': three_weeks_ma,
        'ExponentialSmoothing': exp_smoothing
    }])

# ================== DataFrame Views (Streamlit Helpers) ==================
def get_actual_demand(df):
    """Return DataFrame with Week & Actual Demand only"""
    return df[['Week', 'Demand']]

def get_all_forecasts(df):
    """Return DataFrame with Week, Actual Demand, and all Forecasts"""
    return df[['Week', 'Demand', 'Naive', 'ThreeWeeksMA', 'ExponentialSmoothing']]

def get_error_table(df):
    """Return table with MAD, MSE, TS for all Forecasts"""
    data = []
    for method in ['Naive', 'ThreeWeeksMA', 'ExponentialSmoothing']:
        mad = mean_absolute_deviation(df, method)
        mse = mean_squared_error(df, method)
        ts = tracking_signal(df, method)
        data.append([method, mad, mse, ts])
    return pd.DataFrame(data, columns=['Method', 'MAD', 'MSE', 'TS'])

# ================== Export Function ==================
def export_to_excel(df, filename="forecast_export.xlsx"):
    df.to_excel(filename, index=False)
    print(f"Data exported to {filename}")

# ================== Main (for testing only) ==================
if __name__ == "__main__":
    file_path = "Demand-History.xlsx"
    df = load_demand_data(file_path)
    
    # Apply Forecasts
    df = naive_forecast(df)
    df = three_weeks_moving_average(df)
    df = exponential_smoothing(df, alpha=0.1)
    
    # Print Forecast Table
    print("\nForecasts Table:\n")
    print(df)
    
    # Plot Forecasts
    for forecast in ['Naive', 'ThreeWeeksMA', 'ExponentialSmoothing']:
        plot_forecast(df, forecast)
    
    # Calculate Error Metrics
    print("\nError Metrics:\n")
    error_table = get_error_table(df)
    print(error_table)
    
    # Best Forecast
    best_methods = get_best_methods(df)
    print("\nBest Methods:\n", best_methods)
    
    # Forecast Next Week
    next_forecast = forecast_next_week(df, alpha=0.1)
    print("\nForecast for Next Week:\n", next_forecast)
