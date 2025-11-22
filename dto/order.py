from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel

class OrderCreate(BaseModel):
    symbol: str
    side: str
    price: float
    avg_price: float
    quantity: float
    threshold: float
    percent_change: float
    user: str  # link to User

    class Config:
        orm_mode = True
        
        
class OrderRead(BaseModel):
    id: UUID  # UUID as string
    symbol: str
    side: str
    price: float
    quantity: float
    avg_price: float
    threshold: float
    percent_change: float
    timestamp: datetime  # ISO formatted string
    result: str
    user: UUID

    class Config:
        orm_mode = True


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

