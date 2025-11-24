from fastapi import APIRouter, Depends, HTTPException, Request

from dto.key_vault import APIKeyCreate, APIKeyRead
from models.key_vault import KeyVault
from utils.auth import get_current_user
from utils.index import raise_format_error, run_sync

router = APIRouter(
    tags=["Key Vault"],
    prefix="/key_vaults",
    dependencies=[Depends(get_current_user)]  # ensures auth
)


# Create API key
@router.post("/api-keys", response_model=APIKeyRead)
async def create_api_key(dto: APIKeyCreate, request: Request):
    try:
        dto.user = request.state.user
        keyvault = await run_sync(lambda: KeyVault.create_keyVault(dto))
        # Convert each dict to Pydantic UserRead
        return APIKeyRead.model_validate(keyvault)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")


# Get all keys for a user
@router.get("/", response_model=APIKeyRead)
async def get_trading_pair(request: Request):
    try:
        user = request.state.user
        keyvaults = await run_sync(lambda: KeyVault.findAllByUser(user))
        return [APIKeyRead.model_validate(u) for u in keyvaults]
    except Exception as e:
        raise_format_error(e)
        
