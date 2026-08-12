"""Admin routes for editing About page content (stored in Setting model)."""
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from admin import admin_bp
from admin.utils import _admin_required
from models import Setting, db


# Keys for the About page
ABOUT_KEYS = [
    ('about_subtitle', 'Подзаголовок (hero)', 'Текст под заголовком на странице О центре'),
    ('about_intro_title', 'Заголовок вступления', 'Например: "О нашем центре"'),
    ('about_main_text', 'Основной текст', 'Подробное описание центра (можно использовать HTML-теги)'),
    ('about_approach_title', 'Заголовок раздела "Наш подход"', 'Например: "Наш подход к реабилитации"'),
    ('about_approach_text', 'Текст раздела "Наш подход"', 'Описание методик и подхода (HTML-теги допустимы)'),
    ('about_conditions_title', 'Заголовок раздела "Условия"', 'Например: "Условия проживания"'),
    ('about_conditions_text', 'Текст раздела "Условия"', 'Описание условий проживания (HTML-теги допустимы)'),
    ('about_team_title', 'Заголовок раздела "Команда"', 'Например: "Наша команда"'),
    ('about_team_text', 'Текст раздела "Команда"', 'Описание команды специалистов (HTML-теги допустимы)'),
    ('about_additional_text', 'Дополнительный текст', 'Текст в нижней части страницы (HTML-теги допустимы)'),
]


def _get_about_settings():
    """Return a dict of all about_* settings."""
    result = {}
    for key, _, _ in ABOUT_KEYS:
        setting = Setting.query.filter_by(key=key).first()
        result[key] = setting.value if setting else ''
    return result


def _save_about_settings(form_data):
    """Save about_* settings from form data."""
    for key, _, _ in ABOUT_KEYS:
        value = form_data.get(key, '').strip()
        setting = Setting.query.filter_by(key=key).first()
        if not setting:
            setting = Setting(key=key, description=dict((k, d) for k, _, d in ABOUT_KEYS).get(key, ''))
            db.session.add(setting)
        setting.value = value
    db.session.commit()


@admin_bp.route('/about-content', methods=['GET', 'POST'])
@login_required
def about_content():
    if denied := _admin_required():
        return denied

    if request.method == 'POST':
        _save_about_settings(request.form)
        flash('Контент страницы «О центре» сохранён', 'success')
        return redirect(url_for('admin_new.about_content'))

    settings = _get_about_settings()
    return render_template('admin/about_content.html',
        about_keys=ABOUT_KEYS,
        settings=settings,
    )
