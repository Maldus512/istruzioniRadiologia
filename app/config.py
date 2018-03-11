# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TESTING=False
    DEBUG=True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'maldus-secret-key'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "mattia512maldini@gmail.com"
    MAIL_PASSWORD = "obscured"

    # administrator list
    ADMINS = ['mattia512maldini@gmail.com']

    LANGUAGES = { 
        'it': 'Italiano',
        'en': 'English',
        'es': 'Español'
    }
    LANGUAGES_LIST = [
        {'locale':'it', 'name': 'Italiano'},
        {'locale':'en', 'name': 'English'},
        {'locale':'es', 'name': 'Español'},
    ]




class ReleaseConfig(BaseConfig):
    DEBUG = False