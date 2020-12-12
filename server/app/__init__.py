from flask import Flask, request, render_template, url_for
from flask_mysqldb import MySQL
import pandas as pd

mysql_app = MySQL()

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.DevConfig")
    mysql_app.init_app(app)

    with app.app_context():
        from app.heroes_stats import bp as bp_heroes_stats
        app.register_blueprint(bp_heroes_stats)
    return app
