import pandas as pd
import numpy as np
import time
import random

# --- MOCK DATA GENERATION ---
# This section simulates fetching data from Polymarket.
# In a real application, you would replace these functions
# with actual API calls to Polymarket or a data provider.
# THIS IS MOCK DATA. NO REAL PREDICTIONS. FOR PORTFOLIO DEMONSTRATION ONLY.

def get_mock_market_details(market_id: str):
    """
    MOCKS fetching basic details for a Polymarket market.
    In a real app, this would hit the Polymarket API.
    """
    if not market_id:
        # In a real app, you might raise an error or return a specific error structure
        return {"error": "Market ID cannot be empty."}
    
    # Simulate some market details with more variety
    market_data_store = {
        "market1": {"name": "Will AI achieve AGI by 2030?", "category": "Technology", "base_yes": 0.30, "volatility": 0.1},
        "market2": {"name": "Who will win the next US Presidential Election?", "category": "Politics", "base_yes": 0.50, "volatility": 0.15},
        "market3": {"name": "Will Ethereum reach $10,000 by EOY?", "category": "Crypto", "base_yes": 0.15, "volatility": 0.2},
        "market4": {"name": "Will fusion power be commercially viable by 2040?", "category": "Science", "base_yes": 0.20, "volatility": 0.08},
        "market5": {"name": "Will global temperatures rise >2°C by 2050?", "category": "Climate", "base_yes": 0.65, "volatility": 0.05}
    }
    categories = ["Politics", "Crypto", "Sports", "Technology", "Science", "Climate", "Entertainment"]
    
    # Simulate a delay as if an API call is being made
    # time.sleep(random.uniform(0.2, 0.6)) # Reduced for faster UI updates during dev
    
    selected_market = market_data_store.get(market_id)
    
    if selected_market:
        current_yes_price = round(np.clip(selected_market["base_yes"] + random.uniform(-selected_market["volatility"], selected_market["volatility"]), 0.01, 0.99), 2)
        current_no_price = round(1 - current_yes_price, 2) # For binary markets, No = 1 - Yes
        return {
            "id": market_id,
            "name": selected_market["name"],
            "category": selected_market["category"],
            "current_yes_price": current_yes_price,
            "current_no_price": current_no_price,
            "liquidity_usd": random.randint(5000, 2000000),
            "volume_24h_usd": random.randint(1000, selected_market.get("liquidity_usd", 500000) // 10), # Volume related to liquidity
            "resolution_date": (pd.Timestamp.now() + pd.Timedelta(days=random.randint(10, 730))).strftime('%Y-%m-%d'),
            "description": f"This is a mock description for the market '{selected_market['name']}'. Resolution criteria and other details would go here in a real market."
        }
    else: # Handle unknown market_id more gracefully
        return {
            "id": market_id, 
            "name": f"Mock Market: {market_id} (Generic)", 
            "category": random.choice(categories),
            "current_yes_price": round(random.uniform(0.05, 0.95), 2),
            "current_no_price": round(1 - random.uniform(0.05, 0.95), 2),
            "liquidity_usd": random.randint(1000, 100000),
            "volume_24h_usd": random.randint(100, 10000),
            "resolution_date": (pd.Timestamp.now() + pd.Timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
            "description": "This is a generic mock market. Enter a known ID like 'market1' for more specific mock data.",
            "warning": "Using generic mock data as market_id was not predefined."
        }


def get_mock_historical_prices(market_id: str, days: int = 90):
    """
    MOCKS fetching historical price data for a Polymarket market.
    Generates a plausible-looking random walk for 'Yes' prices, No price is 1 - Yes.
    """
    if not market_id:
        return pd.DataFrame() # Return empty DataFrame if no market_id

    # time.sleep(random.uniform(0.5, 1.2)) # Reduced for faster UI updates

    dates = pd.date_range(end=pd.Timestamp.now() - pd.Timedelta(days=1), periods=days, freq='D') # Ensure historical data ends yesterday
    
    # Start with a random price and let it "walk"
    # Make starting price somewhat consistent for a given mock market_id for more stable visuals if needed,
    # or fully random. For now, let's use a hash for some determinism based on market_id.
    seed_val = sum(ord(c) for c in market_id) % 100 / 100.0 # Simple hash to seed
    yes_price = np.clip(seed_val * 0.8 + 0.1, 0.1, 0.9) # Start price between 0.1 and 0.9
    
    yes_prices = []
    no_prices = []
    volumes = []

    for i in range(days):
        yes_prices.append(yes_price)
        no_prices.append(round(1 - yes_price, 2)) 
        
        # Simulate volume spikes occasionally
        if random.random() < 0.1: # 10% chance of a volume spike
            volumes.append(np.random.randint(2000, 15000))
        else:
            volumes.append(np.random.randint(100, 2000))
        
        # Random walk for yes_price, with a slight drift possibility and mean reversion tendency
        change = random.normalvariate(0, 0.03) # Smaller, more realistic daily changes
        # Add a slight pull back towards 0.5 to prevent extreme sustained drifts in mock data
        # drift_to_mean = (0.5 - yes_price) * 0.01 
        # yes_price += change + drift_to_mean
        yes_price += change
        
        yes_price = np.clip(yes_price, 0.01, 0.99) # Clamp price between 1% and 99%
        yes_price = round(yes_price, 2)

    df = pd.DataFrame({
        'date': dates,
        f'{market_id}_yes_price': yes_prices,
        f'{market_id}_no_price': no_prices,
        f'{market_id}_volume': volumes
    })
    return df

# --- Example Usage (for testing this file directly) ---
if __name__ == "__main__":
    print("--- Mock Market Details ---")
    print(get_mock_market_details("market1"))
    print(get_mock_market_details("market_non_existent"))
    
    print("\n--- Mock Historical Prices ---")
    historical_df_market1 = get_mock_historical_prices("market1", days=30)
    print(f"\nMarket1 Data (first 5 rows of {len(historical_df_market1)}):")
    print(historical_df_market1.head())

    historical_df_market_new = get_mock_historical_prices("some_new_market", days=10)
    print(f"\nNew Market Data (first 5 rows of {len(historical_df_market_new)}):")
    print(historical_df_market_new.head())