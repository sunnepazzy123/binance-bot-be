from peewee import Model
from connection.index import database as db

class BaseModel(Model):
    class Meta:
        database = db