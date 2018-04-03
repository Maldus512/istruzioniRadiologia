from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from radiologia.config import BaseConfig, ReleaseConfig
from flask_migrate import Migrate
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_dir, static_folder=static_dir)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
babel = Babel(app)
migrate = Migrate(app, db)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('logs/patti.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('patti startup')

from radiologia import views, models
