"""Flask config."""
from os import environ, path
from dotenv import load_dotenv

# Access to env variable
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    """MySQL environement variables"""
    MYSQL_HOST = environ.get('MYSQL_HOST', 'db')
    MYSQL_PORT = int(environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_DB = environ.get('MYSQL_DB', 'dota2_datawarehouse')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
