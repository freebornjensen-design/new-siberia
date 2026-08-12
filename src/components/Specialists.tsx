import { getPersonnel, type SpecialistItem } from '@/api';
import { useApiData, useReveal } from '@/hooks';
import { Award, User } from 'lucide-react';
import { fallbackSpecialists } from '@/data';

interface SpecialistCard {
  name: string;
  role: string;
  experience: string;
  photo: string | null;
}

export default function Specialists() {
  const { ref, visible } = useReveal<HTMLDivElement>();
  const { data } = useApiData(getPersonnel, [], []);

  const specialists: SpecialistCard[] =
    data.length > 0
      ? data.map((p: SpecialistItem) => ({
          name: p.name,
          role: p.position ?? '',
          experience: p.intro || p.bio || '',
          photo: p.photo_url,
        }))
      : fallbackSpecialists.map((s) => ({
          name: s.name,
          role: s.role,
          experience: s.experience,
          photo: s.photo,
        }));

  return (
    <section id="specialists" className="section-padding bg-gray-50/50">
      <div className="container-narrow">
        <div ref={ref} className={`reveal ${visible ? 'visible' : ''} text-center max-w-2xl mx-auto mb-16`}>
          <span className="badge bg-accent-50 text-accent-700 border border-accent-200">Наша команда</span>
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-navy-900 mt-4 mb-4">
            Специалисты центра
          </h2>
          <p className="text-gray-500 text-lg">
            Врачи и психологи с многолетним опытом работы с зависимостями. Каждый специалист подбирает индивидуальный подход к пациенту.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {specialists.map((spec, i) => (
            <div
              key={spec.name}
              className={`reveal ${visible ? 'visible' : ''} group card-hover overflow-hidden`}
              style={{ transitionDelay: `${i * 0.1}s` }}
            >
              <div className="relative aspect-[3/4] overflow-hidden bg-gray-100">
                {spec.photo ? (
                  <img
                    src={spec.photo}
                    alt={spec.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-navy-50 to-brand-50">
                    <User className="w-16 h-16 text-navy-300" />
                  </div>
                )}
                <div className="absolute bottom-0 inset-x-0 p-5 bg-gradient-to-t from-white via-white/90 to-transparent">
                  <div className="badge bg-brand-50 text-brand-700 border border-brand-200 mb-2">
                    <Award className="w-3 h-3" />
                    {spec.role || 'Специалист'}
                  </div>
                  <h3 className="font-display font-bold text-lg text-navy-800 leading-tight">{spec.name}</h3>
                </div>
              </div>
              <div className="p-5">
                <p className="text-gray-500 text-sm leading-relaxed">{spec.experience}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
