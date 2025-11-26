from fastapi import APIRouter, HTTPException, Response
from dto.user import UserCreate, UserLogin, UserRead
from models.user import User
from utils.auth import  verify_password
from utils.index import raise_format_error, run_sync
from utils.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_token
from peewee import DoesNotExist

router = APIRouter(
    tags=["Auth"],
    prefix="/auth",
)


@router.post("/login")
async def auth_user(user_login: UserLogin, response: Response):
        try:     
            user_record = User.get(User.email == user_login.email)
            
            if verify_password(user_login.password, user_record.password):
                data = {
                    "id": user_record.id,
                    "email": user_record.email
                }
                # jwt goes here          
                token = create_token(data)
                # Set HTTP-only cookie
                response.set_cookie(
                    key="access_token",
                    value=token,
                    httponly=True,
                    max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60,
                    samesite="lax",  # or "strict"
                    secure=False  # True if using HTTPS
                )
                return {
                    "access_token": token
                }
            else:
                raise HTTPException(status_code=401, detail="Invalid Email or Password.")
            
        except Exception as e:
            if isinstance(e, DoesNotExist):
                raise HTTPException(status_code=400, detail=f"User does not exist..")
            raise raise_format_error(e, "An error occurred during authentication.")


@router.post("/register", response_model=UserRead)
async def create_user(dto: UserCreate, response: Response):
    try:
        new_user = await run_sync(lambda: User.create_user(dto))
        data = {
            "id": new_user["id"],
            "email": new_user["email"]
        }
                        # jwt goes here          
        token = create_token(data)
        # Set HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60,
            samesite="lax",  # or "strict"
            secure=False  # True if using HTTPS
        )
        return UserRead.model_validate(new_user)
    except Exception as e:
        raise raise_format_error(e)

      
   
   
