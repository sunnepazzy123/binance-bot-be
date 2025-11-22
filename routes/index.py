from fastapi import FastAPI
from routes import bot, order, user, trading_pair, auth, price


def register_routers(app: FastAPI):
    app.include_router(user.router, prefix="/api")
    app.include_router(trading_pair.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
    app.include_router(price.router, prefix="/api")
    app.include_router(bot.router, prefix="/api")
    app.include_router(order.router, prefix="/api")
    
    
    

    
   
   
