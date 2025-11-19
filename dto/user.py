
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="sunny@admin.com")  # <-- default example for Swagger
    password: str = Field(..., example="123456")
    first_name: str = Field(..., example="sunday")
    last_name: str = Field(..., example="odibo")


class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="sunny@admin.com")
    password: str = Field(..., example="123456")


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
