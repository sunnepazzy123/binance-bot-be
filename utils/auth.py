import bcrypt 
import re

from fastapi import HTTPException, Request

from utils.jwt import verify_token

# Function to hash the password using bcrypt
def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Function to verify password during login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



def validate_password(password: str) -> bool:
    """Validate the password to contain at least one lowercase letter, 
    one uppercase letter, one digit, and one special character."""
    
    # Define the regex pattern
    pattern = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    )
    
    if pattern.match(password):
        return True
    else:
        return False
    
def get_current_user(request: Request):
    # 1. Try cookie first
    token = request.cookies.get("access_token")

    # 2. Fallback to Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header:
            parts = auth_header.split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    # 3. Verify token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # 4. Attach the user info to request.state
    request.state.user = payload["id"]

    return payload  # or fetch full user from DB if needed