from datetime import datetime
from typing import List
import uuid
from fastapi import HTTPException
from peewee import CharField, UUIDField, FloatField, IntegerField, ForeignKeyField, DateTimeField
from dto.order import OrderCreate
from models.index import BaseModel
from models.user import User
from connection.index import database


class Order(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    symbol = CharField()
    side = CharField()
    price = FloatField()
    quantity = FloatField()
    avg_price = FloatField()
    threshold = FloatField()
    percent_change = FloatField()
    timestamp = DateTimeField(default=datetime.utcnow)
    result = CharField(default="success")
    # One-to-many relation (User → TradingPairs)
    user = ForeignKeyField(User, backref="orders", on_delete="CASCADE")
    
    # --- READ ALL ---
    @classmethod
    def findAll(cls) -> List[dict]:
        fields = [field for field in cls._meta.fields.values()]
        return list(cls.select(*fields).dicts())

    # --- READ ALL BY USER ---
    @classmethod
    def findAllByUser(cls, userId: str) -> List[dict]:
        return list(cls.select().where(cls.user == userId).dicts())

    # --- CREATE ---
    @classmethod
    def create_order(cls, dto: OrderCreate) -> dict:
        
        order_copy = dto.model_dump()
        
        with database.atomic():
            try:
                order_created = cls.create(**order_copy)
                return order_created.__data__
            except Exception as e:
                raise HTTPException(status_code=400, detail=e)
                
