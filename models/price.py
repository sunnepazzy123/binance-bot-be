from datetime import datetime
from typing import Dict, List
import uuid
from fastapi import HTTPException
from peewee import CharField, UUIDField, FloatField, DateTimeField, ForeignKeyField
from dto.trading_pairs import TradingPairCreate
from models.index import BaseModel
from models.user import User
from connection.index import database
import logging

logger = logging.getLogger(__name__)


class Price(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    symbol = CharField()
    timestamp = DateTimeField(default=datetime.utcnow)
    price = FloatField()
    # One-to-many relation (User → Prices)
    user = ForeignKeyField(User, backref="prices", on_delete="CASCADE")
    
    # --- READ ALL ---
    @classmethod
    def findAll(cls) -> List[dict]:
        fields = [field for field in cls._meta.fields.values()]
        return list(cls.select(*fields).dicts())
    
        # --- READ ONE ---
    @classmethod
    def findOne(cls, id: uuid.UUID) -> dict:
        fields = [field for field in cls._meta.fields.values()]

        record = cls.select(*fields).where(cls.id == id).dicts().first()

        if not record:
            raise HTTPException(status_code=404, detail="Trading pair not found")

        return record
    
    @classmethod
    def findOneBySymbol(cls, symbol: str, user: str) -> dict:
        fields = [field for field in cls._meta.fields.values()]

        record = cls.select(*fields).where((cls.symbol == symbol) & (cls.user == user)).dicts().first()

        if not record:
            raise HTTPException(status_code=404, detail="Trading pair not found")

        return record
    
    @classmethod
    def get_recent_prices(cls, symbol: str, n: int = 50) -> List[Dict]:
        try:
            query = (cls
                    .select(cls.timestamp, cls.price)
                    .where(cls.symbol == symbol)
                    .order_by(cls.timestamp.desc())
                    .limit(n))
            
            # Convert query result to list of dicts, oldest first
            results = [{"timestamp": p.timestamp, "price": p.price} for p in reversed(list(query))]
            return results
        except Exception as e:
            logger.exception("Failed to read recent prices: %s", e)
            return []
    
    # --- CREATE ---
    @classmethod
    def create_price(cls, dto: TradingPairCreate) -> dict:

        price_copy = dto.model_dump()
        
        with database.atomic():
            try:
                price_created = cls.create(**price_copy)
                return price_created.__data__
            except Exception as e:
                raise HTTPException(status_code=400, detail=e)
                
