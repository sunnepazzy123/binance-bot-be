from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request
from dto.key_vault import APIKeyCreate, APIKeyRead, APIKeyUpdate
from models.key_vault import KeyVault
from utils.auth import get_current_user
from utils.index import decrypt_secret, raise_format_error, run_sync

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


@router.put("/api-keys/{id}", response_model=APIKeyRead)
async def update_api_key(id: UUID, dto: APIKeyUpdate, request: Request):
    try:
        # Ensure the key belongs to the logged-in user
        user = request.state.user
        dto.user = user

        keyvault = await run_sync(lambda: KeyVault.update_keyVault(id, dto))

        # Decrypt before returning
        keyvault["api_key"] = decrypt_secret(keyvault["api_key"])
        keyvault["api_secret"] = decrypt_secret(keyvault["api_secret"])

        return APIKeyRead.model_validate(keyvault)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating API key: {e}")

# Get all keys for a user
@router.get("/", response_model=List[APIKeyRead])
async def get_key_vault_key(request: Request):
    try:
        user = request.state.user
        keyvaults = await run_sync(lambda: KeyVault.findAllByUser(user))
        # Decrypt api_key + api_secret for each entry
        decrypted_list = []
        for item in keyvaults:
            item["api_key"] = decrypt_secret(item["api_key"])
            item["api_secret"] = decrypt_secret(item["api_secret"])
            decrypted_list.append(APIKeyRead.model_validate(item))

        return decrypted_list
    except Exception as e:
        raise_format_error(e)
        
