from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class APIKeyCreate(BaseModel):
    user: Optional[str] = None
    api_key: str = Field(..., example="vdgsdgs62bnn2283829")
    api_secret: str = Field(..., example="vdgsdgs62bnn2283829")
    environment: str = Field(..., example="development")
    
    
class APIKeyUpdate(BaseModel):
    user: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    environment: Optional[str] = None
    status: Optional[str] = None
    enabled: Optional[bool] = None


class APIKeyRead(BaseModel):
    id: UUID
    user: UUID
    api_key: str
    api_secret: str
    environment: str
    created_at: datetime
    status: str
    enabled: bool