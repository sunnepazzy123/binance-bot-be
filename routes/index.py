from fastapi import FastAPI
from routes import user, trading_pair, auth


def register_routers(app: FastAPI):
    app.include_router(user.router, prefix="/api")
    app.include_router(trading_pair.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")

    
   
   
