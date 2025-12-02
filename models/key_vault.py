from datetime import datetime
from typing import List
import uuid
from fastapi import HTTPException
from peewee import CharField, UUIDField, ForeignKeyField, DateTimeField
from dto.key_vault import APIKeyCreate, APIKeyUpdate
from models.index import BaseModel
from models.user import User
from connection.index import database
from utils.index import encrypt_secret
from peewee import BooleanField

class KeyVault(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    api_key = CharField()
    api_secret = CharField()
    environment = CharField()
    created_at = DateTimeField(default=datetime.utcnow)
    # New columns
    status = CharField(max_length=50, null=True, default="active")
    enabled = BooleanField(null=True, default=True)
    # One-to-many relation (User → TradingPairs)
    user = ForeignKeyField(User, backref="keyvault", on_delete="CASCADE")
    
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
    def create_keyVault(cls, dto: APIKeyCreate) -> dict:
        
        # Encrypt and store in DTO
        dto.api_key = encrypt_secret(dto.api_key)
        dto.api_secret = encrypt_secret(dto.api_secret)

        # Decrypt the same value that was stored
        dto_copy = dto.model_dump()
        
        with database.atomic():
            try:
                keyvault_created = cls.create(**dto_copy)
                return keyvault_created.__data__
            except Exception as e:
                raise HTTPException(status_code=400, detail=e)
                
                
    @classmethod
    def update_keyVault(cls, id: uuid.UUID, dto: APIKeyUpdate) -> dict:
        try:
            data = dto.model_dump(exclude_unset=True)

            # Encrypt fields if they are being updated
            if "api_key" in data:
                data["api_key"] = encrypt_secret(data["api_key"])

            if "api_secret" in data:
                data["api_secret"] = encrypt_secret(data["api_secret"])
                
            # Update only if the key belongs to the user
            rows_modified = (
                cls.update(**data)
                .where((cls.id == id) & (cls.user == dto.user))
                .execute()
            )

            if rows_modified == 0:
                raise HTTPException(
                    status_code=404,
                    detail="KeyVault entry not found for this user"
                )

            # Fetch updated record
            updated = cls.get((cls.id == id) & (cls.user == dto.user))
            return updated.__data__

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))