from colorama import Fore
import numpy as np
import pandas as pd
from config.index import MAX_VOLATILITY



def init_price_dataframe() -> pd.DataFrame:
    """Initialize an empty DataFrame for price data."""
    return pd.DataFrame({
        'time': pd.Series(dtype='datetime64[ns]'),
        'symbol': pd.Series(dtype='str'),
        'price': pd.Series(dtype='float')
    })

def get_base(symbol: str, quote: str) -> str:
    """Extract base asset from the symbol (e.g. BTCUSDT, USDT -> BTC)."""
    return symbol.replace(quote, '')


# === VOLATILITY CHECK ===
def is_market_stable(recent_prices: list, symbol: str = None) -> bool:
    print("DEBUG recent_prices raw =", recent_prices)  # <--- ADD THIS
    # Ensure price list contains only floats
    try:
        recent_prices = [float(p) for p in recent_prices]
    except Exception as e:
        print("❌ recent_prices contains invalid values:", recent_prices, e)
        return False

    if len(recent_prices) < 2:
        return False

    num_points = len(recent_prices)

    avg_price = np.mean(recent_prices)
    std_price = np.std(recent_prices)
    volatility = std_price / avg_price if avg_price > 0 else 0.0

    if symbol:
        vol_color = Fore.CYAN if volatility < MAX_VOLATILITY else Fore.YELLOW
        print(
            vol_color
            + f"{symbol}: last_recents={num_points}, avg_price={avg_price:.2f}, "
              f"std_price={std_price:.2f}, volatility={volatility:.4f}"
            + Fore.RESET
        )
    return volatility < MAX_VOLATILITY
