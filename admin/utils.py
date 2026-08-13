"""Security and utility helpers for the admin panel."""
import os
import re
import unicodedata

from flask import current_app, flash, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

# Strict image-only allowlist – no executables, no scripts
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}

# Maximum upload size (10 MB)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024


def _admin_required():
    """Check admin auth – return a redirect if not admin, None otherwise."""
    if not (current_user.is_authenticated and getattr(current_user, 'is_admin', False)):
        flash('Доступ запрещён', 'error')
        return redirect(url_for('admin_new.login'))
    return None


def allowed_file(filename: str) -> bool:
    """Check extension against strict allowlist (case-insensitive)."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def safe_filename(filename: str) -> str:
    """Sanitize filename – removes path separators, special chars."""
    return secure_filename(filename)


def ensure_upload_dir(*subdirs: str) -> str:
    """Create nested directories under static/uploads/ and return the path."""
    path = os.path.join(current_app.static_folder, 'uploads', *subdirs)
    os.makedirs(path, exist_ok=True)
    return path


def upload_path(folder: str, filename: str) -> str:
    """Full filesystem path for a file in static/uploads/<folder>/."""
    return os.path.join(current_app.static_folder, 'uploads', folder, filename)


def upload_url(folder: str, filename: str) -> str:
    """URL for a file in static/uploads/<folder>/."""
    from flask import url_for
    return url_for('static', filename=f'uploads/{folder}/{filename}')


_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def slugify(text: str) -> str:
    """Transliterate + slugify a title into a URL-safe slug (ASCII)."""
    if not text:
        return ''
    text = text.lower().strip()
    text = ''.join(_TRANSLIT.get(ch, ch) for ch in text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text


def save_uploaded_file(file_storage, upload_dir: str, allowed_extensions: set) -> str:
    """
    Save an uploaded file to disk with overwrite protection.
    Returns the saved filename or None on failure.
    """
    if not file_storage or not file_storage.filename:
        return None

    if '.' not in file_storage.filename:
        return None
    ext = file_storage.filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        return None

    filename = secure_filename(file_storage.filename)
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)

    # Avoid overwriting
    base, ext_part = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filepath):
        filename = f'{base}_{counter}{ext_part}'
        filepath = os.path.join(upload_dir, filename)
        counter += 1

    file_storage.save(filepath)
    return filename
