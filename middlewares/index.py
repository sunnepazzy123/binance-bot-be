from fastapi import Request
import time
from utils.jwt import verify_token
from fastapi import Request, HTTPException
from functools import wraps
from starlette.middleware.base import BaseHTTPMiddleware



async def log_requests(request: Request, call_next):
    print(f"imcoming log request:")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url} - {process_time:.2f}s")
    return response


# This is the auth middleware
def auth_middleware(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Ensure we are passing request as an argument to the wrapped function
        request: Request = kwargs.get("request")  # Fetch the request from kwargs
        if not request:
            # If we cannot find the request in kwargs, try getting it from args
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")

        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return HTTPException(status_code=401, detail="Authorization header missing")

        # Verify Bearer token
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            return HTTPException(status_code=401, detail="Authorization method must be Bearer")

        token = parts[1]
        if not verify_token(token):  # You need to have `verify_token` function defined somewhere
            return HTTPException(status_code=401, detail="Invalid token")

        # Proceed to the next handler if token is verified
        return await func(*args, **kwargs)

    return wrapper


# This is the role middleware
def role_middleware(required_role: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")  # Access the request from kwargs
            if not request:
                # If request isn't found in kwargs, search in args
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if not request:
                raise HTTPException(status_code=400, detail="Request object not found")

            # Auth header check
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return HTTPException(status_code=401, detail="Invalid Authorization...")

            parts = auth_header.split(" ")
            if len(parts) != 2 or parts[0] != "Bearer":
                return HTTPException(status_code=401, detail="Authorization method must be Bearer")

            token = parts[1]
            verified = verify_token(token)
            if not verified:
                return HTTPException(status_code=401, detail="Not verified token.")

            # Extract user data
            userid = verified["id"]
            role = verified.get("role")

            request.state.userid = userid
            request.state.role = role

            if required_role and role != required_role:
                raise HTTPException(status_code=401, detail="Insufficient role")

            return await func(*args, **kwargs)

        return wrapper
    return decorator





class HTTPSRedirectFixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Force FastAPI to treat requests as HTTPS when behind NGINX reverse proxy
        if request.headers.get("x-forwarded-proto") == "https":
            request.scope["scheme"] = "https"
        return await call_next(request)
