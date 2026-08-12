"""Testimonial (Отзывы) management with screenshot file upload."""
import os

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from admin import admin_bp
from admin.forms import TestimonialForm
from admin.utils import _admin_required, save_uploaded_file
from models import Testimonial, db


ALLOWED_SCREENSHOT_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def _screenshot_upload_dir():
    """Return absolute path to static/uploads/testimonials/."""
    return os.path.join(current_app.root_path, 'static', 'uploads', 'testimonials')


# ── list ─────────────────────────────────────────────────────────────────

@admin_bp.route('/testimonials')
@login_required
def testimonial_list():
    if denied := _admin_required():
        return denied

    search = request.args.get('q', '').strip()
    query = Testimonial.query.order_by(Testimonial.order, Testimonial.created_at.desc())
    if search:
        query = query.filter(Testimonial.name.ilike(f'%{search}%'))
    testimonials = query.all()
    return render_template('admin/testimonial_list.html', testimonials=testimonials, search=search)


# ── create ───────────────────────────────────────────────────────────────

@admin_bp.route('/testimonials/create', methods=['GET', 'POST'])
@login_required
def testimonial_create():
    if denied := _admin_required():
        return denied

    form = TestimonialForm()

    if form.validate_on_submit():
        item = Testimonial()
        item.name = form.name.data
        item.text = form.text.data
        item.rating = form.rating.data or 5
        item.author_role = form.author_role.data
        item.order = form.order.data or 0

        # Handle screenshot upload
        file = request.files.get('screenshot_file')
        if file and file.filename:
            saved = save_uploaded_file(file, _screenshot_upload_dir(), ALLOWED_SCREENSHOT_EXTENSIONS)
            if not saved:
                flash('Недопустимый формат. Разрешены: png, jpg, jpeg, gif, webp', 'error')
                return render_template('admin/testimonial_form.html', form=form, is_create=True)
            item.screenshot = saved

        db.session.add(item)
        db.session.commit()
        flash('Отзыв добавлен', 'success')
        return redirect(url_for('admin_new.testimonial_list'))

    return render_template('admin/testimonial_form.html', form=form, is_create=True)


# ── edit ─────────────────────────────────────────────────────────────────

@admin_bp.route('/testimonials/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def testimonial_edit(item_id):
    if denied := _admin_required():
        return denied

    item = Testimonial.query.get_or_404(item_id)
    form = TestimonialForm(obj=item)

    if form.validate_on_submit():
        item.name = form.name.data
        item.text = form.text.data
        item.rating = form.rating.data or 5
        item.author_role = form.author_role.data
        item.order = form.order.data or 0

        # Handle optional screenshot re-upload
        file = request.files.get('screenshot_file')
        if file and file.filename:
            saved = save_uploaded_file(file, _screenshot_upload_dir(), ALLOWED_SCREENSHOT_EXTENSIONS)
            if not saved:
                flash('Недопустимый формат. Разрешены: png, jpg, jpeg, gif, webp', 'error')
                return render_template('admin/testimonial_form.html', form=form, item=item, is_create=False)
            item.screenshot = saved

        db.session.commit()
        flash('Отзыв обновлён', 'success')
        return redirect(url_for('admin_new.testimonial_list'))

    return render_template('admin/testimonial_form.html', form=form, item=item, is_create=False)


# ── delete ───────────────────────────────────────────────────────────────

@admin_bp.route('/testimonials/<int:item_id>/delete', methods=['POST'])
@login_required
def testimonial_delete(item_id):
    if denied := _admin_required():
        return denied

    item = Testimonial.query.get_or_404(item_id)

    # Delete physical file
    if item.screenshot:
        filepath = os.path.join(_screenshot_upload_dir(), item.screenshot)
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(item)
    db.session.commit()
    flash('Отзыв удалён', 'success')
    return redirect(url_for('admin_new.testimonial_list'))
