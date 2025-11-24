import asyncio
from datetime import datetime
import logging
from colorama import Fore
import numpy as np
import pandas as pd
from dto.order import OrderCreate, OrderSide
from dto.trading_pairs import StreamParams, TradeOrderInfo, TradingPairCreate
from models.order import Order
from models.trading_pair import TradingPair
from third_party.binance.binance import connect_binance, get_account_balance
from config.env_config import configLoaded
from third_party.binance.helpers.print import price_color, print_price_update, print_trade_order
from third_party.binance.util import calculate_quantity, get_current_price, init_price_dataframe, is_market_stable
from binance import BinanceSocketManager
from collections import deque
from third_party.binance.config import bot_status


# --- Configurable constants ---
MAX_DF_ROWS = 1000
WS_RECV_TIMEOUT = 10  # seconds to wait for ws.recv before checking stop-flag / reconnect logic
RECONNECT_BASE_DELAY = 1.0
RECONNECT_MAX_DELAY = 60.0

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("trading-bot")


async def start_bot_dynamic(body: TradingPairCreate):
        symbol = body.symbol
        bot_status[symbol] = {"status": "running", "last_trade": None}
        
        client, _ = await connect_binance(
                    api_key=configLoaded.TEST_API_KEY,
                    api_secret=configLoaded.TEST_SECRET_KEY,
                    environment=configLoaded.ENVIRONMENT
                    )
        # get user/trading config
        trading_pair = TradingPair.findOneBySymbol(body.symbol, body.user)
        if not trading_pair:
            logger.error("Trading pair not found for symbol %s user %s", body.symbol, body.user)
            return
        
        balance = await get_account_balance(client, body.quote)
        print(Fore.GREEN + f"💰 {body.quote} balance: {balance}")
        
        # state & params
        price_data = init_price_dataframe()
        stop_flag = {"stop": False}
        
        params = StreamParams(
            symbol=body.symbol,
            quote=trading_pair["quote"],
            quantity=trading_pair["quantity"],
            buy_threshold=trading_pair["buy_threshold"],
            sell_threshold=trading_pair["sell_threshold"],
            price_data=price_data,
            client=client,
            stop_streaming_flag=stop_flag,
            window=trading_pair["window"],
            cooldown_seconds=trading_pair["cooldown_seconds"],
            active_tasks=[],
            config=trading_pair,
            max_volatility=trading_pair["max_volatility"],
            user=trading_pair["user"],
            last_trade_time=None,  # Track last trade
            balance=1000.0
        )
        # rolling buffer for recent prices (fast mean/volatility calc)
        # will contain floats, maintain up to params.window items
        recent_buffer = deque(maxlen=params.window or 50)
        reconnect_delay = RECONNECT_BASE_DELAY
        
        while not params.stop_streaming_flag.get("stop"):
            try:
                bsm = BinanceSocketManager(client)
                socket = bsm.symbol_ticker_socket(params.symbol)

                async with socket as ws:
                    logger.info("Connected to websocket for %s", params.symbol)
                    reconnect_delay = RECONNECT_BASE_DELAY  # reset backoff on success

                    while True:
                        # check stop flag often
                        if params.stop_streaming_flag.get("stop"):
                            logger.warning("Stop flag set, closing websocket for %s", params.symbol)
                            return

                        try:
                            # Wait for a message but don't hang forever
                            msg = await asyncio.wait_for(ws.recv(), timeout=WS_RECV_TIMEOUT)
                        except asyncio.TimeoutError:
                            # periodic check to see if we should stop; continue loop to re-await
                            continue
                        except Exception as e:
                            # some underlying network error, raise to outer reconnect logic
                            raise

                        # validate message
                        if not msg or "c" not in msg:
                            logger.error("Invalid message received (no 'c'): %s", msg)
                            # continue rather than crash; if it's a malformed stream we may want to reconnect
                            continue

                        # Add current price to params + update in-memory buffer
                        add_current_price_to_params(msg, params, recent_buffer)

                        # Evaluate signals (await the async function)
                        try:
                            executed = await evaluate_trade_signals(params, recent_buffer)
                            if executed:
                                # if trade executed you may want to trigger cooldowns, notifications, etc.
                                bot_status[symbol.upper()]["last_trade"] = datetime.utcnow()
                            logger.info("%s executed trade for %s", Fore.GREEN, params.symbol)
                        except Exception as e:
                            # signal eval should never crash the loop
                            logger.exception("Error in evaluate_trade_signals: %s", e)

            except Exception as e:
                # handle websocket/client errors with backoff and reconnect
                logger.exception("WebSocket or network error for %s: %s", params.symbol, e)
                if params.stop_streaming_flag.get("stop"):
                    logger.info("Stop flag set, exiting reconnect loop.")
                    return

                logger.info("Reconnecting in %.1f seconds...", reconnect_delay)
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, RECONNECT_MAX_DELAY)
                continue

        logger.info("Exiting start_bot_dynamic for %s", params.symbol)



def add_current_price_to_params(msg: dict, params: StreamParams, recent_buffer: deque) -> StreamParams:    
    # --- Extract timestamp safely ---
    event_time = msg.get("E")
    current_price = float(msg["c"])
    
    if isinstance(event_time, (int, float)):
        timestamp = pd.to_datetime(event_time, unit="ms")
    else:
        # fallback to now
        timestamp = pd.Timestamp.utcnow()

    # --- Store clean row ---
    params.price_data.loc[len(params.price_data)] = [
        timestamp,
        msg.get("s", params.symbol),
        current_price,
    ]

    # --- Append FLOAT price to deque (important!) ---
    recent_buffer.append(current_price)

    # --- Volatility calculation ---
    calculate_volatility_and_print(params, current_price, timestamp)

    params.current_price = current_price
    return params



# === SIGNAL CHECK ===
async def evaluate_trade_signals(params: StreamParams, recent_buffer: deque):
    current_price = params.current_price
    executed = False  # <- initialize here
    
    # Cooldown check
    now = datetime.utcnow()
    if params.last_trade_time:
        elapsed = (now - params.last_trade_time).total_seconds()
        if elapsed < params.cooldown_seconds:
            print(Fore.YELLOW + f"{params.symbol}: ⏳ Cooldown active ({elapsed:.1f}/{params.cooldown_seconds}s)")
            return False

    if len(recent_buffer) < 5:
        print(Fore.YELLOW + f"{params.symbol}: ⏳ Waiting for more data...")
        return False

    # Volatility check
    if not is_market_stable(list(recent_buffer), params.symbol):
        print(Fore.YELLOW + f"{params.symbol}: ⚠ Market too volatile, skipping trade.")
        return False

    avg_price = np.mean(list(recent_buffer))
    percent_change = ((current_price - avg_price) / avg_price) * 100
    
    # --- BUY ---
    if current_price < avg_price * params.buy_threshold:
        executed = await execute_order(params, current_price, avg_price, percent_change, OrderSide.BUY.value)

    # --- SELL ---
    if current_price > avg_price * params.sell_threshold:
        executed = await execute_order(params, current_price, avg_price, percent_change, OrderSide.SELL.value)

    return executed



def calculate_volatility_and_print(params, current_price, timestamp):
    """
    Calculate price volatility, determine color, print the update, and update current_price.
    """
    if len(params.price_data) > 1:
        previous_price = float(params.price_data.iloc[-2]["price"])
        volatility = abs(current_price - previous_price) / previous_price if previous_price > 0 else 0.0
        color = price_color(current_price, previous_price)
    else:
        previous_price = None
        volatility = 0.0
        color = Fore.WHITE

    print_price_update(timestamp, params.symbol, current_price, color, volatility)
    params.current_price = current_price

    return previous_price, volatility, color
        

async def execute_order(params: StreamParams, current_price: float, avg_price: float, percent_change: float, side: str) -> bool:
    info = TradeOrderInfo(
        base=params.symbol,
        quantity=params.quantity,
        current_price=current_price,
        avg_price=avg_price,
        percent_change=abs(percent_change),
        side=side
    )
    print_trade_order(info)

    try:
        quantity = await calculate_quantity(
            client=params.client,
            symbol=params.symbol,
            balance=params.balance,
            allocation_percent=10,
            price=params.current_price,
        )
        if side == OrderSide.BUY.value:
            order = await params.client.order_market_buy(symbol=params.symbol, quantity=quantity)
        else:
            order = await params.client.order_market_sell(symbol=params.symbol, quantity=quantity)

        order_dto = OrderCreate(
            symbol=params.symbol,
            side=side,
            price=current_price,
            avg_price=avg_price,
            quantity=quantity,
            percent_change=abs(percent_change),
            threshold=params.buy_threshold if side == OrderSide.BUY.value else params.sell_threshold,
            user=str(params.user)
        )
        Order.create_order(order_dto)
        print(Fore.GREEN + f"{params.symbol}: ✅ {side} executed successfully!")
        print(Fore.WHITE + str(order))
        params.last_trade_time = datetime.utcnow()
        return True
    except Exception as e:
        print(Fore.RED + f"{params.symbol}: ⚠ {side} failed: {e}")
        return False