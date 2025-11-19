import uuid
from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from dto.user import UserRead, UserUpdate
from utils.auth import get_current_user
from utils.index import run_sync


router = APIRouter(
    tags=["Users"],
    prefix="/users",
    dependencies=[Depends(get_current_user)]  # ensures auth
)

# Route to get all users
@router.get("/", response_model=list[UserRead])
async def get_users():
    try:
        users = await run_sync(lambda: User.findAll())
        # Convert each dict to Pydantic UserRead
        return [UserRead.model_validate(u) for u in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")

# --- UPDATE USER ---
@router.patch("/{id}", response_model=UserRead)
async def update_user(id: uuid.UUID, dto: UserUpdate):
    try:
        # Only include fields that the client actually sent
        updated_user = await run_sync(lambda: User.update_user(id, dto))
        return UserRead.model_validate(updated_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}")

# --- DELETE USER ---
@router.delete("/{id}")
async def delete_user(id: uuid.UUID):
    try:
        result = await run_sync(lambda: User.delete_user(id))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {e}")