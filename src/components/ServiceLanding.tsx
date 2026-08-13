import { Phone, ArrowLeft, ChevronRight, Shield, Clock } from 'lucide-react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { useApiData } from '@/hooks';
import { getServices, settingsValue, type Settings, type ServiceItem } from '@/api';
import { PHONE, WHATSAPP } from '@/data';

interface Props {
  slug: string;
  settings: Settings;
}

export default function ServiceLanding({ slug, settings }: Props) {
  const { data, loading } = useApiData(getServices, [], []);
  const services: ServiceItem[] = data;
  const service = services.find((s) => s.slug === slug);

  const phone = settingsValue(settings, 'phone', PHONE);
  const phoneLink = `tel:${phone.replace(/[^\d+]/g, '')}`;

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-navy-500 animate-pulse">Загрузка…</div>
      </div>
    );
  }

  if (!service) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center gap-4 px-6 text-center">
        <h1 className="font-display font-bold text-2xl text-navy-900">Услуга не найдена</h1>
        <p className="text-gray-500">Возможно, страница была перемещена или удалена.</p>
        <a href="/" className="btn-primary">На главную</a>
      </div>
    );
  }

  const otherServices = services.filter((s) => s.slug && s.id !== service.id);

  return (
    <div className="min-h-screen bg-white">
      <Header settings={settings} />
      <main>
        {/* Hero */}
        <section className="relative bg-gradient-to-br from-navy-50 via-white to-brand-50 pt-32 pb-20 sm:pt-40 sm:pb-24">
          <div className="container-narrow">
            <a
              href="/#services"
              className="inline-flex items-center gap-2 text-sm font-medium text-navy-500 hover:text-brand-600 mb-8 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" /> Все услуги
            </a>
            <div className="max-w-3xl">
              <span className="badge bg-brand-50 text-brand-700 border border-brand-200">Услуга центра</span>
              <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-navy-900 leading-[1.1] tracking-tight mt-6 mb-8">
                {service.title}
              </h1>
              <div className="flex flex-col sm:flex-row gap-4">
                <a href={phoneLink} className="btn-primary text-lg px-8 py-4">
                  <Phone className="w-5 h-5" /> {phone}
                </a>
                <a href={WHATSAPP} target="_blank" rel="noopener noreferrer" className="btn-outline text-lg px-8 py-4">
                  Написать в WhatsApp
                </a>
              </div>
              <div className="flex flex-wrap gap-6 mt-10 text-sm text-gray-500">
                <span className="flex items-center gap-2">
                  <Shield className="w-4 h-4 text-brand-600" /> Анонимно и конфиденциально
                </span>
                <span className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-brand-600" /> Круглосуточно, 7 дней в неделю
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* Content */}
        <section className="section-padding">
          <div className="container-narrow">
            <div className="grid lg:grid-cols-3 gap-12">
              <article className="lg:col-span-2">
                {service.description ? (
                  <div className="text-lg text-gray-600 leading-relaxed whitespace-pre-line">
                    {service.description}
                  </div>
                ) : (
                  <p className="text-gray-500">
                    Подробное описание услуги появится здесь. Позвоните нам — расскажем всё о программе и условиях.
                  </p>
                )}

                <div className="mt-12 p-6 sm:p-8 rounded-3xl bg-navy-900 text-white">
                  <h2 className="font-display font-bold text-2xl mb-3">Нужна помощь прямо сейчас?</h2>
                  <p className="text-navy-200 mb-6">
                    Позвоните — консультация бесплатная и анонимная. Поможем подобрать программу и ответим на все вопросы.
                  </p>
                  <a href={phoneLink} className="btn-primary text-lg">
                    <Phone className="w-5 h-5" /> {phone}
                  </a>
                </div>
              </article>

              {otherServices.length > 0 && (
                <aside>
                  <h3 className="font-display font-bold text-xl text-navy-800 mb-4">Другие услуги</h3>
                  <div className="space-y-3">
                    {otherServices.map((s) => (
                      <a
                        key={s.id}
                        href={`/services/${s.slug}`}
                        className="card-hover p-4 flex items-center justify-between gap-2 group"
                      >
                        <span className="font-medium text-navy-700 group-hover:text-brand-600 transition-colors">
                          {s.title}
                        </span>
                        <ChevronRight className="w-4 h-4 shrink-0 text-gray-400 group-hover:text-brand-600 transition-colors" />
                      </a>
                    ))}
                  </div>
                </aside>
              )}
            </div>
          </div>
        </section>
      </main>
      <Footer settings={settings} />
    </div>
  );
}
