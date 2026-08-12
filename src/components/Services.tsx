import { getServices, type ServiceItem } from '@/api';
import { useApiData, useReveal } from '@/hooks';
import { Stethoscope } from 'lucide-react';
import { fallbackAdvantages } from '@/data';

export default function Services() {
  const { ref, visible } = useReveal<HTMLDivElement>();
  const { data } = useApiData(getServices, [], []);

  const services: ServiceItem[] = data.length > 0
    ? data
    : fallbackAdvantages.map((a, i) => ({
        id: i + 1,
        title: a.title,
        description: a.description,
        icon: null,
        order: i,
      }));

  return (
    <section id="services" className="section-padding bg-gradient-to-b from-navy-50/50 to-white">
      <div className="container-narrow">
        <div ref={ref} className={`reveal ${visible ? 'visible' : ''} text-center max-w-2xl mx-auto mb-16`}>
          <span className="badge bg-accent-50 text-accent-700 border border-accent-200">Услуги</span>
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-navy-900 mt-4 mb-4">
            Наши услуги
          </h2>
          <p className="text-gray-500 text-lg">
            Комплексный подход к лечению зависимостей — от детоксикации до социальной адаптации.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((s, i) => (
            <div
              key={s.id}
              className={`reveal ${visible ? 'visible' : ''} group card-hover p-7 flex flex-col items-center text-center`}
              style={{ transitionDelay: `${i * 0.1}s` }}
            >
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-accent-50 to-accent-100 border border-accent-200 flex items-center justify-center mb-5 group-hover:scale-110 transition-transform">
                <Stethoscope className="w-7 h-7 text-accent-600" />
              </div>
              <h3 className="font-display font-bold text-xl text-navy-800 mb-2.5">{s.title}</h3>
              {s.description && <p className="text-gray-500 leading-relaxed text-[15px]">{s.description}</p>}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
