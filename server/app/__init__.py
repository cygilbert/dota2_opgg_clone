from flask import Flask
from flask_mysqldb import MySQL


"""Mysql connector"""
mysql_app = MySQL()


def init_app():
    """Create Flask application."""
    # Create
    app = Flask(__name__, instance_relative_config=False)
    # Config
    app.config.from_object("config.DevConfig")
    # Init MySQL app connection
    mysql_app.init_app(app)

    # Import and register blueprint
    with app.app_context():
        from app.heroes_stats import bp as bp_heroes_stats
        app.register_blueprint(bp_heroes_stats)
    return app
