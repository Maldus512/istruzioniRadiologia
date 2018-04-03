from radiologia.config import BaseConfig, TestingConfig
from radiologia import db, babel
from flask import Flask
from radiologia import app

def create_test_app():
    tapp = Flask(__name__)
    tapp.config.from_object(TestingConfig)
    # Dynamically bind SQLAlchemy to application
    db.init_app(tapp)
    babel.init_app(tapp)
    tapp.app_context().push() # this does the binding
    return tapp
