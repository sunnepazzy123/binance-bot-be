# auto-generated snapshot
from peewee import *
import datetime
import peewee
import uuid


snapshot = Snapshot()


@snapshot.append
class User(peewee.Model):
    id = UUIDField(default=uuid.uuid4, primary_key=True)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    password = CharField(max_length=255, null=True)
    picture = CharField(max_length=255, null=True)
    provider = CharField(max_length=255, null=True)
    class Meta:
        table_name = "user"


@snapshot.append
class KeyVault(peewee.Model):
    id = UUIDField(default=uuid.uuid4, primary_key=True)
    api_key = CharField(max_length=255)
    api_secret = CharField(max_length=255)
    environment = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    user = snapshot.ForeignKeyField(backref='keyvault', index=True, model='user', on_delete='CASCADE')
    class Meta:
        table_name = "keyvault"


def migrate_forward(op, old_orm, new_orm):
    op.create_table(new_orm.keyvault)
    op.run_data_migration()


def migrate_backward(op, old_orm, new_orm):
    op.run_data_migration()
    op.drop_table(old_orm.keyvault)
