from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class TradingPairCreate(BaseModel):
    symbol: str = Field(..., example="BTCUSDT")                # Trading pair
    quote: str = Field(..., example="USDT")                   # Quote currency
    threshold: float = Field(..., example=0.98)               # Buy threshold
    quantity: float = Field(..., example=0.1)                 # Trade quantity
    window: int = Field(..., example=10)                      # Window size for signals
    cooldown_seconds: int = Field(..., example=300)           # Cooldown between trades
    stop_loss: float = Field(..., example=0.01)               # Stop loss percentage
    take_profit: float = Field(..., example=0.02)             # Take profit percentage
    max_volatility: float = Field(..., example=0.02)          # Max allowed volatility
    user: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "symbol": "BTCUSDT",
                "quote": "USDT",
                "threshold": 0.98,
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
    threshold: float
    quantity: float
    window: int
    cooldown_seconds: int
    stop_loss: float
    take_profit: float
    max_volatility: float
    

class TradingPairLookup(BaseModel):
    id: Optional[UUID] = None
    symbol: Optional[str] = None

    def to_param(self) -> dict:
        if self.id:
            return {"id": self.id}
        if self.symbol:
            return {"symbol": self.symbol}
        raise ValueError("Either id or symbol must be provided")
    
