from dotenv import load_dotenv
# Load env file
load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI 
from connection.setup import create_tables
from middlewares.setup_cors import setup_cors
from swagger.index import custom_openapi
from connection.index import database
from middlewares.index import HTTPSRedirectFixMiddleware, log_requests
from routes.index import register_routers
from starlette.middleware.sessions import SessionMiddleware
from config.env_config import configLoaded




                  
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
app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",          # Swagger docs
    openapi_url="/api/openapi.json" # OpenAPI JSON
    )

# FIX: Proper HTTPS handling behind NGINX
app.add_middleware(HTTPSRedirectFixMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=configLoaded.SESSION_SECRET_KEY,
    https_only=False,  # True in production
    max_age=3600,
)

# Setup CORS using the function
setup_cors(app)  # or use ["*"] for all

app.middleware('http')(log_requests)
app.openapi = lambda: custom_openapi(app)

