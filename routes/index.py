from fastapi import FastAPI
from routes import bot, order, user, trading_pair, auth, price, key_vault, account


def register_routers(app: FastAPI):
    app.include_router(user.router, prefix="/api")
    app.include_router(trading_pair.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
    app.include_router(price.router, prefix="/api")
    app.include_router(bot.router, prefix="/api")
    app.include_router(order.router, prefix="/api")
    app.include_router(key_vault.router, prefix="/api")
    app.include_router(account.router, prefix="/api")
    
    
    
    
    

    
   
   
