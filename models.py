from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Article {self.id} {self.title}>'


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    addiction_type = db.Column(db.String(50), nullable=True)  # тип зависимости: алко/стимуляторы/опиоиды/каннабиноиды/другое
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Contact {self.id} {self.phone}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Personnel(db.Model):
    __tablename__ = 'personnel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=True)
    photo = db.Column(db.String(255), nullable=True)  # filename under static/photo
    achievements = db.Column(db.Text, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    intro = db.Column(db.Text, nullable=True)  # короткое сильное вступление (1-2 предложения)
    full_bio = db.Column(db.Text, nullable=True)  # развёрнутая биография, основной текст
    education = db.Column(db.Text, nullable=True)  # образование (список)
    competencies = db.Column(db.Text, nullable=True)  # ключевые компетенции (маркированный список)
    personal_message = db.Column(db.Text, nullable=True)  # личный посыл / цитата
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    certificates = db.relationship('Certificate', lazy='dynamic', order_by='Certificate.order')

    def __repr__(self):
        return f'<Personnel {self.id} {self.name}>'


class Service(db.Model):
    """Услуги центра"""
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=True, index=True)  # URL: /services/<slug>
    description = db.Column(db.Text, nullable=True)
    meta_title = db.Column(db.String(255), nullable=True)  # SEO title (fallback: title)
    meta_description = db.Column(db.Text, nullable=True)  # SEO meta description (независимо от видимого описания)
    keywords = db.Column(db.String(500), nullable=True)  # SEO keywords
    icon = db.Column(db.String(50), nullable=True)  # icon name/identifier
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Service {self.id} {self.title}>'


class GalleryImage(db.Model):
    """Изображения для галереи"""
    __tablename__ = 'gallery_images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)  # filename under static/uploads/{folder}
    folder = db.Column(db.String(255), nullable=False, default='gallery')  # gallery, personnel, events
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<GalleryImage {self.id} {self.filename}>'


class Testimonial(db.Model):
    """Отзывы клиентов"""
    __tablename__ = 'testimonials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)  # 1-5 stars
    photo = db.Column(db.String(255), nullable=True)  # filename under static/photo
    screenshot = db.Column(db.String(255), nullable=True)  # uploaded screenshot filename under static/uploads/testimonials/
    author_role = db.Column(db.String(100), nullable=True)  # e.g., 'Пациент', 'Родственник'
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Testimonial {self.id} {self.name}>'


class Statistic(db.Model):
    """Статистика 'О нас'"""
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)  # e.g., 'Награды', 'Лет опыта', 'Клиенты', 'Проекты'
    value = db.Column(db.String(50), nullable=False)  # e.g., '17', '12+', '138', '350'
    icon = db.Column(db.String(50), nullable=True)  # icon identifier
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Statistic {self.id} {self.label}>'


class Certificate(db.Model):
    """Сертификаты и дипломы сотрудников"""
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=True, index=True)
    file = db.Column(db.String(255), nullable=False)  # filename under static/certs
    owner = db.Column(db.String(255), nullable=True)  # ФИО / принадлежность
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    personnel = db.relationship('Personnel', back_populates='certificates', foreign_keys=[personnel_id])

    def __repr__(self):
        return f'<Certificate {self.id} {self.owner or self.file}>'


class Advantage(db.Model):
    """Преимущества центра"""
    __tablename__ = 'advantages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=True)
    fa_icon = db.Column(db.String(50), nullable=True, default='fa-check-circle')
    icon_type = db.Column(db.String(10), nullable=False, default='fa')  # 'fa' or 'svg'
    svg_file = db.Column(db.String(255), nullable=True)  # uploaded SVG filename
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Advantage {self.id} {self.title}>'


class DailyAudio(db.Model):
    """Аудиозапись Книги дня"""
    __tablename__ = 'daily_audio'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # Название
    description = db.Column(db.Text, nullable=True)     # Краткое описание
    filename = db.Column(db.String(255), nullable=False)  # Файл под static/uploads/audio/
    audio_date = db.Column(db.Date, nullable=True)       # Дата записи
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<DailyAudio {self.id} {self.title}>'


class ChatMessage(db.Model):
    """Сообщение из чат-виджета на сайте"""
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=True)  # Имя пользователя (запрашивается при первом сообщении)
    message = db.Column(db.Text, nullable=False)
    is_from_admin = db.Column(db.Boolean, default=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<ChatMessage {self.id} {self.session_id[:8]}...>'


class Setting(db.Model):
    """Глобальные настройки"""
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)  # e.g., 'site_title', 'phone', 'email', 'address', 'faq_item_1'
    value = db.Column(db.Text, nullable=True)
    question = db.Column(db.Text, nullable=True)  # for FAQ
    answer = db.Column(db.Text, nullable=True)  # for FAQ
    description = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Setting {self.id} {self.key}>'


class PriceItem(db.Model):
    """Прайс-лист / тарифы"""
    __tablename__ = 'price_items'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255), nullable=False)  # e.g., 'Консультации', 'Вывод из запоя', 'Кодирование'
    name = db.Column(db.String(255), nullable=False)       # Название услуги
    price = db.Column(db.String(100), nullable=True)        # Цена (строка для гибкости: 'от 5 000 ₽', '15 000 ₽')
    description = db.Column(db.Text, nullable=True)          # Примечание / описание тарифа
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<PriceItem {self.id} {self.category} / {self.name}>'


class ClinicLicense(db.Model):
    """Лицензии и сертификаты клиники (не сотрудников)"""
    __tablename__ = 'clinic_licenses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    file = db.Column(db.String(255), nullable=False)  # filename under static/uploads/licenses/
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<ClinicLicense {self.id} {self.title}>'


class MenuItem(db.Model):
    """Пункты навигационного меню (древовидная структура)"""
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=True, index=True)
    title = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(500), nullable=True)      # внешняя ссылка или якорь (#services)
    icon = db.Column(db.String(50), nullable=True)      # CSS класс иконки
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Self-referential relationship for tree
    children = db.relationship(
        'MenuItem', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic', order_by='MenuItem.order',
    )

    def __repr__(self):
        return f'<MenuItem {self.id} {self.title}>'
