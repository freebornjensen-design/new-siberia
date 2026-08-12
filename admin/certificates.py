"""Certificate (Сертификаты) management with file upload and personnel link."""
import os

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from admin import admin_bp
from admin.forms import CertificateForm
from admin.utils import _admin_required, save_uploaded_file
from models import Certificate, db


ALLOWED_CERT_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}


def _certs_upload_dir():
    """Return absolute path to static/certs/."""
    return os.path.join(current_app.root_path, 'static', 'certs')


# ── list ─────────────────────────────────────────────────────────────────

@admin_bp.route('/certificates')
@login_required
def certificate_list():
    if denied := _admin_required():
        return denied
    certs = Certificate.query.order_by(Certificate.order, Certificate.created_at.desc()).all()
    return render_template('admin/certificate_list.html', certs=certs)


# ── create ───────────────────────────────────────────────────────────────

@admin_bp.route('/certificates/create', methods=['GET', 'POST'])
@login_required
def certificate_create():
    if denied := _admin_required():
        return denied

    # Pre-fill personnel_id if passed as query param (from personnel edit page)
    preselected_person_id = request.args.get('personnel_id', type=int)

    form = CertificateForm()

    if form.validate_on_submit():
        cert = Certificate()
        cert.personnel_id = form.personnel_id.data if form.personnel_id.data and form.personnel_id.data != 0 else None
        cert.owner = form.owner.data
        cert.description = form.description.data
        cert.order = form.order.data or 0

        # Handle file upload
        file = request.files.get('cert_file')
        if file and file.filename:
            saved = save_uploaded_file(file, _certs_upload_dir(), ALLOWED_CERT_EXTENSIONS)
            if not saved:
                flash('Недопустимый формат. Разрешены: png, jpg, jpeg, gif, webp, pdf', 'error')
                return render_template('admin/certificate_form.html', form=form, is_create=True)
            cert.file = saved
        else:
            flash('Выберите файл сертификата для загрузки', 'error')
            return render_template('admin/certificate_form.html', form=form, is_create=True)

        db.session.add(cert)
        db.session.commit()
        flash('Сертификат добавлен', 'success')

        # Redirect back to personnel edit if that's where we came from
        next_url = request.args.get('next')
        if next_url:
            return redirect(next_url)
        return redirect(url_for('admin_new.certificate_list'))

    # Pre-select personnel_id on GET
    if request.method == 'GET' and preselected_person_id:
        form.personnel_id.data = preselected_person_id

    return render_template('admin/certificate_form.html', form=form, is_create=True)


# ── edit ─────────────────────────────────────────────────────────────────

@admin_bp.route('/certificates/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def certificate_edit(item_id):
    if denied := _admin_required():
        return denied

    cert = Certificate.query.get_or_404(item_id)
    form = CertificateForm(obj=cert)

    if form.validate_on_submit():
        cert.personnel_id = form.personnel_id.data if form.personnel_id.data and form.personnel_id.data != 0 else None
        cert.owner = form.owner.data
        cert.description = form.description.data
        cert.order = form.order.data or 0

        # Handle optional file re-upload
        file = request.files.get('cert_file')
        if file and file.filename:
            saved = save_uploaded_file(file, _certs_upload_dir(), ALLOWED_CERT_EXTENSIONS)
            if not saved:
                flash('Недопустимый формат. Разрешены: png, jpg, jpeg, gif, webp, pdf', 'error')
                return render_template('admin/certificate_form.html', form=form, item=cert, is_create=False)
            cert.file = saved

        db.session.commit()
        flash('Сертификат обновлён', 'success')

        next_url = request.args.get('next')
        if next_url:
            return redirect(next_url)
        return redirect(url_for('admin_new.certificate_list'))

    return render_template('admin/certificate_form.html', form=form, item=cert, is_create=False)


# ── delete ───────────────────────────────────────────────────────────────

@admin_bp.route('/certificates/<int:item_id>/delete', methods=['POST'])
@login_required
def certificate_delete(item_id):
    if denied := _admin_required():
        return denied

    cert = Certificate.query.get_or_404(item_id)

    # Delete physical file
    if cert.file:
        filepath = os.path.join(_certs_upload_dir(), cert.file)
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(cert)
    db.session.commit()
    flash('Сертификат удалён', 'success')

    next_url = request.args.get('next')
    if next_url:
        return redirect(next_url)
    return redirect(url_for('admin_new.certificate_list'))
