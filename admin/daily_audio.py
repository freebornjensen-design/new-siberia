"""DailyAudio (Книга дня) management with file upload."""
import os

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from admin import admin_bp
from admin.forms import DailyAudioForm
from admin.utils import _admin_required, save_uploaded_file
from models import DailyAudio, db


ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a', 'aac'}


def _audio_upload_dir():
    """Return absolute path to static/uploads/audio/."""
    return os.path.join(current_app.root_path, 'static', 'uploads', 'audio')


# ── list ─────────────────────────────────────────────────────────────────

@admin_bp.route('/daily_audio')
@login_required
def daily_audio_list():
    if denied := _admin_required():
        return denied
    recordings = DailyAudio.query.order_by(
        DailyAudio.audio_date.desc().nullslast(),
        DailyAudio.order,
    ).all()
    return render_template('admin/daily_audio_list.html', recordings=recordings)


# ── create ───────────────────────────────────────────────────────────────

@admin_bp.route('/daily_audio/create', methods=['GET', 'POST'])
@login_required
def daily_audio_create():
    if denied := _admin_required():
        return denied

    form = DailyAudioForm()

    if form.validate_on_submit():
        rec = DailyAudio()
        rec.title = form.title.data
        rec.description = form.description.data
        rec.audio_date = form.audio_date.data
        rec.order = form.order.data or 0

        # Handle file upload
        file = request.files.get('audio_file')
        if file and file.filename:
            saved = save_uploaded_file(file, _audio_upload_dir(), ALLOWED_AUDIO_EXTENSIONS)
            if not saved:
                flash('Недопустимый формат аудиофайла. Разрешены: mp3, wav, ogg, m4a, aac', 'error')
                return render_template('admin/daily_audio_form.html', form=form, is_create=True)
            rec.filename = saved
        else:
            flash('Выберите аудиофайл для загрузки', 'error')
            return render_template('admin/daily_audio_form.html', form=form, is_create=True)

        db.session.add(rec)
        db.session.commit()
        flash('Запись добавлена', 'success')
        return redirect(url_for('admin_new.daily_audio_list'))

    return render_template('admin/daily_audio_form.html', form=form, is_create=True)


# ── edit ─────────────────────────────────────────────────────────────────

@admin_bp.route('/daily_audio/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def daily_audio_edit(item_id):
    if denied := _admin_required():
        return denied

    rec = DailyAudio.query.get_or_404(item_id)
    form = DailyAudioForm(obj=rec)

    if form.validate_on_submit():
        rec.title = form.title.data
        rec.description = form.description.data
        rec.audio_date = form.audio_date.data
        rec.order = form.order.data or 0

        # Handle optional file re-upload
        file = request.files.get('audio_file')
        if file and file.filename:
            saved = save_uploaded_file(file, _audio_upload_dir(), ALLOWED_AUDIO_EXTENSIONS)
            if not saved:
                flash('Недопустимый формат аудиофайла. Разрешены: mp3, wav, ogg, m4a, aac', 'error')
                return render_template('admin/daily_audio_form.html', form=form, item=rec, is_create=False)
            rec.filename = saved

        db.session.commit()
        flash('Запись обновлена', 'success')
        return redirect(url_for('admin_new.daily_audio_list'))

    return render_template('admin/daily_audio_form.html', form=form, item=rec, is_create=False)


# ── delete ───────────────────────────────────────────────────────────────

@admin_bp.route('/daily_audio/<int:item_id>/delete', methods=['POST'])
@login_required
def daily_audio_delete(item_id):
    if denied := _admin_required():
        return denied

    rec = DailyAudio.query.get_or_404(item_id)

    # Delete physical file
    if rec.filename:
        filepath = os.path.join(_audio_upload_dir(), rec.filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(rec)
    db.session.commit()
    flash('Запись удалена', 'success')
    return redirect(url_for('admin_new.daily_audio_list'))
