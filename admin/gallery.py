"""Gallery management – upload, tree-view, drag-and-drop move, delete."""
import os
import shutil

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from admin import admin_bp
from admin.utils import (
    ALLOWED_EXTENSIONS, _admin_required, allowed_file, safe_filename,
    ensure_upload_dir, upload_path, upload_url,
)
from models import GalleryImage, db

# Supported folders for gallery tree
GALLERY_FOLDERS = ['gallery', 'personnel', 'events']
FOLDER_LABELS = {
    'gallery': 'Галерея',
    'personnel': 'Персонал',
    'events': 'Мероприятия',
}


def _admin_json_required():
    """AJAX-specific auth check – returns JSON 403 instead of redirect."""
    from flask import jsonify
    if not (current_user.is_authenticated and getattr(current_user, 'is_admin', False)):
        return jsonify({'error': 'Доступ запрещён'}), 403
    return None


# ── gallery page ─────────────────────────────────────────────────────────

@admin_bp.route('/gallery')
@login_required
def gallery_page():
    if denied := _admin_required():
        return denied

    current_folder = request.args.get('folder', 'gallery')
    if current_folder not in GALLERY_FOLDERS:
        current_folder = 'gallery'

    images = GalleryImage.query.filter_by(
        folder=current_folder,
    ).order_by(GalleryImage.order).all()

    # Folder counts for sidebar
    folder_counts = {}
    for f in GALLERY_FOLDERS:
        folder_counts[f] = GalleryImage.query.filter_by(folder=f).count()

    return render_template('admin/gallery.html',
        images=images,
        folders=GALLERY_FOLDERS,
        folder_labels=FOLDER_LABELS,
        folder_counts=folder_counts,
        current_folder=current_folder,
    )


# ── upload ───────────────────────────────────────────────────────────────

@admin_bp.route('/gallery/upload', methods=['POST'])
@login_required
def gallery_upload():
    if denied := _admin_json_required():
        return denied

    target_folder = request.form.get('folder', 'gallery')
    if target_folder not in GALLERY_FOLDERS:
        return jsonify({'error': 'Неизвестная папка'}), 400

    if 'file' not in request.files:
        return jsonify({'error': 'Файл не выбран'}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'Файл не выбран'}), 400

    if not allowed_file(file.filename):
        return jsonify({
            'error': f'Недопустимый формат. Разрешены: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400

    filename = safe_filename(file.filename)
    folder_path = ensure_upload_dir(target_folder)
    filepath = os.path.join(folder_path, filename)
    file.save(filepath)

    # Create GalleryImage record
    existing = GalleryImage.query.filter_by(filename=filename, folder=target_folder).first()
    if not existing:
        img = GalleryImage(
            filename=filename,
            folder=target_folder,
            is_active=True,
            order=GalleryImage.query.filter_by(folder=target_folder).count(),
        )
        db.session.add(img)
        db.session.commit()
    else:
        existing.is_active = True
        db.session.commit()

    return jsonify({
        'success': True,
        'filename': filename,
        'folder': target_folder,
        'url': upload_url(target_folder, filename),
    })


# ── move (drag-and-drop or button) ───────────────────────────────────────

@admin_bp.route('/gallery/move', methods=['POST'])
@login_required
def gallery_move():
    if denied := _admin_json_required():
        return denied

    filename = request.form.get('filename')
    old_folder = request.form.get('from_folder')
    new_folder = request.form.get('to_folder')

    if not all([filename, old_folder, new_folder]):
        return jsonify({'error': 'Не все параметры переданы'}), 400

    if new_folder not in GALLERY_FOLDERS:
        return jsonify({'error': 'Неизвестная папка назначения'}), 400

    img = GalleryImage.query.filter_by(filename=filename, folder=old_folder).first()
    if not img:
        return jsonify({'error': 'Файл не найден в БД'}), 404

    # Move physical file
    src = upload_path(old_folder, filename)
    dst = upload_path(new_folder, filename)
    ensure_upload_dir(new_folder)
    if os.path.exists(src):
        shutil.move(src, dst)

    img.folder = new_folder
    db.session.commit()

    return jsonify({
        'success': True,
        'filename': filename,
        'folder': new_folder,
        'url': upload_url(new_folder, filename),
    })


# ── toggle active ────────────────────────────────────────────────────────

@admin_bp.route('/gallery/toggle', methods=['POST'])
@login_required
def gallery_toggle():
    if denied := _admin_json_required():
        return denied

    filename = request.form.get('filename')
    folder = request.form.get('folder')

    img = GalleryImage.query.filter_by(filename=filename, folder=folder).first()
    if img:
        img.is_active = not img.is_active
    else:
        img = GalleryImage(filename=filename, folder=folder, is_active=True)
        db.session.add(img)
    db.session.commit()

    return jsonify({'success': True, 'is_active': img.is_active})


# ── delete ───────────────────────────────────────────────────────────────

@admin_bp.route('/gallery/delete', methods=['POST'])
@login_required
def gallery_delete():
    if denied := _admin_json_required():
        return denied

    filename = request.form.get('filename')
    folder = request.form.get('folder')

    img = GalleryImage.query.filter_by(filename=filename, folder=folder).first()
    if img:
        # Delete physical file
        filepath = upload_path(folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        db.session.delete(img)
        db.session.commit()

    return jsonify({'success': True})
