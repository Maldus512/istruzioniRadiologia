from migrate.versioning import api
from radiologia.config import BaseConfig as c
api.upgrade(c.SQLALCHEMY_DATABASE_URI, c.SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(c.SQLALCHEMY_DATABASE_URI, c.SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))