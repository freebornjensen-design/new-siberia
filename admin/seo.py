"""Admin routes for SEO & analytics settings (stored in the Setting model)."""
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from admin import admin_bp
from admin.utils import _admin_required
from models import Setting, db


# (key, label, description, field_type) — field_type is 'input' or 'textarea'
SEO_KEYS = [
    ('seo_title', 'Title (заголовок вкладки)', 'До 60 символов. Главный заголовок в поисковой выдаче.', 'input'),
    ('seo_description', 'Description (описание)', 'До 160 символов. Текст-сниппет под заголовком в выдаче.', 'textarea'),
    ('seo_keywords', 'Keywords (ключевые слова)', 'Через запятую. Учитываются Яндексом.', 'input'),
    ('og_title', 'OG Title (заголовок для соцсетей)', 'Заголовок при шаринге в ВК / Telegram / WhatsApp.', 'input'),
    ('og_description', 'OG Description (описание для соцсетей)', 'Описание при шаринге.', 'textarea'),
    ('og_image', 'OG Image (URL картинки)', 'Абсолютный URL картинки для превью при шаринге (например, https://new-siberia.center/...). Пусто = без превью.', 'input'),
    ('gtm_id', 'Google Tag Manager ID', 'Идентификатор вида GTM-XXXXXXX. Пусто = счётчик отключён.', 'input'),
]


def _get_seo_settings():
    result = {}
    for key, _, _, _ in SEO_KEYS:
        setting = Setting.query.filter_by(key=key).first()
        result[key] = setting.value if setting else ''
    return result


def _save_seo_settings(form_data):
    descriptions = {key: desc for key, _, desc, _ in SEO_KEYS}
    for key, _, _, _ in SEO_KEYS:
        value = form_data.get(key, '').strip()
        setting = Setting.query.filter_by(key=key).first()
        if not setting:
            setting = Setting(key=key, description=descriptions.get(key, ''))
            db.session.add(setting)
        setting.value = value
    db.session.commit()


@admin_bp.route('/seo', methods=['GET', 'POST'])
@login_required
def seo_content():
    if denied := _admin_required():
        return denied

    if request.method == 'POST':
        _save_seo_settings(request.form)
        flash('Настройки SEO и аналитики сохранены', 'success')
        return redirect(url_for('admin_new.seo_content'))

    settings = _get_seo_settings()
    return render_template('admin/seo.html', seo_keys=SEO_KEYS, settings=settings)
