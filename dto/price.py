from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class PriceCreate(BaseModel):
    symbol: str = Field(..., example="BTCUSDT")
    price: float = Field(..., example=93056.89)
    user: Optional[str] = None
    

class PriceRead(BaseModel):
    id: UUID
    symbol: str
    price: float
    timestamp: datetime
    user: UUID

    class Config:
        orm_mode = True  # allows reading from Peewee model directly
