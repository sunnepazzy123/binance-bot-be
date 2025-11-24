import decimal
import math
from colorama import Fore
import numpy as np
import pandas as pd
from config.index import MAX_VOLATILITY
from binance import AsyncClient



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



async def calculate_quantity(client, symbol: str, balance: float, allocation_percent: float, price: float):
    step_size = await get_step_size(client, symbol)

    # Convert percent (example: 10 → 0.10)
    usable_balance = balance * (allocation_percent / 100)

    # Unrounded quantity
    raw_qty = usable_balance / price

    # Apply Binance step size rules
    qty = apply_step_size(raw_qty, step_size)

    return qty



async def get_step_size(client: AsyncClient, symbol: str) -> float:
    info = await client.get_symbol_info(symbol)

    for f in info["filters"]:
        if f["filterType"] == "LOT_SIZE":
            return float(f["stepSize"])

    raise ValueError(f"Step size not found for {symbol}")


def apply_step_size(quantity: float, step_size: float) -> float:
    decimals = abs(decimal.Decimal(str(step_size)).as_tuple().exponent)
    q = math.floor(quantity / step_size) * step_size
    return float(f"{q:.{decimals}f}")


async def get_current_price(client: AsyncClient, symbol: str) -> float:
    """
    Fetch latest market price using Binance ticker API.
    """
    ticker = await client.get_symbol_ticker(symbol=symbol)
    return float(ticker["price"])