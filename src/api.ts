// ── Types (mirror of the Flask /api/* JSON) ──────────────────────────

export interface AdvantageItem {
  id: number;
  title: string;
  text: string | null;
  fa_icon: string | null;
  icon_type: 'fa' | 'svg';
  svg_url: string | null;
  order: number;
}

export interface SpecialistItem {
  id: number;
  name: string;
  position: string | null;
  photo_url: string | null;
  bio: string | null;
  intro: string | null;
  order: number;
}

export interface ArticleItem {
  id: number;
  title: string;
  excerpt: string;
  body: string | null;
  date: string | null;
  created_at: string | null;
}

export interface GalleryItem {
  id: number;
  filename: string;
  url: string;
  full_url: string;
  thumb_url: string;
  title: string | null;
  alt: string;
}

export interface StatisticItem {
  id: number;
  label: string;
  value: string;
  icon: string | null;
  order: number;
}

export interface TestimonialItem {
  id: number;
  name: string;
  text: string;
  rating: number | null;
  screenshot_url: string | null;
}

export interface PriceCategory {
  category: string;
  items: PriceRow[];
}

export interface PriceRow {
  id: number;
  name: string;
  price: string | null;
  description: string | null;
  order: number;
}

export interface LicenseItem {
  id: number;
  title: string;
  description: string | null;
  image_url: string | null;
}

export interface MenuNode {
  id: number;
  title: string;
  url: string | null;
  icon: string | null;
  children?: MenuNode[];
}

export interface FAQItem {
  id: number;
  question: string;
  answer: string;
}

export interface Settings {
  [key: string]: string | null;
}

export interface ServiceItem {
  id: number;
  title: string;
  slug: string | null;
  description: string | null;
  icon: string | null;
  order: number;
}

// ── Fetch helpers ─────────────────────────────────────────────────────

async function getJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} → ${res.status}`);
  return res.json() as Promise<T>;
}

export const getSettings = () => getJSON<Settings>('/api/settings');
export const getAdvantages = () => getJSON<AdvantageItem[]>('/api/advantages');
export const getPersonnel = () => getJSON<SpecialistItem[]>('/api/personnel');
export const getArticles = () => getJSON<ArticleItem[]>('/api/articles');
export const getGallery = () => getJSON<GalleryItem[]>('/api/gallery');
export const getStatistics = () => getJSON<StatisticItem[]>('/api/statistics');
export const getTestimonials = () => getJSON<TestimonialItem[]>('/api/testimonials');
export const getPrices = () => getJSON<PriceCategory[]>('/api/prices');
export const getLicenses = () => getJSON<LicenseItem[]>('/api/licenses');
export const getMenu = () => getJSON<MenuNode[]>('/api/menu');
export const getFAQ = () => getJSON<FAQItem[]>('/api/faq');
export const getServices = () => getJSON<ServiceItem[]>('/api/services');

// ── Settings helpers with fallbacks ───────────────────────────────────

export const settingsValue = (settings: Settings, key: string, fallback = '') =>
  settings[key]?.trim() || fallback;
