import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
import pandas as pd
from binance import AsyncClient

class TradingPairCreate(BaseModel):
    symbol: str = Field(..., example="BTCUSDT")                # Trading pair
    quote: str = Field(..., example="USDT")                   # Quote currency
    buy_threshold: float = Field(..., example=0.98)               # Buy threshold
    sell_threshold: float = Field(..., example=1.02)               # Sell threshold
    quantity: float = Field(..., example=0.1)                 # Trade quantity
    window: int = Field(..., example=10)                      # Window size for signals
    cooldown_seconds: int = Field(..., example=300)           # Cooldown between trades
    stop_loss: float = Field(..., example=0.01)               # Stop loss percentage
    take_profit: float = Field(..., example=0.02)             # Take profit percentage
    max_volatility: float = Field(..., example=0.02)          # Max allowed volatility
    user: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "BTCUSDT",
                "quote": "USDT",
                "buy_threshold": 0.98,
                "sell_threshold": 1.02,
                "quantity": 0.1,
                "window": 10,
                "cooldown_seconds": 300,
                "stop_loss": 0.01,
                "take_profit": 0.02,
                "max_volatility": 0.02
            }
        }



class TradingPairRead(BaseModel):
    id: UUID
    user: UUID
    symbol: str
    quote: str
    buy_threshold: float
    sell_threshold: float
    quantity: float
    window: int
    cooldown_seconds: int
    stop_loss: float
    take_profit: float
    max_volatility: float
    

@dataclass
class StreamParams:
    """Holds all shared parameters for the Binance WebSocket stream."""
    symbol: str
    quote: str
    quantity: float
    buy_threshold: float
    sell_threshold: float
    price_data: pd.DataFrame
    window: int
    cooldown_seconds: int
    client: AsyncClient
    stop_streaming_flag: Dict[str, bool]
    balance: float
    active_tasks: List[asyncio.Task] = field(default_factory=list)
    config: Dict = field(default_factory=dict)
    max_volatility: float = 0.02  # ✅ also fixed here
    current_price: float = None
    last_trade_time: datetime = None  # keeps track of the last executed trade
    user: str = None
    
@dataclass
class TradeOrderInfo:
    base: str
    quantity: float
    current_price: float
    avg_price: float
    percent_change: float   # positive value, works for buy or sell
    side: str               # 'BUY' or 'SELL'
