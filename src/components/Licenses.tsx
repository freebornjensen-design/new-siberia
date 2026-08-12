import { useState, useEffect, useCallback } from 'react';
import { getLicenses, type LicenseItem } from '@/api';
import { useApiData, useReveal } from '@/hooks';
import { FileCheck, X, ZoomIn } from 'lucide-react';
import { fallbackLicenses } from '@/data';

export default function Licenses() {
  const { ref, visible } = useReveal<HTMLDivElement>();
  const { data } = useApiData(getLicenses, [], []);
  const [lightbox, setLightbox] = useState<string | null>(null);

  const licenses: LicenseItem[] = data.length > 0 ? data : [];

  const close = useCallback(() => setLightbox(null), []);

  useEffect(() => {
    if (!lightbox) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') close(); };
    window.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [lightbox, close]);

  // Show fallback if no data
  const displayItems = licenses.length > 0
    ? licenses
    : fallbackLicenses.map((l, i) => ({ id: i, title: l.title, description: l.description, image_url: null }));

  return (
    <section id="licenses" className="section-padding bg-gray-50/50">
      <div className="container-narrow">
        <div ref={ref} className={`reveal ${visible ? 'visible' : ''} text-center max-w-2xl mx-auto mb-16`}>
          <span className="badge bg-brand-50 text-brand-700 border border-brand-200">Документы</span>
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-navy-900 mt-4 mb-4">
            Лицензии и сертификаты
          </h2>
          <p className="text-gray-500 text-lg">
            Мы работаем официально. Все лицензии и разрешительные документы в открытом доступе.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {displayItems.map((item, i) => (
            <div
              key={item.id}
              className={`reveal ${visible ? 'visible' : ''} group card-hover p-6 flex flex-col items-center text-center`}
              style={{ transitionDelay: `${i * 0.12}s` }}
            >
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-brand-50 to-brand-100 border border-brand-200 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <FileCheck className="w-8 h-8 text-brand-600" />
              </div>
              <h3 className="font-display font-bold text-navy-800 mb-2">{item.title}</h3>
              {item.description && <p className="text-gray-500 text-sm">{item.description}</p>}
              {item.image_url && (
                <button
                  onClick={() => setLightbox(item.image_url)}
                  className="mt-4 inline-flex items-center gap-1.5 text-brand-600 hover:text-brand-700 font-medium text-sm transition-colors"
                >
                  <ZoomIn className="w-4 h-4" />
                  Посмотреть
                </button>
              )}
            </div>
          ))}
        </div>
      </div>

      {lightbox && (
        <div className="fixed inset-0 z-[100] bg-navy-900/98 backdrop-blur-xl flex items-center justify-center animate-fade-in" onClick={close}>
          <button onClick={close} className="absolute top-6 right-6 w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-white hover:bg-white/20 transition-colors z-10" aria-label="Закрыть">
            <X className="w-6 h-6" />
          </button>
          <img src={lightbox} alt="Лицензия" className="max-w-4xl max-h-[85vh] object-contain rounded-2xl shadow-2xl" onClick={(e) => e.stopPropagation()} />
        </div>
      )}
    </section>
  );
}
