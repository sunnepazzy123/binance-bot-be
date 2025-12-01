from peewee import PostgresqlDatabase
from config.env_config import configLoaded

# Initialize the PostgreSQL database connection using env vars
database = PostgresqlDatabase(
    configLoaded.DB_NAME,
    user=configLoaded.DB_USER,
    password=configLoaded.DB_PASSWORD,
    host=configLoaded.DB_HOST,
    port=configLoaded.DB_PORT
)