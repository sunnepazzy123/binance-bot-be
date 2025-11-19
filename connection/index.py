from peewee import PostgresqlDatabase
from constant.index import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


# Initialize the PostgreSQL database connection using env vars
database = PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)