from typing import List
import uuid
from fastapi import HTTPException
from peewee import CharField, UUIDField, FloatField, IntegerField, ForeignKeyField
from dto.trading_pairs import TradingPairCreate
from models.index import BaseModel
from models.user import User
from connection.index import database


class TradingPair(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    symbol = CharField(unique=True)
    quote = CharField()
    buy_threshold = FloatField(default=0.98)
    sell_threshold = FloatField(default=0.98)
    quantity = FloatField(default=0.0)
    window = IntegerField(default=10)
    cooldown_seconds = IntegerField(default=300)
    stop_loss = FloatField(default=0.01)
    take_profit = FloatField(default=0.02)
    max_volatility = FloatField(default=0.02)
    # One-to-many relation (User → TradingPairs)
    user = ForeignKeyField(User, backref="trading_pairs", on_delete="CASCADE")
    
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
    
    # --- CREATE ---
    @classmethod
    def create_trading_pair(cls, dto: TradingPairCreate) -> dict:
        # Correct condition: AND must use & operator
        exists = cls.select().where(
            (cls.symbol == dto.symbol) & (cls.user == dto.user)
        ).exists()

        if exists:
            raise HTTPException(status_code=400, detail="Symbol already exists for this user")

        trading_pair_dto = dto.model_dump()
        
        with database.atomic():
            try:
                new_trading_pair = cls.create(**trading_pair_dto)
                return new_trading_pair.__data__
            except Exception as e:
                raise HTTPException(status_code=400, detail=e)
                
    # --- UPSERT ---
    @classmethod
    def upsert_trading_pair(cls, dto: TradingPairCreate) -> dict:
        trading_pair_dto = dto.model_dump()

        with database.atomic():
            # Check if exists
            existing = cls.select().where(
                (cls.symbol == dto.symbol) & (cls.user == dto.user)
            ).first()

            if existing:
                # Update only provided fields
                query = cls.update(**trading_pair_dto).where(
                    cls.id == existing.id
                )
                query.execute()

                # Refresh object
                updated = cls.get_by_id(existing.id)
                return updated.__data__

            # Create new if not found
            new_trading_pair = cls.create(**trading_pair_dto)
            return new_trading_pair.__data__