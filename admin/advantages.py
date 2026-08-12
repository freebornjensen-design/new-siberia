"""Advantage (Преимущества) management with SVG upload and icon type selection."""
import os

from flask import current_app, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from admin import admin_bp
from admin.forms import AdvantageForm
from admin.utils import _admin_required, save_uploaded_file
from models import Advantage, db

ALLOWED_SVG_EXTENSIONS = {'svg'}

ADVANTAGE_CFG = {
    'title': 'Преимущества',
    'title_singular': 'Преимущество',
    'columns': ['title', 'icon', 'icon_type', 'order'],
    'search_field': 'title',
}


def _svg_upload_dir():
    """Return absolute path to static/uploads/svg_icons/."""
    return os.path.join(current_app.root_path, 'static', 'uploads', 'svg_icons')


# ── SVG list JSON endpoint ──────────────────────────────────────────────

@admin_bp.route('/advantages/svg-list.json')
@login_required
def advantage_svg_list():
    """Return JSON list of available SVG files in the uploads directory.
    Response is uncacheable to ensure gallery always shows fresh data."""
    svg_dir = _svg_upload_dir()
    svg_files = []
    static_prefix = 'uploads/svg_icons/'
    if os.path.isdir(svg_dir):
        for fname in sorted(os.listdir(svg_dir)):
            if fname.lower().endswith('.svg'):
                svg_files.append({
                    'filename': fname,
                    'url': url_for('static', filename=static_prefix + fname),
                })
    resp = make_response(jsonify(svg_files))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp


# ── list ─────────────────────────────────────────────────────────────────

@admin_bp.route('/advantages')
@login_required
def advantage_list():
    if denied := _admin_required():
        return denied
    items = Advantage.query.order_by(Advantage.order).all()
    return render_template('admin/generic/list.html',
        entity='advantages',
        cfg=ADVANTAGE_CFG,
        items=items,
        search=request.args.get('q', ''),
    )


# ── create ───────────────────────────────────────────────────────────────

@admin_bp.route('/advantages/create', methods=['GET', 'POST'])
@login_required
def advantage_create():
    if denied := _admin_required():
        return denied

    form = AdvantageForm()

    if form.validate_on_submit():
        item = Advantage()
        item.title = form.title.data
        item.text = form.text.data
        item.fa_icon = form.fa_icon.data
        item.icon_type = form.icon_type.data
        item.order = form.order.data or 0

        # Handle SVG file upload if icon_type is 'svg'
        if form.icon_type.data == 'svg':
            file = request.files.get('svg_upload')
            if file and file.filename:
                saved = save_uploaded_file(file, _svg_upload_dir(), ALLOWED_SVG_EXTENSIONS)
                if not saved:
                    flash('Недопустимый формат. Разрешены только SVG', 'error')
                    return render_template('admin/generic/form.html',
                        entity='advantages', form=form, is_create=True,
                        cfg=ADVANTAGE_CFG)
                item.svg_file = saved
            elif form.svg_file.data:
                # Выбрано из галереи, новый файл не загружался
                item.svg_file = form.svg_file.data
            else:
                flash('Загрузите SVG файл или выберите из галереи', 'error')
                return render_template('admin/generic/form.html',
                    entity='advantages', form=form, is_create=True,
                    cfg=ADVANTAGE_CFG)

        db.session.add(item)
        db.session.commit()
        flash('Преимущество создано', 'success')
        return redirect(url_for('admin_new.advantage_list'))

    return render_template('admin/generic/form.html',
        entity='advantages', form=form, is_create=True,
        cfg=ADVANTAGE_CFG)


# ── edit ─────────────────────────────────────────────────────────────────

@admin_bp.route('/advantages/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def advantage_edit(item_id):
    if denied := _admin_required():
        return denied

    item = Advantage.query.get_or_404(item_id)
    form = AdvantageForm(obj=item)

    if form.validate_on_submit():
        item.title = form.title.data
        item.text = form.text.data
        item.fa_icon = form.fa_icon.data
        item.icon_type = form.icon_type.data
        item.order = form.order.data or 0

        # Handle SVG file upload if icon_type is 'svg'
        if form.icon_type.data == 'svg':
            file = request.files.get('svg_upload')
            if file and file.filename:
                saved = save_uploaded_file(file, _svg_upload_dir(), ALLOWED_SVG_EXTENSIONS)
                if not saved:
                    flash('Недопустимый формат. Разрешены только SVG', 'error')
                    return render_template('admin/generic/form.html',
                        entity='advantages', form=form, item=item, is_create=False,
                        cfg=ADVANTAGE_CFG)
                # Delete old SVG file if exists
                if item.svg_file:
                    old_path = os.path.join(_svg_upload_dir(), item.svg_file)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                item.svg_file = saved
        else:
            # If switching from svg to fa, delete the old svg file
            if item.svg_file:
                old_path = os.path.join(_svg_upload_dir(), item.svg_file)
                if os.path.exists(old_path):
                    os.remove(old_path)
                item.svg_file = None

        db.session.commit()
        flash('Преимущество обновлено', 'success')
        return redirect(url_for('admin_new.advantage_list'))

    return render_template('admin/generic/form.html',
        entity='advantages', form=form, item=item, is_create=False,
        cfg=ADVANTAGE_CFG)


# ── AJAX: set SVG from gallery ──────────────────────────────────────────

@admin_bp.route('/advantages/<int:item_id>/set-svg', methods=['POST'])
@login_required
def advantage_set_svg(item_id):
    """AJAX: assign an existing SVG file to an advantage."""
    if denied := _admin_required():
        return jsonify({'ok': False, 'error': 'Access denied'}), 403
    item = Advantage.query.get_or_404(item_id)
    data = request.get_json(silent=True) or {}
    svg_file = data.get('svg_file', '')
    svg_dir = _svg_upload_dir()
    if svg_file and os.path.exists(os.path.join(svg_dir, svg_file)):
        item.svg_file = svg_file
        item.icon_type = 'svg'
        db.session.commit()
        return jsonify({
            'ok': True,
            'filename': svg_file,
            'url': url_for('static', filename='uploads/svg_icons/' + svg_file),
        })
    return jsonify({'ok': False, 'error': 'Файл не найден'}), 400


# ── AJAX: upload SVG ────────────────────────────────────────────────────

@admin_bp.route('/advantages/<int:item_id>/upload-svg', methods=['POST'])
@login_required
def advantage_upload_svg(item_id):
    """AJAX: upload SVG file and assign to an advantage."""
    if denied := _admin_required():
        return jsonify({'ok': False, 'error': 'Access denied'}), 403
    item = Advantage.query.get_or_404(item_id)
    file = request.files.get('file')
    if not file or not file.filename:
        return jsonify({'ok': False, 'error': 'Файл не выбран'}), 400
    saved = save_uploaded_file(file, _svg_upload_dir(), ALLOWED_SVG_EXTENSIONS)
    if not saved:
        return jsonify({'ok': False, 'error': 'Недопустимый формат. Разрешены только SVG'}), 400
    item.svg_file = saved
    item.icon_type = 'svg'
    db.session.commit()
    return jsonify({
        'ok': True,
        'filename': saved,
        'url': url_for('static', filename='uploads/svg_icons/' + saved),
    })


# ── delete ───────────────────────────────────────────────────────────────

@admin_bp.route('/advantages/<int:item_id>/delete', methods=['POST'])
@login_required
def advantage_delete(item_id):
    if denied := _admin_required():
        return denied

    item = Advantage.query.get_or_404(item_id)

    # Delete SVG file if exists
    if item.svg_file:
        filepath = os.path.join(_svg_upload_dir(), item.svg_file)
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(item)
    db.session.commit()
    flash('Преимущество удалено', 'success')
    return redirect(url_for('admin_new.advantage_list'))
