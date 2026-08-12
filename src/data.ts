import {
  MapPin,
  BedDouble,
  Users,
  Stethoscope,
  LifeBuoy,
  ShieldCheck,
  type LucideIcon,
} from 'lucide-react';

// ── Fallback data (used while loading or when the API is unavailable) ──

export const PHONE = '+7 983 305-06-90';
export const PHONE_LINK = 'tel:+79833050690';
export const WHATSAPP = 'https://wa.me/79833050690';

export interface FallbackAdvantage {
  icon: LucideIcon;
  title: string;
  description: string;
}

export const fallbackAdvantages: FallbackAdvantage[] = [
  {
    icon: MapPin,
    title: 'В черте города',
    description: 'Удобное расположение в городе — близко к транспорту и близким. Не нужно ехать далеко, чтобы получить помощь.',
  },
  {
    icon: BedDouble,
    title: 'Комфортабельные палаты',
    description: 'Уютные светлые палаты с современными удобствами. Чистота, тепло и домашняя атмосфера на протяжении всего курса.',
  },
  {
    icon: Users,
    title: 'Социальные мероприятия',
    description: 'Регулярные групповые занятия, спорт, творчество и выезды на природу. Помогают восстановить социальные навыки.',
  },
  {
    icon: Stethoscope,
    title: 'Грамотные специалисты',
    description: 'Опытные психотерапевты, наркологи и консультанты с многолетней практикой. Индивидуальный подход к каждому.',
  },
  {
    icon: LifeBuoy,
    title: 'Постпрограммная поддержка',
    description: 'Сопровождение после прохождения программы. Помощь в адаптации и поддержании трезвости в повседневной жизни.',
  },
  {
    icon: ShieldCheck,
    title: 'Анонимность и конфиденциальность',
    description: 'Полная конфиденциальность обращения. Информация о прохождении реабилитации не разглашается третьим лицам.',
  },
];

export interface FallbackSpecialist {
  name: string;
  role: string;
  experience: string;
  photo: string;
}

export const fallbackSpecialists: FallbackSpecialist[] = [
  {
    name: 'Андрей Викторович К.',
    role: 'Главный врач-нарколог',
    experience: '18 лет практики в лечении зависимостей. Автор программ медицинской реабилитации.',
    photo: 'https://images.pexels.com/photos/32254658/pexels-photo-32254658.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  },
  {
    name: 'Елена Сергеевна М.',
    role: 'Психотерапевт',
    experience: '15 лет работы с зависимыми и созависимыми. Когнитивно-поведенческая и семейная терапия.',
    photo: 'https://images.pexels.com/photos/7578810/pexels-photo-7578810.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  },
  {
    name: 'Дмитрий Александрович П.',
    role: 'Психолог-консультант',
    experience: '12 лет опыта. Работает с мотивацией к выздоровлению и групповой терапией.',
    photo: 'https://images.pexels.com/photos/15962798/pexels-photo-15962798.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  },
  {
    name: 'Ольга Николаевна В.',
    role: 'Клинический психолог',
    experience: '10 лет практики. Диагностика, индивидуальное консультирование и арт-терапия.',
    photo: 'https://images.pexels.com/photos/7904478/pexels-photo-7904478.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  },
];

export interface FallbackArticle {
  title: string;
  excerpt: string;
  category: string;
  date: string;
  cover: string;
}

export const fallbackArticles: FallbackArticle[] = [
  {
    title: 'Как распознать зависимость у близкого человека',
    excerpt: 'Первые признаки, на которые стоит обратить внимание, и как правильно начать разговор о помощи.',
    category: 'Зависимости',
    date: '12 марта 2025',
    cover: 'https://images.pexels.com/photos/5710980/pexels-photo-5710980.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  },
  {
    title: 'Этапы реабилитации: что ждёт пациента',
    excerpt: 'От детоксикации до социальной адаптации — подробный обзор каждого этапа программы восстановления.',
    category: 'Реабилитация',
    date: '28 февраля 2025',
    cover: 'https://images.pexels.com/photos/7176302/pexels-photo-7176302.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  },
  {
    title: 'Созависимость: как помочь себе, помогая близкому',
    excerpt: 'Почему поддержка семьи так же важна, как и лечение. Рекомендации для родственников пациентов.',
    category: 'Семья',
    date: '15 января 2025',
    cover: 'https://images.pexels.com/photos/7468213/pexels-photo-7468213.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  },
];

export interface FallbackPhoto {
  src: string;
  alt: string;
  caption: string;
}

export const fallbackGallery: FallbackPhoto[] = [
  {
    src: 'https://images.pexels.com/photos/7031721/pexels-photo-7031721.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
    alt: 'Уютная палата центра',
    caption: 'Комфортабельная палата',
  },
  {
    src: 'https://images.pexels.com/photos/7176302/pexels-photo-7176302.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
    alt: 'Групповое занятие с терапевтом',
    caption: 'Групповая терапия',
  },
  {
    src: 'https://images.pexels.com/photos/7031731/pexels-photo-7031731.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
    alt: 'Спальная комната центра',
    caption: 'Спальная комната',
  },
  {
    src: 'https://images.pexels.com/photos/97083/pexels-photo-97083.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
    alt: 'Интерьер палаты центра',
    caption: 'Интерьер палаты',
  },
  {
    src: 'https://images.pexels.com/photos/7746572/pexels-photo-7746572.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
    alt: 'Комната отдыха центра',
    caption: 'Комната отдыха',
  },
  {
    src: 'https://images.pexels.com/photos/7546638/pexels-photo-7546638.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
    alt: 'Уютная палата центра',
    caption: 'Уютная палата',
  },
];

export interface FallbackAchievement {
  value: number;
  suffix: string;
  label: string;
}

export const fallbackAchievements: FallbackAchievement[] = [
  { value: 500, suffix: '+', label: 'Пациентов прошли реабилитацию' },
  { value: 12, suffix: ' лет', label: 'Опыта работы центра' },
  { value: 78, suffix: '%', label: 'Успешных случаев' },
  { value: 24, suffix: '/7', label: 'Поддержка и сопровождение' },
];

export interface FallbackTestimonial {
  name: string;
  text: string;
}

export const fallbackTestimonials: FallbackTestimonial[] = [
  {
    name: 'Алексей, 34 года',
    text: 'Центр помог мне вернуться к жизни. Команда профессионалов, которые действительно заботятся. Уже 2 года в трезвости.',
  },
  {
    name: 'Марина, мать пациента',
    text: 'Сын прошёл программу полгода назад. Впервые за годы я спокойна за него. Спасибо за постпрограммную поддержку.',
  },
  {
    name: 'Игорь, 41 год',
    text: 'Думал, что уже безнадёжен. Здесь мне показали, что выход есть. Отдельная благодарность психологам.',
  },
];

// ── New fallbacks for prices, licenses, menu, FAQ ─────────────────────

export interface FallbackPriceCategory {
  category: string;
  items: { name: string; price: string; description?: string }[];
}

export const fallbackPrices: FallbackPriceCategory[] = [
  {
    category: 'Консультации',
    items: [
      { name: 'Первичная консультация нарколога', price: 'Бесплатно' },
      { name: 'Консультация психотерапевта', price: '2 500 ₽' },
      { name: 'Консультация психиатра', price: '3 000 ₽' },
    ],
  },
  {
    category: 'Стационарная реабилитация',
    items: [
      { name: 'Стандарт (общая палата)', price: 'от 1 500 ₽/сут.' },
      { name: 'Комфорт (двухместная палата)', price: 'от 2 500 ₽/сут.' },
      { name: 'VIP (одноместная палата)', price: 'от 4 000 ₽/сут.' },
    ],
  },
  {
    category: 'Амбулаторная программа',
    items: [
      { name: 'Индивидуальная терапия', price: '3 000 ₽/сеанс' },
      { name: 'Групповая терапия', price: '1 500 ₽/сеанс' },
      { name: 'Семейная терапия', price: '4 000 ₽/сеанс' },
    ],
  },
];

export interface FallbackFAQ {
  question: string;
  answer: string;
}

export const fallbackFAQ: FallbackFAQ[] = [
  {
    question: 'Сколько длится программа реабилитации?',
    answer: 'Стандартный курс реабилитации длится от 3 до 6 месяцев в зависимости от индивидуальных потребностей пациента. Возможны более короткие (1-2 месяца) и более длительные программы (до 12 месяцев).',
  },
  {
    question: 'Можно ли навещать пациента во время реабилитации?',
    answer: 'Да, мы поощряем участие семьи в процессе выздоровления. Посещения возможны по согласованному графику после адаптационного периода (обычно через 2-3 недели после начала программы).',
  },
  {
    question: 'Гарантируется ли анонимность?',
    answer: 'Абсолютно. Мы не передаём данные пациентов третьим лицам, не ставим на учёт и не отправляем информацию в государственные органы. Все обращения полностью конфиденциальны.',
  },
  {
    question: 'Работаете ли вы с принудительной мотивацией?',
    answer: 'Да, у нас есть специалисты по интервенции, которые помогут мотивировать зависимого на лечение. Мы выезжаем на дом для проведения беседы и убеждения.',
  },
  {
    question: 'Какие методы лечения вы используете?',
    answer: 'Мы применяем комплексный подход: медикаментозная терапия, индивидуальная и групповая психотерапия (КПТ, гештальт, арт-терапия), программа 12 шагов, трудотерапия, спорт и социальная адаптация.',
  },
];

export const fallbackMenu = [
  {
    title: 'Услуги',
    url: '#services',
    children: [
      { title: 'Реабилитация алкогольной зависимости', url: '#services' },
      { title: 'Реабилитация наркотической зависимости', url: '#services' },
      { title: 'Амбулаторная программа', url: '#services' },
      { title: 'Постпрограммное сопровождение', url: '#services' },
    ],
  },
  {
    title: 'О центре',
    url: '#advantages',
    children: [
      { title: 'Преимущества', url: '#advantages' },
      { title: 'Специалисты', url: '#specialists' },
      { title: 'Фото центра', url: '#gallery' },
      { title: 'Лицензии', url: '#licenses' },
    ],
  },
  {
    title: 'Пациентам',
    url: '#prices',
    children: [
      { title: 'Цены', url: '#prices' },
      { title: 'FAQ', url: '#faq' },
      { title: 'Статьи', url: '#articles' },
      { title: 'Отзывы', url: '#achievements' },
    ],
  },
  { title: 'Контакты', url: '#contacts' },
];

export const fallbackLicenses = [
  {
    title: 'Лицензия на медицинскую деятельность',
    description: 'Лицензия № ЛО-54-01-005678 от 15.03.2021',
  },
  {
    title: 'Сертификат соответствия стандартам реабилитации',
    description: 'Выдан Национальной ассоциацией реабилитационных центров',
  },
];
