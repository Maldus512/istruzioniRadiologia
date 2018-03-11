#!flask/bin/python
from migrate.versioning import api
from app.config import BaseConfig as c
from app import db
import os.path
db.create_all()
#if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
api.create(c.SQLALCHEMY_MIGRATE_REPO, 'database repository')
api.version_control(c.SQLALCHEMY_DATABASE_URI, c.SQLALCHEMY_MIGRATE_REPO)
#else:
#    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))