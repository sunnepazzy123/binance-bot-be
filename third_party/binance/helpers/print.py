from colorama import Fore

from dto.trading_pairs import TradeOrderInfo


def price_color(current_price: float, previous_price: float) -> str:
    if current_price > previous_price:
        return Fore.GREEN
    elif current_price < previous_price:
        return Fore.RED
    return Fore.WHITE


def print_price_update(time, symbol, current_price, color, volatility):
    print(color + f"{time} | {symbol} | Price: {current_price} | Volatility: {volatility:.4f}")

def print_trade_order(info: TradeOrderInfo):
    """Pretty-print a trade order (buy or sell) using the TradeOrderInfo dataclass."""
    if info.percent_change < 0:
        info_msg = "above"
    elif info.percent_change == 0:
        info_msg = "exact"
    else:
        info_msg = "below"

    print(
        Fore.CYAN +
        f"\n🔹 Condition met! Current: {info.current_price:.2f} "
        f"is {info.percent_change:.1f}% {info_msg} average {info.avg_price:.2f}"
    )
    print(
        (Fore.GREEN if info.side.upper() == "BUY" else Fore.MAGENTA) +
        f"🚀 Placing testnet {info.side.upper()} order for {info.quantity} {info.base}…"
    )


