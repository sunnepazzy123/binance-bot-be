import asyncio
from peewee import DoesNotExist
from fastapi import HTTPException
from pydantic import ValidationError


async def run_sync(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
   
   

def raise_format_error(e: ValidationError, title: str = '') -> str:
    # Join all error messages into a single string
    if isinstance(e, ValidationError):
        errors = e.errors()  # Get all validation errors
        messages = [f"{error['loc'][0]}: {error['msg']}" for error in errors]
        # Handle validation errors
        formatted_message = ", ".join(messages)
        raise HTTPException(
            status_code=400, detail=f"Validation errors: {formatted_message}"
        )
    elif isinstance(e, DoesNotExist):
        raise HTTPException(status_code=400, detail=f"Does not exist..")
    else:
        # Handle generic exceptions
        raise HTTPException(status_code=400, detail=f"{title} Error: {str(e)}")

