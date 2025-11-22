
DEFAULT_TAKE_PROFIT = 0.02   # 2% take-profit
DEFAULT_STOP_LOSS = 0.01     # 1% stop-loss
THRESHOLD = 0.98         # buy when price drops 2% below moving average
WINDOW = 10                   # moving average window
MAX_VOLATILITY = 0.02         # max allowed volatility (2%)
SYMBOL = "BTCUSDT"
QUOTE = "USDT"
QUANTITY = 0.1
COOLDOWN_SECONDS = 60 * 5     # 5 minutes between trades per symbol
ROLLING_WINDOW = 1000         # how many past prices to fetch from DB
SIMULATE = True               # True = testnet/simulated orders, False = live trading

JWT_ALGORITHM = "HS256"
