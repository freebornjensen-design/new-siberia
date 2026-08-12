"""Admin blueprint – custom admin panel replacing Flask-Admin.

Registered at /admin-new during migration, then switched to /admin.
"""
from flask import Blueprint

admin_bp = Blueprint(
    'admin_new',
    __name__,
    template_folder='../templates/admin',
    static_folder='../static',
    url_prefix='/admin',
)

# Import routes so they register with the blueprint
from admin import routes, gallery, personnel, daily_audio, certificates, advantages, about, testimonials  # noqa: E402, F401
