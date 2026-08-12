"""Personnel management with gallery photo picker."""
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from admin import admin_bp
from admin.forms import PersonnelForm
from admin.utils import _admin_required
from models import GalleryImage, Personnel, db


@admin_bp.route('/personnel')
@login_required
def personnel_page():
    if denied := _admin_required():
        return denied
    people = Personnel.query.order_by(Personnel.order, Personnel.created_at.desc()).all()
    return render_template('admin/personnel.html', people=people)


@admin_bp.route('/personnel/create', methods=['GET', 'POST'])
@login_required
def personnel_create():
    if denied := _admin_required():
        return denied
    form = PersonnelForm()
    if form.validate_on_submit():
        person = Personnel()
        form.populate_obj(person)
        db.session.add(person)
        db.session.commit()
        flash('Сотрудник добавлен', 'success')
        return redirect(url_for('admin_new.personnel_page'))
    return render_template('admin/personnel_form.html', form=form, is_create=True)


@admin_bp.route('/personnel/<int:person_id>/edit', methods=['GET', 'POST'])
@login_required
def personnel_edit(person_id):
    if denied := _admin_required():
        return denied
    person = Personnel.query.get_or_404(person_id)
    form = PersonnelForm(obj=person)
    if form.validate_on_submit():
        form.populate_obj(person)
        db.session.commit()
        flash('Сотрудник обновлён', 'success')
        return redirect(url_for('admin_new.personnel_page'))
    # Get certificates for this person
    from models import Certificate
    certs = Certificate.query.filter_by(personnel_id=person.id).order_by(Certificate.order).all()
    return render_template('admin/personnel_form.html',
        form=form, person=person, certs=certs, is_create=False)


@admin_bp.route('/personnel/<int:person_id>/delete', methods=['POST'])
@login_required
def personnel_delete(person_id):
    if denied := _admin_required():
        return denied
    person = Personnel.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    flash('Сотрудник удалён', 'success')
    return redirect(url_for('admin_new.personnel_page'))


@admin_bp.route('/personnel/photos')
@login_required
def personnel_photos_json():
    """JSON endpoint: list photos in 'personnel' folder for the picker modal."""
    if denied := _admin_required():
        return denied
    folder = request.args.get('folder', 'personnel')
    images = GalleryImage.query.filter_by(
        folder=folder, is_active=True
    ).order_by(GalleryImage.order).all()
    return {
        'photos': [{
            'id': img.id,
            'filename': img.filename,
            'url': f'/static/uploads/{folder}/{img.filename}',
        } for img in images]
    }
