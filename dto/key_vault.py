from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class APIKeyCreate(BaseModel):
    user: Optional[str] = None
    api_key: str = Field(..., example="vdgsdgs62bnn2283829")
    api_secret: str = Field(..., example="vdgsdgs62bnn2283829")
    environment: str = Field(..., example="development")

class APIKeyRead(BaseModel):
    id: UUID
    user: UUID
    api_key: str
    api_secret: str
    environment: str
    created_at: datetime