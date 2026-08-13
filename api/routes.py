"""JSON endpoints consumed by the React SPA (new-siberia frontend)."""
import os
import re

from flask import current_app, jsonify, request, url_for

from api import api_bp
from helpers.thumbnails import ensure_personnel_thumbnail, ensure_image_variants
from models import (
    db, Advantage, Article, Certificate, ClinicLicense, Contact, DailyAudio,
    GalleryImage, MenuItem, Personnel, PriceItem, Service, Setting, Statistic,
    Testimonial,
)
from helpers.shared import normalize_path, send_telegram_notification


# ── helpers ─────────────────────────────────────────────────────────────

def _static_url(path):
    """URL for a file under static/, with backslash normalization."""
    if not path:
        return None
    return url_for('static', filename=normalize_path(path))


def _settings_dict():
    return {s.key: s.value for s in Setting.query.all()}


# ── settings ────────────────────────────────────────────────────────────

@api_bp.route('/settings')
def get_settings():
    return jsonify(_settings_dict())


# ── advantages ──────────────────────────────────────────────────────────

@api_bp.route('/advantages')
def get_advantages():
    items = []
    for a in Advantage.query.order_by(Advantage.order, Advantage.id).all():
        svg_url = None
        if a.icon_type == 'svg' and a.svg_file:
            svg_url = _static_url(f'uploads/svg_icons/{a.svg_file}')
        items.append({
            'id': a.id,
            'title': a.title,
            'text': a.text,
            'fa_icon': a.fa_icon,
            'icon_type': a.icon_type,
            'svg_url': svg_url,
            'order': a.order,
        })
    return jsonify(items)


# ── personnel ───────────────────────────────────────────────────────────

@api_bp.route('/personnel')
def get_personnel():
    items = []
    for p in Personnel.query.order_by(Personnel.order, Personnel.id).all():
        photo_url = None
        if p.photo:
            photo_dir = current_app.config['PERSONNEL_PHOTO_DIR']
            thumb_rel = ensure_personnel_thumbnail(current_app, p)
            photo_url = _static_url(thumb_rel or f'{photo_dir}/{p.photo}')
        items.append({
            'id': p.id,
            'name': p.name,
            'position': p.position,
            'photo_url': photo_url,
            'bio': p.bio,
            'intro': p.intro,
            'order': p.order,
        })
    return jsonify(items)


# ── articles ────────────────────────────────────────────────────────────

@api_bp.route('/articles')
def get_articles():
    items = []
    for a in Article.query.order_by(Article.created_at.desc()).all():
        # Plain-text excerpt (first 200 chars), strip HTML tags
        text = re.sub(r'<[^>]+>', ' ', a.body or '')
        text = re.sub(r'\s+', ' ', text).strip()
        excerpt = text[:200] + ('…' if len(text) > 200 else '')
        items.append({
            'id': a.id,
            'title': a.title,
            'excerpt': excerpt,
            'body': a.body,
            'date': a.created_at.strftime('%d.%m.%Y') if a.created_at else None,
            'created_at': a.created_at.isoformat() if a.created_at else None,
        })
    return jsonify(items)


# ── gallery ─────────────────────────────────────────────────────────────

@api_bp.route('/gallery')
def get_gallery():
    images = GalleryImage.query.filter_by(
        folder='gallery', is_active=True,
    ).order_by(GalleryImage.order, GalleryImage.id).all()

    items = []
    for img in images:
        thumb_rel, web_rel = ensure_image_variants(
            current_app, 'uploads/gallery', img.filename,
            thumb_size=(1200, 800), web_size=(1600, 1200),
        )
        items.append({
            'id': img.id,
            'filename': img.filename,
            'url': _static_url(thumb_rel or f'uploads/gallery/{img.filename}'),
            'full_url': _static_url(web_rel or f'uploads/gallery/{img.filename}'),
            'thumb_url': _static_url(thumb_rel or f'uploads/gallery/{img.filename}'),
            'title': img.title,
            'alt': img.title or f'Фото {img.id}',
        })
    return jsonify(items)


# ── statistics (achievements) ───────────────────────────────────────────

@api_bp.route('/statistics')
def get_statistics():
    items = []
    for s in Statistic.query.order_by(Statistic.order, Statistic.id).all():
        items.append({
            'id': s.id,
            'label': s.label,
            'value': s.value,
            'icon': s.icon,
            'order': s.order,
        })
    return jsonify(items)


# ── testimonials ────────────────────────────────────────────────────────

@api_bp.route('/testimonials')
def get_testimonials():
    items = []
    for t in Testimonial.query.order_by(Testimonial.order, Testimonial.id).all():
        items.append({
            'id': t.id,
            'name': t.name,
            'text': t.text,
            'rating': t.rating,
            'screenshot_url': _static_url(f'uploads/testimonials/{t.screenshot}') if t.screenshot else None,
        })
    return jsonify(items)


# ── services ────────────────────────────────────────────────────────────

@api_bp.route('/services')
def get_services():
    items = []
    for s in Service.query.order_by(Service.order, Service.id).all():
        items.append({
            'id': s.id,
            'title': s.title,
            'slug': s.slug,
            'description': s.description,
            'icon': s.icon,
            'order': s.order,
        })
    return jsonify(items)


# ── daily audio (Книга дня) ─────────────────────────────────────────────

@api_bp.route('/daily-audio')
def get_daily_audio():
    items = []
    for r in DailyAudio.query.order_by(DailyAudio.audio_date.desc().nullslast(), DailyAudio.order).all():
        items.append({
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'audio_url': _static_url(f'uploads/audio/{r.filename}') if r.filename else None,
            'date': r.audio_date.isoformat() if r.audio_date else None,
        })
    return jsonify(items)


# ── prices ────────────────────────────────────────────────────────────

@api_bp.route('/prices')
def get_prices():
    items = PriceItem.query.filter_by(is_active=True).order_by(
        PriceItem.order, PriceItem.category, PriceItem.id
    ).all()
    # Group by category (preserve order of first appearance)
    categories: list[dict] = []
    seen: dict[str, int] = {}  # category → index in categories
    for p in items:
        if p.category not in seen:
            seen[p.category] = len(categories)
            categories.append({'category': p.category, 'items': []})
        categories[seen[p.category]]['items'].append({
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'description': p.description,
            'order': p.order,
        })
    return jsonify(categories)


# ── clinic licenses ────────────────────────────────────────────────────

@api_bp.route('/licenses')
def get_licenses():
    items = []
    for lic in ClinicLicense.query.order_by(ClinicLicense.order, ClinicLicense.id).all():
        url = _static_url(f'uploads/licenses/{lic.file}') if lic.file else None
        items.append({
            'id': lic.id,
            'title': lic.title,
            'description': lic.description,
            'image_url': url,
        })
    return jsonify(items)


# ── navigation menu ───────────────────────────────────────────────────

@api_bp.route('/menu')
def get_menu():
    """Return the menu tree — top-level items with nested children."""
    top_items = MenuItem.query.filter_by(
        parent_id=None, is_active=True,
    ).order_by(MenuItem.order, MenuItem.id).all()

    def serialize(item):
        node = {
            'id': item.id,
            'title': item.title,
            'url': item.url,
            'icon': item.icon,
        }
        children = item.children.filter_by(is_active=True).order_by(MenuItem.order, MenuItem.id).all()
        if children:
            node['children'] = [serialize(c) for c in children]
        return node

    return jsonify([serialize(item) for item in top_items])


# ── FAQ (from settings with question+answer) ──────────────────────────

@api_bp.route('/faq')
def get_faq():
    items = Setting.query.filter(
        Setting.question.isnot(None),
        Setting.question != '',
    ).order_by(Setting.id).all()
    return jsonify([{
        'id': s.id,
        'question': s.question,
        'answer': s.answer or '',
    } for s in items])


# ── contact form ────────────────────────────────────────────────────────

@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()[:120]
    phone = (data.get('phone') or '').strip()[:50]
    addiction_type = (data.get('addiction_type') or '').strip()[:50]
    consent = bool(data.get('consent'))

    if not phone:
        return jsonify({'ok': False, 'error': 'Укажите номер телефона'}), 400
    if not consent:
        return jsonify({'ok': False, 'error': 'Необходимо согласие на обработку персональных данных'}), 400

    contact = Contact(name=name or None, phone=phone, addiction_type=addiction_type or None)
    db.session.add(contact)
    db.session.commit()

    try:
        send_telegram_notification(phone, name or None, addiction_type=addiction_type or None)
    except Exception:
        pass

    return jsonify({'ok': True})


# ── certificates for a person ───────────────────────────────────────────

@api_bp.route('/personnel/<int:person_id>/certificates')
def get_person_certificates(person_id):
    certs = Certificate.query.filter_by(personnel_id=person_id).order_by(Certificate.order).all()
    items = []
    for c in certs:
        if not c.file:
            continue
        url = _static_url(f'certs/{c.file}')
        ext = c.file.rsplit('.', 1)[-1].lower() if '.' in c.file else ''
        if ext in ('png', 'jpg', 'jpeg', 'gif', 'webp'):
            thumb_rel, web_rel = ensure_image_variants(
                current_app, 'certs', c.file, thumb_size=(600, 600), web_size=(1400, 1400),
            )
            thumb_url = _static_url(thumb_rel) if thumb_rel else url
            full_url = _static_url(web_rel) if web_rel else url
        else:
            thumb_url = full_url = url
        items.append({
            'id': c.id,
            'owner': c.owner,
            'description': c.description,
            'file': c.file,
            'url': url,
            'thumb_url': thumb_url,
            'full_url': full_url,
            'order': c.order,
        })
    return jsonify(items)
