#!flask/bin/python
from migrate.versioning import api
import migrate
from radiologia.config import BaseConfig as c
from radiologia.config import TestingConfig as tc
from radiologia import db
import os.path
db.create_all()
#if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
try:
    api.create(c.SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(c.SQLALCHEMY_DATABASE_URI, c.SQLALCHEMY_MIGRATE_REPO)
except migrate.exceptions.KnownError:
    print("base database already exists")
#else:
#    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))