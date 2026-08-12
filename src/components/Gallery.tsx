import { useState, useEffect, useCallback } from 'react';
import { getGallery, type GalleryItem } from '@/api';
import { useApiData, useReveal } from '@/hooks';
import { X, ChevronLeft, ChevronRight, Camera } from 'lucide-react';
import { fallbackGallery } from '@/data';

interface Photo {
  src: string;
  full: string;
  alt: string;
  caption: string;
}

export default function Gallery() {
  const { ref, visible } = useReveal<HTMLDivElement>();
  const { data } = useApiData(getGallery, [], []);
  const [lightboxIndex, setLightboxIndex] = useState<number | null>(null);

  const photos: Photo[] =
    data.length > 0
      ? data.map((img: GalleryItem) => ({
          src: img.thumb_url ?? img.url,
          full: img.full_url ?? img.url,
          alt: img.alt,
          caption: img.title ?? img.alt,
        }))
      : fallbackGallery.map((p) => ({
          src: p.src,
          full: p.src,
          alt: p.alt,
          caption: p.caption,
        }));

  const closeLightbox = useCallback(() => setLightboxIndex(null), []);
  const next = useCallback(() => {
    setLightboxIndex((prev) => (prev === null ? prev : (prev + 1) % photos.length));
  }, [photos.length]);
  const prev = useCallback(() => {
    setLightboxIndex((prev) => (prev === null ? prev : (prev - 1 + photos.length) % photos.length));
  }, [photos.length]);

  useEffect(() => {
    if (lightboxIndex === null) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowRight') next();
      if (e.key === 'ArrowLeft') prev();
    };
    window.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [lightboxIndex, closeLightbox, next, prev]);

  return (
    <section id="gallery" className="section-padding bg-gray-50/50">
      <div className="container-narrow">
        <div ref={ref} className={`reveal ${visible ? 'visible' : ''} text-center max-w-2xl mx-auto mb-16`}>
          <span className="badge bg-brand-50 text-brand-700 border border-brand-200">Галерея</span>
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-navy-900 mt-4 mb-4">
            Фото центра
          </h2>
          <p className="text-gray-500 text-lg">
            Посмотрите, в каких условиях проходит реабилитация. Чистые, светлые и уютные помещения для комфортного восстановления.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {photos.map((photo, i) => (
            <button
              key={photo.src}
              onClick={() => setLightboxIndex(i)}
              className={`reveal ${visible ? 'visible' : ''} group relative rounded-2xl overflow-hidden aspect-[4/3] cursor-pointer hover:ring-4 hover:ring-brand-200 transition-all bg-gray-100`}
              style={{ transitionDelay: `${i * 0.06}s` }}
            >
              <img
                src={photo.src}
                alt={photo.alt}
                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-navy-900/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
              <div className="absolute bottom-0 inset-x-0 p-4 text-left opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="inline-flex items-center gap-1.5 text-white text-sm font-medium">
                  <Camera className="w-3.5 h-3.5 text-brand-400" />
                  {photo.caption}
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {lightboxIndex !== null && (
        <div
          className="fixed inset-0 z-[100] bg-navy-900/98 backdrop-blur-xl flex items-center justify-center animate-fade-in"
          onClick={closeLightbox}
        >
          <button onClick={closeLightbox} className="absolute top-6 right-6 w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-white hover:bg-white/20 transition-colors z-10" aria-label="Закрыть">
            <X className="w-6 h-6" />
          </button>
          <button onClick={(e) => { e.stopPropagation(); prev(); }} className="absolute left-4 sm:left-8 w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-white hover:bg-white/20 transition-colors z-10" aria-label="Предыдущее">
            <ChevronLeft className="w-6 h-6" />
          </button>
          <button onClick={(e) => { e.stopPropagation(); next(); }} className="absolute right-4 sm:right-8 w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-white hover:bg-white/20 transition-colors z-10" aria-label="Следующее">
            <ChevronRight className="w-6 h-6" />
          </button>
          <figure className="max-w-5xl w-full px-4" onClick={(e) => e.stopPropagation()}>
            <img src={photos[lightboxIndex].full} alt={photos[lightboxIndex].alt} className="w-full max-h-[80vh] object-contain rounded-2xl" />
            <figcaption className="text-center text-gray-400 mt-4 text-sm">{photos[lightboxIndex].caption}</figcaption>
          </figure>
        </div>
      )}
    </section>
  );
}
