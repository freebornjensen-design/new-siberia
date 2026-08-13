"""WTForms for all admin-editable models."""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, IntegerField, BooleanField,
    SelectField, SubmitField, DateField, FileField,
)
from wtforms.validators import DataRequired, Optional, Length, NumberRange

from admin.utils import slugify


class ArticleForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=255)])
    body = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class ServiceForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=255)])
    slug = StringField('URL (slug, латиница)', validators=[Optional(), Length(max=255)],
        description='Оставляйте пустым — сгенерируется автоматически из названия. Пример: vyvod-iz-zapoya')
    description = TextAreaField('Описание (текст страницы)', validators=[Optional()])
    meta_title = StringField('SEO Title (заголовок вкладки)', validators=[Optional(), Length(max=255)],
        description='Пусто = используется название услуги')
    meta_description = TextAreaField('SEO описание (meta description, до 160 симв.)', validators=[Optional(), Length(max=160)], render_kw={'rows': 3, 'maxlength': 160})
    keywords = StringField('Ключевые слова (через запятую)', validators=[Optional(), Length(max=500)])
    icon = StringField('Иконка', validators=[Optional(), Length(max=50)])
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    submit = SubmitField('Сохранить')

    def populate_obj(self, obj):
        super().populate_obj(obj)
        if not obj.slug:
            obj.slug = slugify(obj.title)
        # Ensure uniqueness (append -2, -3, … on collision)
        from models import Service
        q = Service.query.filter(Service.slug == obj.slug)
        if getattr(obj, 'id', None):
            q = q.filter(Service.id != obj.id)
        if q.first():
            i = 2
            while Service.query.filter_by(slug=f'{obj.slug}-{i}').first():
                i += 1
            obj.slug = f'{obj.slug}-{i}'


class StatisticForm(FlaskForm):
    label = StringField('Название', validators=[DataRequired(), Length(max=100)])
    value = StringField('Значение', validators=[DataRequired(), Length(max=50)])
    icon = StringField('Иконка', validators=[Optional(), Length(max=50)])
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    submit = SubmitField('Сохранить')


class TestimonialForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(max=120)])
    text = TextAreaField('Текст отзыва', validators=[DataRequired()])
    rating = IntegerField(
        'Оценка (1-5)',
        validators=[Optional(), NumberRange(min=1, max=5)],
        default=5,
    )
    author_role = StringField('Роль', validators=[Optional(), Length(max=100)])
    screenshot_file = FileField('Скриншот отзыва', validators=[Optional()])
    screenshot = StringField('Имя файла скриншота (заполняется автоматически)', validators=[Optional(), Length(max=255)], render_kw={'readonly': True, 'disabled': True})
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    submit = SubmitField('Сохранить')


class SettingForm(FlaskForm):
    key = StringField('Ключ', validators=[DataRequired(), Length(max=100)])
    value = TextAreaField('Значение', validators=[Optional()])
    question = TextAreaField('Вопрос (FAQ)', validators=[Optional()])
    answer = TextAreaField('Ответ (FAQ)', validators=[Optional()])
    description = StringField('Описание', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Сохранить')


class CertificateForm(FlaskForm):
    personnel_id = SelectField('Сотрудник', coerce=int, validators=[Optional()])
    cert_file = FileField('Скан сертификата', validators=[Optional()])
    file = StringField('Имя файла (заполняется автоматически)', validators=[Optional(), Length(max=255)], render_kw={'readonly': True, 'disabled': True})
    owner = StringField('Принадлежность (ФИО)', validators=[Optional(), Length(max=255)])
    description = TextAreaField('Описание', validators=[Optional()])
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from models import Personnel
        self.personnel_id.choices = [(0, '— Не выбрано —')] + [
            (p.id, p.name) for p in Personnel.query.order_by(Personnel.order, Personnel.name).all()
        ]


# ── Раздел Font Awesome иконок ──
FA_CHOICES = [
    ('fas fa-check-circle', '✓ fa-check-circle'),
    ('fas fa-check', '✓ fa-check'),
    ('fas fa-heart', '♥ fa-heart'),
    ('fas fa-heartbeat', '♥ fa-heartbeat'),
    ('fas fa-star', '★ fa-star'),
    ('fas fa-trophy', '🏆 fa-trophy'),
    ('fas fa-award', '🏅 fa-award'),
    ('fas fa-medal', '🥇 fa-medal'),
    ('fas fa-shield-alt', '🛡 fa-shield-alt'),
    ('fas fa-hand-holding-heart', '🤝 fa-hand-holding-heart'),
    ('fas fa-hands-helping', '🤝 fa-hands-helping'),
    ('fas fa-handshake', '🤝 fa-handshake'),
    ('fas fa-user-md', '👨‍⚕️ fa-user-md'),
    ('fas fa-user-check', '✓ fa-user-check'),
    ('fas fa-users', '👥 fa-users'),
    ('fas fa-user-friends', '👥 fa-user-friends'),
    ('fas fa-brain', '🧠 fa-brain'),
    ('fas fa-leaf', '🌿 fa-leaf'),
    ('fas fa-seedling', '🌱 fa-seedling'),
    ('fas fa-tree', '🌳 fa-tree'),
    ('fas fa-clock', '🕐 fa-clock'),
    ('fas fa-calendar-check', '📅 fa-calendar-check'),
    ('fas fa-chart-line', '📈 fa-chart-line'),
    ('fas fa-chart-bar', '📊 fa-chart-bar'),
    ('fas fa-chart-pie', '📊 fa-chart-pie'),
    ('fas fa-graduation-cap', '🎓 fa-graduation-cap'),
    ('fas fa-book', '📚 fa-book'),
    ('fas fa-book-open', '📖 fa-book-open'),
    ('fas fa-lightbulb', '💡 fa-lightbulb'),
    ('fas fa-flask', '🔬 fa-flask'),
    ('fas fa-microscope', '🔬 fa-microscope'),
    ('fas fa-clinic-medical', '🏥 fa-clinic-medical'),
    ('fas fa-hospital', '🏥 fa-hospital'),
    ('fas fa-procedures', '🛏 fa-procedures'),
    ('fas fa-stethoscope', '🩺 fa-stethoscope'),
    ('fas fa-syringe', '💉 fa-syringe'),
    ('fas fa-pills', '💊 fa-pills'),
    ('fas fa-capsules', '💊 fa-capsules'),
    ('fas fa-dna', '🧬 fa-dna'),
    ('fas fa-walking', '🚶 fa-walking'),
    ('fas fa-running', '🏃 fa-running'),
    ('fas fa-smile', '🙂 fa-smile'),
    ('fas fa-smile-beam', '😄 fa-smile-beam'),
    ('fas fa-cog', '⚙ fa-cog'),
    ('fas fa-fire', '🔥 fa-fire'),
    ('fas fa-globe', '🌐 fa-globe'),
    ('fas fa-phone', '📞 fa-phone'),
    ('fas fa-envelope', '📧 fa-envelope'),
    ('fas fa-map-marker-alt', '📍 fa-map-marker-alt'),
    ('fas fa-home', '🏠 fa-home'),
    ('fas fa-building', '🏢 fa-building'),
    ('fas fa-balance-scale', '⚖ fa-balance-scale'),
    ('fas fa-magic', '✨ fa-magic'),
    ('fas fa-search', '🔍 fa-search'),
    ('fas fa-eye', '👁 fa-eye'),
    ('fas fa-thumbs-up', '👍 fa-thumbs-up'),
    ('fas fa-rocket', '🚀 fa-rocket'),
    ('fas fa-infinity', '∞ fa-infinity'),
    ('fas fa-shield-virus', '🛡 fa-shield-virus'),
    ('fas fa-lungs', '🫁 fa-lungs'),
]

# ── Раздел Remix Icon иконок ──
RI_CHOICES = [
    ('ri ri-heart-line', '♥ ri-heart-line'),
    ('ri ri-heart-fill', '♥ ri-heart-fill'),
    ('ri ri-heart-pulse-line', '♥ ri-heart-pulse-line'),
    ('ri ri-heart-pulse-fill', '♥ ri-heart-pulse-fill'),
    ('ri ri-star-line', '★ ri-star-line'),
    ('ri ri-star-fill', '★ ri-star-fill'),
    ('ri ri-award-line', '🏅 ri-award-line'),
    ('ri ri-medal-line', '🥇 ri-medal-line'),
    ('ri ri-medal-fill', '🥇 ri-medal-fill'),
    ('ri ri-trophy-line', '🏆 ri-trophy-line'),
    ('ri ri-trophy-fill', '🏆 ri-trophy-fill'),
    ('ri ri-shield-check-line', '🛡 ri-shield-check-line'),
    ('ri ri-shield-star-line', '🛡 ri-shield-star-line'),
    ('ri ri-hand-heart-line', '🤝 ri-hand-heart-line'),
    ('ri ri-hand-heart-fill', '🤝 ri-hand-heart-fill'),
    ('ri ri-hands-line', '🤝 ri-hands-line'),
    ('ri ri-handshake-line', '🤝 ri-handshake-line'),
    ('ri ri-nurse-line', '👩‍⚕️ ri-nurse-line'),
    ('ri ri-nurse-fill', '👩‍⚕️ ri-nurse-fill'),
    ('ri ri-stethoscope-line', '🩺 ri-stethoscope-line'),
    ('ri ri-user-heart-line', '👤♥ ri-user-heart-line'),
    ('ri ri-user-heart-fill', '👤♥ ri-user-heart-fill'),
    ('ri ri-group-line', '👥 ri-group-line'),
    ('ri ri-group-2-line', '👥 ri-group-2-line'),
    ('ri ri-brain-line', '🧠 ri-brain-line'),
    ('ri ri-brain-fill', '🧠 ri-brain-fill'),
    ('ri ri-psychotherapy-line', '🧠 ri-psychotherapy-line'),
    ('ri ri-mental-health-line', '🧠 ri-mental-health-line'),
    ('ri ri-leaf-line', '🌿 ri-leaf-line'),
    ('ri ri-seedling-line', '🌱 ri-seedling-line'),
    ('ri ri-tree-line', '🌳 ri-tree-line'),
    ('ri ri-flower-line', '🌸 ri-flower-line'),
    ('ri ri-sun-line', '☀ ri-sun-line'),
    ('ri ri-moon-line', '🌙 ri-moon-line'),
    ('ri ri-time-line', '🕐 ri-time-line'),
    ('ri ri-calendar-check-line', '📅 ri-calendar-check-line'),
    ('ri ri-bar-chart-line', '📊 ri-bar-chart-line'),
    ('ri ri-bar-chart-fill', '📊 ri-bar-chart-fill'),
    ('ri ri-line-chart-line', '📈 ri-line-chart-line'),
    ('ri ri-graduation-cap-line', '🎓 ri-graduation-cap-line'),
    ('ri ri-book-line', '📚 ri-book-line'),
    ('ri ri-book-open-line', '📖 ri-book-open-line'),
    ('ri ri-lightbulb-line', '💡 ri-lightbulb-line'),
    ('ri ri-flask-line', '🔬 ri-flask-line'),
    ('ri ri-hospital-line', '🏥 ri-hospital-line'),
    ('ri ri-hospital-fill', '🏥 ri-hospital-fill'),
    ('ri ri-first-aid-kit-line', '🩹 ri-first-aid-kit-line'),
    ('ri ri-first-aid-kit-fill', '🩹 ri-first-aid-kit-fill'),
    ('ri ri-pulse-line', '♥ ri-pulse-line'),
    ('ri ri-drug-line', '💊 ri-drug-line'),
    ('ri ri-capsule-line', '💊 ri-capsule-line'),
    ('ri ri-health-book-line', '📖 ri-health-book-line'),
    ('ri ri-walk-line', '🚶 ri-walk-line'),
    ('ri ri-run-line', '🏃 ri-run-line'),
    ('ri ri-bike-line', '🚲 ri-bike-line'),
    ('ri ri-smile-line', '🙂 ri-smile-line'),
    ('ri ri-smile-fill', '😄 ri-smile-fill'),
    ('ri ri-emotion-happy-line', '😊 ri-emotion-happy-line'),
    ('ri ri-settings-line', '⚙ ri-settings-line'),
    ('ri ri-fire-line', '🔥 ri-fire-line'),
    ('ri ri-fire-fill', '🔥 ri-fire-fill'),
    ('ri ri-globe-line', '🌐 ri-globe-line'),
    ('ri ri-earth-line', '🌏 ri-earth-line'),
    ('ri ri-phone-line', '📞 ri-phone-line'),
    ('ri ri-mail-line', '📧 ri-mail-line'),
    ('ri ri-map-pin-line', '📍 ri-map-pin-line'),
    ('ri ri-home-line', '🏠 ri-home-line'),
    ('ri ri-building-line', '🏢 ri-building-line'),
    ('ri ri-search-line', '🔍 ri-search-line'),
    ('ri ri-eye-line', '👁 ri-eye-line'),
    ('ri ri-thumb-up-line', '👍 ri-thumb-up-line'),
    ('ri ri-thumb-up-fill', '👍 ri-thumb-up-fill'),
    ('ri ri-rocket-line', '🚀 ri-rocket-line'),
    ('ri ri-rocket-fill', '🚀 ri-rocket-fill'),
    ('ri ri-shield-line', '🛡 ri-shield-line'),
    ('ri ri-shield-fill', '🛡 ri-shield-fill'),
    ('ri ri-safe-line', '🛡 ri-safe-line'),
    ('ri ri-syringe-line', '💉 ri-syringe-line'),
    ('ri ri-thermometer-line', '🌡 ri-thermometer-line'),
    ('ri ri-blood-drop-line', '🩸 ri-blood-drop-line'),
    ('ri ri-restaurant-line', '🍽 ri-restaurant-line'),
    ('ri ri-cup-line', '☕ ri-cup-line'),
    ('ri ri-water-flash-line', '💧 ri-water-flash-line'),
]


class AdvantageForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField('Текст', validators=[Optional()])
    fa_icon = SelectField('Иконка (FA/Remix)', choices=FA_CHOICES + RI_CHOICES, default='fas fa-check-circle')
    icon_type = SelectField('Тип иконки', choices=[('fa', 'Font Awesome / Remix'), ('svg', 'SVG файл')], default='fa')
    svg_upload = FileField('SVG файл (если тип SVG)', validators=[Optional()])
    svg_file = StringField('Имя SVG файла (заполняется автоматически)', validators=[Optional(), Length(max=255)], render_kw={'readonly': True})
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    submit = SubmitField('Сохранить')


class PersonnelForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(max=120)])
    position = StringField('Должность', validators=[Optional(), Length(max=120)])
    photo = StringField('Фото', validators=[Optional(), Length(max=255)])
    intro = TextAreaField('Вступление (1-2 предложения)', validators=[Optional()])
    full_bio = TextAreaField('Развёрнутая биография', validators=[Optional()])
    achievements = TextAreaField('Достижения', validators=[Optional()])
    bio = TextAreaField('Биография (кратко)', validators=[Optional()])
    education = TextAreaField('Образование', validators=[Optional()])
    competencies = TextAreaField('Ключевые компетенции', validators=[Optional()])
    personal_message = TextAreaField('Личный посыл / цитата', validators=[Optional()])
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    submit = SubmitField('Сохранить')


class DailyAudioForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Описание', validators=[Optional()])
    audio_file = FileField('Аудиофайл (MP3)', validators=[Optional()])
    filename = StringField('Имя файла (заполняется автоматически)', validators=[Optional(), Length(max=255)], render_kw={'readonly': True, 'disabled': True})
    audio_date = DateField('Дата записи', validators=[Optional()], format='%Y-%m-%d')
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    submit = SubmitField('Сохранить')


class NavMenuForm(FlaskForm):
    """Form for enabling/disabling dropdown per nav item."""
    nav_dropdown_services = BooleanField('Услуги', default=True)
    nav_dropdown_articles = BooleanField('Блог', default=True)
    nav_dropdown_personnel = BooleanField('Персонал', default=True)
    nav_dropdown_faq = BooleanField('Вопросы', default=True)
    submit = SubmitField('Сохранить')


class PriceItemForm(FlaskForm):
    category = StringField('Категория', validators=[DataRequired(), Length(max=255)])
    name = StringField('Название услуги', validators=[DataRequired(), Length(max=255)])
    price = StringField('Цена', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Примечание', validators=[Optional()])
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    is_active = BooleanField('Активно', default=True)
    submit = SubmitField('Сохранить')


class ClinicLicenseForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=255)])
    license_file = FileField('Скан лицензии', validators=[Optional()])
    file = StringField('Имя файла (заполняется автоматически)', validators=[Optional(), Length(max=255)], render_kw={'readonly': True, 'disabled': True})
    description = TextAreaField('Описание', validators=[Optional()])
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    submit = SubmitField('Сохранить')


class MenuItemForm(FlaskForm):
    parent_id = SelectField('Родительский пункт', coerce=int, validators=[Optional()])
    title = StringField('Название', validators=[DataRequired(), Length(max=120)])
    url = StringField('Ссылка (URL или #якорь)', validators=[Optional(), Length(max=500)])
    icon = StringField('CSS класс иконки', validators=[Optional(), Length(max=50)])
    order = IntegerField('Порядок', validators=[Optional()], default=0)
    is_active = BooleanField('Активно', default=True)
    submit = SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from models import MenuItem
        self.parent_id.choices = [(0, '— Корневой уровень —')] + [
            (m.id, m.title) for m in MenuItem.query.order_by(MenuItem.order, MenuItem.title).all()
        ]


class FAQForm(FlaskForm):
    question = TextAreaField('Вопрос', validators=[DataRequired()])
    answer = TextAreaField('Ответ', validators=[Optional()])
    description = StringField('Описание (служебное)', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Сохранить')


# Map model names to form classes and display names
MODEL_CONFIG = {
    'articles': {
        'model_name': 'Article',
        'form': ArticleForm,
        'title': 'Статьи',
        'title_singular': 'Статья',
        'columns': ['title', 'created_at'],
        'search_field': 'title',
    },
    'services': {
        'model_name': 'Service',
        'form': ServiceForm,
        'title': 'Услуги',
        'title_singular': 'Услуга',
        'columns': ['title', 'slug', 'order', 'created_at'],
        'search_field': 'title',
    },
    'statistics': {
        'model_name': 'Statistic',
        'form': StatisticForm,
        'title': 'Статистика',
        'title_singular': 'Статистика',
        'columns': ['label', 'value', 'order'],
        'search_field': 'label',
    },
    'price_items': {
        'model_name': 'PriceItem',
        'form': PriceItemForm,
        'title': 'Цены',
        'title_singular': 'Цена',
        'columns': ['category', 'name', 'price', 'order', 'is_active'],
        'list_fields': ['category', 'name', 'price', 'order', 'is_active'],
        'search_field': 'name',
    },
    'clinic_licenses': {
        'model_name': 'ClinicLicense',
        'form': ClinicLicenseForm,
        'title': 'Лицензии клиники',
        'title_singular': 'Лицензия',
        'columns': ['title', 'order'],
        'search_field': 'title',
    },
    'menu_items': {
        'model_name': 'MenuItem',
        'form': MenuItemForm,
        'title': 'Меню',
        'title_singular': 'Пункт меню',
        'columns': ['title', 'url', 'order', 'is_active'],
        'search_field': 'title',
    },
    # 'testimonials' has custom routes in admin/testimonials.py
    # 'advantages' has custom routes in admin/advantages.py
    # 'certificates' has custom routes in admin/certificates.py
    'settings': {
        'model_name': 'Setting',
        'form': SettingForm,
        'title': 'Настройки',
        'title_singular': 'Настройка',
        'columns': ['key', 'value', 'description', 'updated_at'],
        'search_field': 'key',
    },
}
