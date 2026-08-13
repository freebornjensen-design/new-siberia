import { useEffect } from 'react';
import { settingsValue, type Settings } from '@/api';

declare global {
  interface Window {
    dataLayer?: Record<string, unknown>[];
  }
}

function upsertMeta(attr: 'name' | 'property', key: string, content: string) {
  if (!content) return;
  let el = document.head.querySelector<HTMLMetaElement>(`meta[${attr}="${key}"]`);
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  el.setAttribute('content', content);
}

/**
 * Applies SEO meta tags and injects Google Tag Manager from admin settings.
 * The static tags in index.html act as the fallback; these override them
 * at runtime so changes made in the admin take effect without a rebuild.
 */
export default function SeoManager({ settings }: { settings: Settings }) {
  useEffect(() => {
    const fallbackTitle = document.title;
    const title = settingsValue(settings, 'seo_title', fallbackTitle);
    document.title = title;

    upsertMeta('name', 'description', settingsValue(settings, 'seo_description'));
    upsertMeta('name', 'keywords', settingsValue(settings, 'seo_keywords'));
    upsertMeta('property', 'og:title', settingsValue(settings, 'og_title', title));
    upsertMeta('property', 'og:description', settingsValue(settings, 'og_description'));
    upsertMeta('property', 'og:type', 'website');
    upsertMeta('property', 'og:locale', 'ru_RU');
    upsertMeta('property', 'og:image', settingsValue(settings, 'og_image'));

    const gtmId = settingsValue(settings, 'gtm_id');
    if (gtmId && !document.getElementById('gtm-script')) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
      const s = document.createElement('script');
      s.id = 'gtm-script';
      s.async = true;
      s.src = `https://www.googletagmanager.com/gtm.js?id=${gtmId}`;
      document.head.appendChild(s);
    }
  }, [settings]);

  return null;
}
