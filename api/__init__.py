"""Public JSON API for the React SPA frontend.

All endpoints return JSON. The blueprint is CSRF-exempt (all requests
are JSON, not form posts).
"""
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from api import routes  # noqa: E402, F401
