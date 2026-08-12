"""Admin routes – login, dashboard, contacts, generic CRUD, password change."""
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from admin import admin_bp
from admin.forms import MODEL_CONFIG, NavMenuForm
from admin.utils import _admin_required
from models import (
    Article, Certificate, ChatMessage, ClinicLicense, Contact, MenuItem,
    Personnel, PriceItem, Service, GalleryImage, Statistic, Testimonial,
    Setting, User, db,
)

# ── login / logout ──────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and getattr(current_user, 'is_admin', False):
        return redirect(url_for('admin_new.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_admin:
            login_user(user)
            flash('Вход выполнен', 'success')
            next_url = request.args.get('next') or url_for('admin_new.dashboard')
            return redirect(next_url)
        flash('Неверные учётные данные', 'error')
        return redirect(url_for('admin_new.login'))

    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли', 'info')
    return redirect(url_for('admin_new.login'))


@admin_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if denied := _admin_required():
        return denied

    if request.method == 'POST':
        current_pw = request.form.get('current_password', '')
        new_pw = request.form.get('new_password', '')
        confirm_pw = request.form.get('confirm_password', '')

        if not current_user.check_password(current_pw):
            flash('Текущий пароль неверен', 'error')
        elif len(new_pw) < 6:
            flash('Новый пароль должен быть не менее 6 символов', 'error')
        elif new_pw != confirm_pw:
            flash('Пароли не совпадают', 'error')
        else:
            current_user.set_password(new_pw)
            db.session.commit()
            flash('Пароль успешно изменён', 'success')
            return redirect(url_for('admin_new.dashboard'))

    return render_template('admin/change_password.html')


# ── helpers ──────────────────────────────────────────────────────────────

def _get_model(entity: str):
    """Resolve entity slug to SQLAlchemy model."""
    mapping = {
        'articles': Article, 'services': Service,
        # 'advantages' has custom routes in admin/advantages.py
        # 'daily_audio' has custom routes in admin/daily_audio.py
        # 'certificates' has custom routes in admin/certificates.py
        'statistics': Statistic,
        'settings': Setting,
        'price_items': PriceItem,
        'clinic_licenses': ClinicLicense,
        'menu_items': MenuItem,
    }
    return mapping.get(entity)


# ── dashboard ────────────────────────────────────────────────────────────

@admin_bp.route('/')
@login_required
def dashboard():
    if denied := _admin_required():
        return denied
    return render_template('admin/dashboard.html',
        personnel_count=Personnel.query.count(),
        articles_count=Article.query.count(),
        services_count=Service.query.count(),
        testimonials_count=Testimonial.query.count(),
        certificates_count=Certificate.query.count(),
        gallery_count=GalleryImage.query.count(),
        contacts_count=Contact.query.count(),
        price_items_count=PriceItem.query.count(),
        clinic_licenses_count=ClinicLicense.query.count(),
        menu_items_count=MenuItem.query.count(),
        faq_count=Setting.query.filter(Setting.question.isnot(None), Setting.question != '').count(),
        recent_contacts=Contact.query.order_by(Contact.created_at.desc()).limit(10).all(),
        recent_articles=Article.query.order_by(Article.created_at.desc()).limit(10).all(),
    )


# ── contacts (read-only) ─────────────────────────────────────────────────

@admin_bp.route('/menu', methods=['GET', 'POST'])
@login_required
def nav_menu():
    if denied := _admin_required():
        return denied

    form = NavMenuForm()

    if request.method == 'POST' and form.validate():
        keys = ['nav_dropdown_services', 'nav_dropdown_articles',
                'nav_dropdown_personnel', 'nav_dropdown_faq']
        for key in keys:
            setting = Setting.query.filter_by(key=key).first()
            if not setting:
                setting = Setting(key=key)
                db.session.add(setting)
            setting.value = '1' if request.form.get(key) else '0'
        db.session.commit()
        flash('Настройки меню сохранены', 'success')
        return redirect(url_for('admin_new.nav_menu'))

    # Pre-fill form from DB
    for key in ['nav_dropdown_services', 'nav_dropdown_articles',
                'nav_dropdown_personnel', 'nav_dropdown_faq']:
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            getattr(form, key).data = (setting.value == '1')
        else:
            getattr(form, key).data = True

    return render_template('admin/menu.html', form=form)


@admin_bp.route('/contacts')
@login_required
def contacts():
    if denied := _admin_required():
        return denied
    all_contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=all_contacts)


@admin_bp.route('/contacts/<int:contact_id>/delete', methods=['POST'])
@login_required
def contact_delete(contact_id):
    if denied := _admin_required():
        return denied
    c = Contact.query.get_or_404(contact_id)
    db.session.delete(c)
    db.session.commit()
    flash('Заявка удалена', 'success')
    return redirect(url_for('admin_new.contacts'))


# ── generic CRUD ─────────────────────────────────────────────────────────

# ── Chats ────────────────────────────────────────────────────────────────

@admin_bp.route('/chats')
@login_required
def chats_list():
    if denied := _admin_required():
        return denied
    return render_template('admin/chats.html')


# ── FAQ management (special case: uses Setting model with question/answer) ─

@admin_bp.route('/faq')
@login_required
def faq_list():
    if denied := _admin_required():
        return denied
    items = Setting.query.filter(
        Setting.question.isnot(None), Setting.question != ''
    ).order_by(Setting.id).all()
    return render_template('admin/generic/list.html',
        entity='faq',
        cfg={'title': 'FAQ (Вопросы и ответы)', 'title_singular': 'FAQ', 'columns': ['question', 'answer']},
        items=items, search='')


@admin_bp.route('/faq/create', methods=['GET', 'POST'])
@login_required
def faq_create():
    if denied := _admin_required():
        return denied
    from admin.forms import FAQForm
    form = FAQForm()
    if form.validate_on_submit():
        s = Setting(
            key=f'faq_{Setting.query.count() + 1}',
            question=form.question.data,
            answer=form.answer.data,
            description=form.description.data or 'FAQ',
        )
        db.session.add(s)
        db.session.commit()
        flash('FAQ добавлен', 'success')
        return redirect(url_for('admin_new.faq_list'))
    return render_template('admin/generic/form.html',
        entity='faq',
        cfg={'title': 'FAQ', 'title_singular': 'FAQ'},
        form=form, is_create=True)


@admin_bp.route('/faq/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def faq_edit(item_id):
    if denied := _admin_required():
        return denied
    from admin.forms import FAQForm
    item = Setting.query.get_or_404(item_id)
    form = FAQForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('FAQ обновлён', 'success')
        return redirect(url_for('admin_new.faq_list'))
    return render_template('admin/generic/form.html',
        entity='faq',
        cfg={'title': 'FAQ', 'title_singular': 'FAQ'},
        form=form, item=item, is_create=False)


@admin_bp.route('/faq/<int:item_id>/delete', methods=['POST'])
@login_required
def faq_delete(item_id):
    if denied := _admin_required():
        return denied
    item = Setting.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('FAQ удалён', 'success')
    return redirect(url_for('admin_new.faq_list'))


@admin_bp.route('/chats/<session_id>')
@login_required
def chat_detail(session_id):
    if denied := _admin_required():
        return denied
    # Get user name from first message in this session
    first_msg = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at.asc()).first()
    user_name = first_msg.name if first_msg and first_msg.name else 'Аноним'
    return render_template('admin/chat_detail.html', session_id=session_id, user_name=user_name)


# ── generic CRUD ─────────────────────────────────────────────────────────

@admin_bp.route('/<entity>')
@login_required
def crud_list(entity):
    if denied := _admin_required():
        return denied
    model = _get_model(entity)
    cfg = MODEL_CONFIG.get(entity)
    if not model or not cfg:
        flash('Неизвестная сущность', 'error')
        return redirect(url_for('admin_new.dashboard'))

    query = model.query
    search = request.args.get('q', '').strip()
    if search and cfg.get('search_field'):
        field = getattr(model, cfg['search_field'])
        query = query.filter(field.ilike(f'%{search}%'))

    # default ordering
    if hasattr(model, 'order'):
        query = query.order_by(model.order)
    elif hasattr(model, 'created_at'):
        query = query.order_by(model.created_at.desc())
    else:
        query = query.order_by(model.id)

    items = query.all()
    return render_template('admin/generic/list.html',
        entity=entity, cfg=cfg, items=items, search=search)


@admin_bp.route('/<entity>/create', methods=['GET', 'POST'])
@login_required
def crud_create(entity):
    if denied := _admin_required():
        return denied
    model = _get_model(entity)
    cfg = MODEL_CONFIG.get(entity)
    if not model or not cfg:
        flash('Неизвестная сущность', 'error')
        return redirect(url_for('admin_new.dashboard'))

    form = cfg['form']()
    if form.validate_on_submit():
        item = model()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash(f'{cfg["title_singular"]} создан(а)', 'success')
        return redirect(url_for('admin_new.crud_list', entity=entity))

    return render_template('admin/generic/form.html',
        entity=entity, cfg=cfg, form=form, is_create=True)


@admin_bp.route('/<entity>/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def crud_edit(entity, item_id):
    if denied := _admin_required():
        return denied
    model = _get_model(entity)
    cfg = MODEL_CONFIG.get(entity)
    if not model or not cfg:
        flash('Неизвестная сущность', 'error')
        return redirect(url_for('admin_new.dashboard'))

    item = model.query.get_or_404(item_id)
    form = cfg['form'](obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash(f'{cfg["title_singular"]} обновлен(а)', 'success')
        return redirect(url_for('admin_new.crud_list', entity=entity))

    return render_template('admin/generic/form.html',
        entity=entity, cfg=cfg, form=form, item=item, is_create=False)


@admin_bp.route('/<entity>/<int:item_id>/delete', methods=['POST'])
@login_required
def crud_delete(entity, item_id):
    if denied := _admin_required():
        return denied
    model = _get_model(entity)
    cfg = MODEL_CONFIG.get(entity)
    if not model or not cfg:
        flash('Неизвестная сущность', 'error')
        return redirect(url_for('admin_new.dashboard'))

    item = model.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'{cfg["title_singular"]} удален(а)', 'success')
    return redirect(url_for('admin_new.crud_list', entity=entity))
