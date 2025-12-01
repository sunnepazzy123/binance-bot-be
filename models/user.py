from connection.index import database
from typing import List
import uuid
from fastapi import HTTPException
from peewee import CharField, UUIDField
from dto.user import GoogleIdTokenPayload, UserCreate, UserUpdate
from models.index import BaseModel
from utils.auth import hash_password
from utils.index import raise_format_error

class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField(null=True, default=None)   # ⬅️ allow NULL
    picture = CharField(null=True, default=None)   # ⬅️ allow NULL
    provider = CharField(null=True, default=None)
    

    # --- READ ALL ---
    @classmethod
    def findAll(cls) -> List[dict]:
        fields = [field for field in cls._meta.fields.values() if field.name != "password"]
        return list(cls.select(*fields).dicts())

    # --- CREATE ---
    @classmethod
    def create_user(cls, user: UserCreate) -> dict:
        if cls.select().where(cls.email == user.email).exists():
            raise HTTPException(status_code=400, detail="User already exists")
        
        hashed_password = hash_password(user.password)
        user_dict = user.model_dump()
        user_dict["password"] = hashed_password
        
        with database.atomic():
            try:
                new_user = cls.create(**user_dict)
                return new_user.__data__
            except Exception as e:
                raise_format_error(e, "creating user")

    # --- READ ONE ---
    @classmethod
    def findOne(cls, id: int) -> dict | None:
        fields = [field for field in cls._meta.fields.values() if field.name != "password"]
        user = cls.select(*fields).where(cls.id == id).get_or_none()
        return user.__data__ if user else None

    # --- UPDATE ---
    @classmethod
    def update_user(cls, id: uuid.UUID, user_data: UserUpdate) -> dict:
        with database.atomic():
            user = cls.get_or_none(cls.id == id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            # Convert Pydantic model to dict, only including fields actually provided
            update_data = user_data.model_dump(exclude_unset=True)

            if not update_data:
                raise HTTPException(status_code=400, detail="No fields provided to update")

            # Hash password if present
            if "password" in update_data:
                update_data["password"] = hash_password(update_data["password"])

            # Check email uniqueness if present
            if "email" in update_data:
                print("Checking email uniqueness for:", update_data["email"])
                if cls.select().where(cls.email == update_data["email"], cls.id != id).exists():
                    raise HTTPException(status_code=400, detail="Email already in use")


            cls.update(**update_data).where(cls.id == id).execute()

            # Return updated user without password
            fields = [f for f in cls._meta.fields.values() if f.name != "password"]
            updated_user = cls.select(*fields).where(cls.id == id).get()
            return updated_user.__data__


    # --- DELETE ---
    @classmethod
    def delete_user(cls, id: uuid.UUID) -> dict:
        with database.atomic():
            existing_user = cls.get_or_none(cls.id == id)
            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found")
            try:
                existing_user.delete_instance()
                return {"detail": "User deleted successfully"}
            except Exception as e:
                raise_format_error(e, "deleting user")
                
    # --- UPSERT ---
    @classmethod
    def upsert_google_user(cls, userinfo: GoogleIdTokenPayload) -> dict:
        try:
            user, created = cls.get_or_create(
                email=userinfo.email,
                defaults={
                    "first_name": userinfo.given_name,
                    "last_name": userinfo.family_name,
                    "password": None,
                    "picture": userinfo.picture,
                },
            )

            if not created:
                updated = False
                if not user.first_name:
                    user.first_name = userinfo.given_name
                    updated = True
                if not user.last_name:
                    user.last_name = userinfo.family_name
                    updated = True
                if not user.picture:
                    user.picture = userinfo.picture
                    updated = True
                if updated:
                    user.save()

            return user.__data__  # ✅ Return dict for API
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"User upsert failed: {e}")