from radiologia.config import BaseConfig, TestingConfig
from radiologia import db, babel
from flask import Flask

def create_test_app():
    app = Flask(__name__)
    app.config.from_object(TestingConfig)
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    babel.init_app(app)
    app.app_context().push() # this does the binding
    return app

# you can create another app context here, say for production
def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    babel.init_app(app)
    app.app_context().push()
    return app