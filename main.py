from contextlib import asynccontextmanager
from fastapi import FastAPI 
from connection.setup import create_tables
from middlewares.setup_cors import setup_cors
from swagger.index import custom_openapi
from connection.index import database
from middlewares.index import log_requests
from routes.index import register_routers

                  
# Defining the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform startup tasks
    print("Application is starting up.")
    
    if database.is_closed():
        database.connect()
        create_tables(database)
               
    register_routers(app)
    # Yield control back to FastAPI
    yield

    # Perform shutdown tasks
    print("Application is shutting down.")
    if not database.is_closed():
        database.close()

# Initializing the
app = FastAPI(lifespan=lifespan)

# Setup CORS using the function
setup_cors(app)  # or use ["*"] for all

app.middleware('http')(log_requests)
app.openapi = lambda: custom_openapi(app)

