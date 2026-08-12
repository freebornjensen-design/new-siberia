"""REST API endpoints for chat widget + admin chat panel.

SocketIO events are registered in app.py to keep the socketio instance globally accessible.
"""
import os
import threading
from datetime import datetime
from functools import wraps
from flask import jsonify, request
from flask_login import current_user
from models import db, ChatMessage

from chat import chat_bp


# ── Custom decorator for admin API endpoints ──────────────────────────
# Returns JSON 401 instead of Flask-Login's HTML redirect

def admin_api_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            return jsonify({'ok': False, 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return wrapper


# ── Helper: notify Telegram bot about new message ──────────────────────

def _notify_bot(session_id: str, name: str, message: str):
    """POST to bot's /notify endpoint with inline reply marker."""
    bot_url = os.getenv('BOT_NOTIFY_URL', 'https://bot.xn----9sbbbck9a5agbgyb0md.xn--p1ai/notify')
    secret = os.getenv('NOTIFY_SECRET', '')
    admin_id = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
    if not admin_id or not bot_url:
        return

    text = (
        f"Имя: {name or 'Не указано'}\n"
        f"Сессия: <code>{session_id}</code>\n"
        f"Сообщение: {message}\n\n"
        f"👇 Нажмите кнопку ниже, чтобы ответить."
    )

    try:
        import requests
        headers = {'X-Notify-Secret': secret} if secret else {}
        resp = requests.post(bot_url, json={
            'chat_id': admin_id,
            'text': text,
            'source': 'chat',
            'reply_marker': session_id,
        }, headers=headers, timeout=10)
        if not resp.ok:
            print(f'Chat notify bot failed: {resp.status_code} {resp.text[:200]}')
    except Exception as e:
        print(f'Chat notify bot error: {e}')


# ── REST endpoints ──────────────────────────────────────────────────────

@chat_bp.route('/send', methods=['POST'])
def send_message():
    """Receive a message from the chat widget."""
    data = request.get_json(silent=True) or {}
    session_id = data.get('session_id', '').strip()
    name = data.get('name', '').strip()
    message = data.get('message', '').strip()

    if not session_id or not message:
        return jsonify({'ok': False, 'error': 'session_id and message required'}), 400

    if len(message) > 2000:
        message = message[:2000]
    if len(name) > 100:
        name = name[:100]

    msg = ChatMessage(
        session_id=session_id,
        name=name or None,
        message=message,
        is_from_admin=False,
    )
    db.session.add(msg)
    db.session.commit()

    t = threading.Thread(target=_notify_bot, args=(session_id, name, message))
    t.start()

    return jsonify({'ok': True, 'id': msg.id, 'created_at': msg.created_at.isoformat()})


@chat_bp.route('/history')
def get_history():
    """Get messages for a session."""
    session_id = request.args.get('session_id', '').strip()
    if not session_id:
        return jsonify({'ok': False, 'error': 'session_id required'}), 400

    since = request.args.get('since')
    query = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at.asc())

    if since:
        try:
            since_dt = datetime.fromisoformat(since)
            query = query.filter(ChatMessage.created_at > since_dt)
        except ValueError:
            pass

    messages = query.all()
    return jsonify({
        'ok': True,
        'messages': [{
            'id': m.id,
            'message': m.message,
            'is_from_admin': m.is_from_admin,
            'created_at': m.created_at.isoformat(),
        } for m in messages],
    })


@chat_bp.route('/admin-reply', methods=['POST'])
def admin_reply():
    """Receive a reply from Telegram bot (protected by NOTIFY_SECRET)."""
    data = request.get_json(silent=True) or {}
    session_id = data.get('session_id', '').strip()
    message = data.get('message', '').strip()
    secret = data.get('secret', '')

    expected_secret = os.getenv('NOTIFY_SECRET', '')
    if expected_secret and secret != expected_secret:
        return jsonify({'ok': False, 'error': 'Forbidden'}), 403

    if not session_id or not message:
        return jsonify({'ok': False, 'error': 'session_id and message required'}), 400

    if len(message) > 2000:
        message = message[:2000]

    msg = ChatMessage(
        session_id=session_id,
        name='Администратор',
        message=message,
        is_from_admin=True,
    )
    db.session.add(msg)
    db.session.commit()

    _emit_to_user(session_id, msg)
    return jsonify({'ok': True, 'id': msg.id})


def _emit_to_user(session_id, msg):
    """Helper to emit a message to a user's SocketIO room."""
    try:
        from app import socketio
        socketio.emit('new_message', {
            'id': msg.id,
            'message': msg.message,
            'is_from_admin': msg.is_from_admin,
            'created_at': msg.created_at.isoformat(),
        }, room=f'user_{session_id}')
    except (ImportError, RuntimeError):
        pass


# ── Admin endpoints (protected by admin_api_required) ─────────────────

@chat_bp.route('/admin/sessions')
@admin_api_required
def admin_sessions():
    """List all chat sessions with last message and unread count."""
    from sqlalchemy import func

    subq = db.session.query(
        ChatMessage.session_id,
        func.max(ChatMessage.created_at).label('last_time'),
    ).group_by(ChatMessage.session_id).subquery()

    sessions = db.session.query(
        ChatMessage.session_id,
        ChatMessage.name,
        ChatMessage.message,
        ChatMessage.created_at,
    ).join(
        subq,
        db.and_(
            ChatMessage.session_id == subq.c.session_id,
            ChatMessage.created_at == subq.c.last_time,
        )
    ).order_by(ChatMessage.created_at.desc()).all()

    result = []
    for s in sessions:
        unread = ChatMessage.query.filter_by(
            session_id=s.session_id,
            is_from_admin=False,
            is_read=False,
        ).count()
        result.append({
            'session_id': s.session_id,
            'name': s.name or 'Аноним',
            'last_message': (s.message or '')[:100],
            'last_time': s.created_at.isoformat(),
            'unread': unread,
        })

    return jsonify({'ok': True, 'sessions': result})


@chat_bp.route('/admin/sessions/<session_id>/mark-read', methods=['POST'])
@admin_api_required
def mark_read(session_id):
    """Mark all user messages in a session as read."""
    ChatMessage.query.filter_by(
        session_id=session_id,
        is_from_admin=False,
        is_read=False,
    ).update({'is_read': True})
    db.session.commit()
    return jsonify({'ok': True})


@chat_bp.route('/admin/sessions/<session_id>/reply', methods=['POST'])
@admin_api_required
def admin_panel_reply(session_id):
    """Send a reply from the admin panel."""
    data = request.get_json(silent=True) or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'ok': False, 'error': 'message required'}), 400

    if len(message) > 2000:
        message = message[:2000]

    msg = ChatMessage(
        session_id=session_id,
        name='Администратор',
        message=message,
        is_from_admin=True,
    )
    db.session.add(msg)
    db.session.commit()

    _emit_to_user(session_id, msg)
    return jsonify({'ok': True, 'id': msg.id})
