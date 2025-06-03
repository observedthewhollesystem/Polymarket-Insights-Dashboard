import pandas as pd
import numpy as np # Ensure numpy is imported if used, e.g. for np.nan

def calculate_moving_average(price_series: pd.Series, window: int = 7):
    """
    Calculates a simple moving average for a given price series.
    Returns a series with NaN for periods where MA cannot be calculated.
    """
    if not isinstance(price_series, pd.Series):
        # In a real app, might log this or raise a more specific error
        print("Error: price_series must be a Pandas Series for moving average.")
        return pd.Series(dtype='float64') 
    if price_series.empty or len(price_series) < 1: # Allow MA even if less than window, will produce NaNs
        return pd.Series(index=price_series.index, dtype='float64')
    return price_series.rolling(window=window, min_periods=1).mean() # min_periods=1 allows MA for shorter series

def calculate_price_change_percentage(price_series: pd.Series, periods: int = 1):
    """
    Calculates the percentage change in price over a number of periods.
    Returns a series with NaN for initial periods.
    """
    if not isinstance(price_series, pd.Series):
        print("Error: price_series must be a Pandas Series for percentage change.")
        return pd.Series(dtype='float64')
    if price_series.empty or len(price_series) < periods: # Need at least 'periods' values to calculate change
        return pd.Series(index=price_series.index, dtype='float64')
    return price_series.pct_change(periods=periods) * 100

def calculate_volatility(price_series: pd.Series, window: int = 14):
    """
    Calculates historical volatility (standard deviation of log returns) over a window.
    This is a common financial metric.
    """
    if not isinstance(price_series, pd.Series) or price_series.empty or len(price_series) < window:
        return pd.Series(index=price_series.index, dtype='float64')
    
    log_returns = np.log(price_series / price_series.shift(1))
    volatility = log_returns.rolling(window=window, min_periods=1).std() * np.sqrt(window) # Annualize if daily data and window is days
    return volatility


def process_market_data(historical_df: pd.DataFrame, market_id: str):
    """
    Processes historical market data to add analytical columns.
    This is where you'd add more "fancy" descriptive stats on PAST data.
    NO PREDICTIVE analytics.
    """
    if not isinstance(historical_df, pd.DataFrame) or historical_df.empty:
        print(f"Warning: Historical DataFrame for {market_id} is empty or not a DataFrame. Skipping processing.")
        return pd.DataFrame() # Return empty DataFrame

    # Ensure the critical 'yes_price' column exists
    yes_price_col = f'{market_id}_yes_price'
    if yes_price_col not in historical_df.columns:
        print(f"Warning: Column '{yes_price_col}' not found in historical_df for {market_id}. Cannot process.")
        return historical_df # Or return empty: pd.DataFrame()

    processed_df = historical_df.copy()
    
    # Ensure 'date' column is datetime
    if 'date' in processed_df.columns:
        processed_df['date'] = pd.to_datetime(processed_df['date'])
        processed_df = processed_df.sort_values(by='date') # Ensure data is sorted by date for rolling calculations
    else:
        print("Warning: 'date' column missing. Time-series calculations might be incorrect.")

    # Calculate 7-day and 30-day moving average for 'Yes' price
    processed_df[f'{yes_price_col}_7d_ma'] = calculate_moving_average(processed_df[yes_price_col], window=7)
    processed_df[f'{yes_price_col}_30d_ma'] = calculate_moving_average(processed_df[yes_price_col], window=30)
    
    # Calculate 1-day percentage change for 'Yes' price
    processed_df[f'{yes_price_col}_1d_pct_change'] = calculate_price_change_percentage(processed_df[yes_price_col], periods=1)
    
    # Calculate 14-day Volatility for 'Yes' price
    processed_df[f'{yes_price_col}_14d_volatility'] = calculate_volatility(processed_df[yes_price_col], window=14)

    # Example: Identify days with high volume (e.g., > 80th percentile of historical volume)
    volume_col = f'{market_id}_volume'
    if volume_col in processed_df.columns and not processed_df[volume_col].empty:
        # Ensure volume is numeric, coerce errors to NaN then fill with 0 for quantile calculation
        numeric_volume = pd.to_numeric(processed_df[volume_col], errors='coerce').fillna(0)
        if not numeric_volume.empty and numeric_volume.nunique() > 1: # Check if there's actual variation
            high_volume_threshold = numeric_volume.quantile(0.80)
            processed_df['high_volume_day'] = numeric_volume > high_volume_threshold
        else:
            processed_df['high_volume_day'] = False # Default if no variation or all NaN/zero
    else:
        processed_df['high_volume_day'] = False # Default if volume column is missing or empty
        
    return processed_df

# --- Example Usage (for testing this file directly) ---
if __name__ == "__main__":
    # from polymarket_client_mock import get_mock_historical_prices # For direct testing
    
    mock_market_id = "test_market"
    sample_dates = pd.date_range(end=pd.Timestamp.now(), periods=90, freq='D')
    # More realistic price simulation for testing volatility
    np.random.seed(42)
    initial_price = 0.5
    price_changes = np.random.normal(0, 0.03, 90)
    sample_yes_prices = np.clip(initial_price + np.cumsum(price_changes), 0.01, 0.99)
    sample_volume = np.random.randint(100, 5000, 90)
    
    sample_df = pd.DataFrame({
        'date': sample_dates,
        f'{mock_market_id}_yes_price': sample_yes_prices,
        f'{mock_market_id}_volume': sample_volume
    })

    print("--- Original Sample Data (Tail) ---")
    print(sample_df.tail())

    processed_data = process_market_data(sample_df.copy(), mock_market_id) # Pass a copy
    print("\n--- Processed Data (Tail) ---")
    
    cols_to_print = [
        'date', 
        f'{mock_market_id}_yes_price', 
        f'{mock_market_id}_yes_price_7d_ma',
        f'{mock_market_id}_yes_price_30d_ma',
        f'{mock_market_id}_yes_price_1d_pct_change',
        f'{mock_market_id}_yes_price_14d_volatility',
        'high_volume_day'
    ]
    print(processed_data[cols_to_print].tail())
    # Check for NaNs
    print("\nNaN counts in processed data:")
    print(processed_data[cols_to_print].isnull().sum())