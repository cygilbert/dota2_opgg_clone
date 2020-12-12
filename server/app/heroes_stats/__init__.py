"""
Heroes stats Blueprint
This is 2 page web apps:
    - first page (/) is all heroes and their global ranking
    - second page (/focus/<hero_id>) focus on one hero of <hero_id>
"""
from flask import Blueprint

bp = Blueprint('heroes_stats', __name__)

from app.heroes_stats import routes
