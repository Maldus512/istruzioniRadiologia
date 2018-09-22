# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    AUDIODIR = "static/audio"
    ALLOWED_EXTENSIONS = set(['mp3'])
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
        'es': 'Español',
        'zh': '中国',
        'ar': 'العربية',
    }
    LANGUAGES_LIST = [
        {'locale':'it', 'name': 'Italiano'},
        {'locale':'en', 'name': 'English'},
        {'locale':'es', 'name': 'Español'},
        {'locale':'zh', 'name': '中国'},
        {'locale':'ar', 'name': 'العربية'},
    ]


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_db.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'test_db_repository')
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False


class ReleaseConfig(BaseConfig):
    DEBUG = False
