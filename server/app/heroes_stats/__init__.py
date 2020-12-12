from flask import Blueprint

bp = Blueprint('heroes_stats', __name__)

from app.heroes_stats import routes