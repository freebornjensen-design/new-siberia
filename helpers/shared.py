"""Shared helpers used across app.py and api/routes.py.

Kept out of app.py so that api/ and chat/ blueprints can import these
without creating a circular import at module level.
"""
import os

import requests


def normalize_path(path):
    """Convert backslashes to forward slashes for URLs (Windows compatibility)."""
    return path.replace('\\', '/')


def send_telegram_notification(phone, name=None, addiction_type=None):
    """Notify the admin via the Telegram bot (bypasses API blocking in RU)."""
    admin_id = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
    if not admin_id:
        return False

    text = f"Номер: {phone}"
    if name:
        text += f"\nИмя: {name}"
    if addiction_type:
        text += f"\nТип зависимости: {addiction_type}"

    # Send through the bot (bypasses Telegram API blocking in RU)
    bot_url = os.getenv('BOT_NOTIFY_URL', 'https://bot.xn----9sbbbck9a5agbgyb0md.xn--p1ai/notify')
    secret = os.getenv('NOTIFY_SECRET', '')
    headers = {'X-Notify-Secret': secret} if secret else {}
    try:
        resp = requests.post(bot_url, json={
            'chat_id': admin_id,
            'text': text,
            'source': 'callback',
        }, headers=headers, timeout=10)
        if not resp.ok:
            print(f'Telegram notify failed: {resp.status_code} {resp.text[:200]}')
            return False
        return True
    except Exception as e:
        print(f'Telegram notify error: {e}')
        return False
