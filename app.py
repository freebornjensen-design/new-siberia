import gevent.monkey
gevent.monkey.patch_all()

import os
import time
from flask import Flask, request, redirect, url_for, Response, send_from_directory
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO, join_room
from dotenv import load_dotenv
from flask_migrate import Migrate

from helpers.shared import normalize_path, send_telegram_notification

load_dotenv()

# SocketIO instance – created after app is created in create_app()
socketio = SocketIO()


from models import db, Article, Advantage, Certificate, ChatMessage, Contact, DailyAudio, User, Personnel, Service, GalleryImage, Testimonial, Statistic, Setting


def create_app():
    app = Flask(__name__)
    # basic config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/rehabdb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        if os.getenv('FLASK_ENV') == 'production':
            raise RuntimeError(
                "SECRET_KEY must be set in production. Generate one with: "
                "python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        # dev-only fallback
        secret_key = 'devsecret'
        print('WARNING: SECRET_KEY not set, using insecure dev fallback. Do NOT use in production.')
    app.config['SECRET_KEY'] = secret_key

    # Path under static/ where personnel photos live (no trailing slash)
    app.config['PERSONNEL_PHOTO_DIR'] = 'uploads/personnel'

    # CSRF protection (Flask-WTF)
    csrf = CSRFProtect(app)

    db.init_app(app)

    # Thumbnail generation helpers
    from helpers.thumbnails import ensure_personnel_thumbnail, ensure_image_variants

    # Ensure default settings exist (silently skip if table doesn't exist yet, e.g. during migration)
    with app.app_context():
        try:
            defaults = {
                'site_title': 'Новая Сибирь',
                'phone': '+7 983 305-06-90',
                'phone_2': '',
                'address': 'г. Новосибирск, в черте города',
                'work_hours': 'Круглосуточно, 7 дней в неделю',
                'site_headline': 'Реабилитационный центр — профессиональная помощь зависимым',
            }
            for key, val in defaults.items():
                if not Setting.query.filter_by(key=key).first():
                    db.session.add(Setting(key=key, value=val))
            db.session.commit()
        except Exception:
            db.session.rollback()

    # ── TTL cache for context_processor (settings) ─────────────────────
    # Runs on EVERY page render; without cache it issues DB queries per request.
    _context_cache = {}
    _CONTEXT_CACHE_TTL = 30  # seconds

    def _load_context_data():
        settings = {}
        for setting in Setting.query.all():
            settings[setting.key] = setting.value
        return settings

    # Context processor to make settings available to admin templates
    @app.context_processor
    def inject_settings():
        now = time.time()
        cached = _context_cache.get('nav')
        if cached and now - cached[0] < _CONTEXT_CACHE_TTL:
            settings = cached[1]
        else:
            settings = _load_context_data()
            _context_cache['nav'] = (now, settings)
        return {'settings': settings}

    # Register Jinja filter for path normalization
    app.jinja_env.filters['normalize_path'] = normalize_path

    # Flask-Migrate
    Migrate(app, db)

    # Photo migration CLI command
    from migrate_photos import register as register_photo_migrate
    register_photo_migrate(app)

    # Chat blueprint – REST API for live chat widget
    from chat import chat_bp
    app.register_blueprint(chat_bp)

    # Public JSON API for the SPA
    from api import api_bp
    app.register_blueprint(api_bp)

    # Exempt chat + api blueprints from CSRF (all endpoints use JSON, not form data)
    csrf.exempt(chat_bp)
    csrf.exempt(api_bp)

    # Custom admin blueprint – replaces Flask-Admin entirely
    from admin import admin_bp
    app.register_blueprint(admin_bp)

    # Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'admin_new.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.cli.command('create-admin')
    def create_admin_command():
        """Create an admin user: flask create-admin"""
        import click
        username = click.prompt('Username', default='admin')
        password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
        if User.query.filter_by(username=username).first():
            print(f'✗ User "{username}" already exists')
            return
        user = User(username=username, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f'✓ Admin user "{username}" created')

    @app.cli.command('generate-thumbnails')
    def generate_thumbnails_command():
        """Generate personnel photo thumbnails for all existing records."""
        from helpers.thumbnails import ensure_personnel_thumbnail
        count = 0
        for p in Personnel.query.all():
            if p.photo:
                result = ensure_personnel_thumbnail(app, p)
                if result:
                    count += 1
        print(f'✓ Generated {count} thumbnails')

    @app.cli.command('generate-all-thumbnails')
    def generate_all_thumbnails_command():
        """Alias for generate-thumbnails."""
        from helpers.thumbnails import ensure_personnel_thumbnail
        count = 0
        for p in Personnel.query.all():
            if p.photo:
                result = ensure_personnel_thumbnail(app, p)
                if result:
                    count += 1
        print(f'✓ Generated {count} thumbnails')

    # ── SPA serving (React build in dist/) ─────────────────────────────
    DIST_DIR = os.path.join(app.root_path, 'dist')
    SPA_SKIP_PREFIXES = ('admin', 'api', 'static', 'uploads')

    @app.route('/admin')
    def admin_index_redirect():
        # /admin (no trailing slash) → admin dashboard; must not fall into the SPA catch-all
        return redirect(url_for('admin_new.dashboard'))

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def spa(path):
        # Never swallow backend/upload paths
        if path and path.split('/')[0] in SPA_SKIP_PREFIXES:
            from flask import abort
            abort(404)
        # Serve real built assets from dist/, fall back to index.html for SPA routing
        candidate = os.path.join(DIST_DIR, path)
        if path and os.path.isfile(candidate):
            return send_from_directory(DIST_DIR, path)
        return send_from_directory(DIST_DIR, 'index.html')

    # ── Sitemap ────────────────────────────────────────────────────────
    SITE_URL = os.getenv('SITE_URL', 'https://xn----9sbbbck9a5agbgyb0md.xn--p1ai')

    @app.route('/sitemap.xml')
    def sitemap():
        # Static pages (single-page app – homepage only, everything else is SPA routes)
        static_pages = [
            ('/', '1.0', 'daily'),
        ]

        lines = []
        lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        for loc, priority, changefreq in static_pages:
            lines.append('  <url>')
            lines.append(f'    <loc>{SITE_URL}{loc}</loc>')
            lines.append(f'    <priority>{priority}</priority>')
            lines.append(f'    <changefreq>{changefreq}</changefreq>')
            lines.append('  </url>')

        lines.append('</urlset>')
        return Response('\n'.join(lines), mimetype='application/xml')

    # --- Robots.txt ---
    @app.route('/robots.txt')
    def robots():
        return Response(
            f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n',
            mimetype='text/plain'
        )

    # ── Security headers (HSTS, CSP, X-Frame-Options, etc.) ────────────
    @app.after_request
    def security_headers(resp):
        # HSTS — only meaningful over HTTPS
        if request.is_secure or request.headers.get('X-Forwarded-Proto', '').lower() == 'https':
            resp.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        resp.headers['X-Content-Type-Options'] = 'nosniff'
        resp.headers['X-Frame-Options'] = 'DENY'
        resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        resp.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://cdn.socket.io "
            "https://fonts.googleapis.com https://www.googletagmanager.com; "
            "style-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com "
            "https://fonts.googleapis.com https://fonts.gstatic.com; "
            "font-src 'self' data: https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.gstatic.com; "
            "img-src 'self' data: blob: https: http:; "
            "connect-src 'self' ws: wss: https://mc.yandex.ru https://yastatic.net; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'"
        )
        return resp

    # Initialize SocketIO with gevent async mode
    socketio.init_app(app, async_mode='gevent', cors_allowed_origins='*')

    # ── SocketIO event handlers ────────────────────────────────────────
    @socketio.on('connect')
    def handle_connect():
        session_id = request.args.get('session_id', '')
        if session_id:
            join_room(f'user_{session_id}')
            print(f'SocketIO connected: session={session_id[:8]}...')

    @socketio.on('join_admin')
    def handle_join_admin():
        # Admin panel joins the 'admin' room to receive notifications
        join_room('admin')

    @socketio.on('new_user_message')
    def handle_new_user_message(data):
        """Receive a message from the widget via SocketIO."""
        session_id = data.get('session_id', '')
        name = data.get('name', '').strip()
        message = data.get('message', '').strip()
        if not session_id or not message:
            return
        if len(message) > 2000:
            message = message[:2000]

        msg = ChatMessage(
            session_id=session_id,
            name=name or None,
            message=message,
            is_from_admin=False,
        )
        db.session.add(msg)
        db.session.commit()

        # Broadcast to admin room (admin panel opens automatically)
        socketio.emit('admin_new_message', {
            'id': msg.id,
            'session_id': session_id,
            'name': name or 'Аноним',
            'message': message,
            'created_at': msg.created_at.isoformat(),
        }, room='admin')

        # Notify Telegram bot
        from chat.routes import _notify_bot
        import threading
        t = threading.Thread(target=_notify_bot, args=(session_id, name, message))
        t.start()

    return app


# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('FLASK_DEBUG', '1') == '1')
