import { Phone, ChevronDown, Shield, Award, Clock } from 'lucide-react';
import { PHONE } from '@/data';

const stats = [
  { icon: Shield, value: '500+', label: 'Пациентов помогли' },
  { icon: Award, value: '12 лет', label: 'Опыта работы' },
  { icon: Clock, value: '24/7', label: 'Поддержка' },
];

export default function Hero() {
  return (
    <section id="top" className="relative min-h-screen flex flex-col overflow-hidden bg-gradient-to-br from-navy-50 via-white to-brand-50">
      {/* Background pattern */}
      <div className="absolute inset-0 z-0 opacity-[0.03] bg-[radial-gradient(#1e3a5f_1px,transparent_1px)] [background-size:24px_24px]" />

      {/* Hero image */}
      <div className="absolute top-0 right-0 w-full lg:w-[55%] h-[60vh] lg:h-full z-0">
        <div className="absolute inset-0 bg-gradient-to-r from-navy-50 via-white/80 to-transparent lg:from-white/60 lg:to-transparent z-10" />
        <img
          src="https://images.pexels.com/photos/7176302/pexels-photo-7176302.jpeg?auto=compress&cs=tinysrgb&h=650&w=940"
          alt=""
          className="w-full h-full object-cover"
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-5 sm:px-8 flex-1 flex flex-col justify-center pt-28 pb-16">
        <div className="max-w-2xl">
          <div className="badge bg-brand-50 text-brand-700 border border-brand-200 mb-6 animate-fade-up">
            <Shield className="w-3.5 h-3.5" />
            Анонимно и конфиденциально
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl lg:text-6xl text-navy-900 leading-[1.1] tracking-tight mb-6 animate-fade-up" style={{ animationDelay: '0.1s' }}>
            Реабилитационный центр <span className="text-gradient">«Новая Сибирь»</span>
          </h1>
          <p className="text-lg sm:text-xl text-gray-600 leading-relaxed max-w-xl mb-8 animate-fade-up" style={{ animationDelay: '0.2s' }}>
            Комплексное лечение наркотической и алкогольной зависимости. Опытные специалисты, комфортные условия и поддержка на каждом этапе пути к выздоровлению.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 animate-fade-up" style={{ animationDelay: '0.3s' }}>
            <a href={`tel:${PHONE.replace(/[^\d+]/g, '')}`} className="btn-primary text-lg px-8 py-4">
              <Phone className="w-5 h-5" />
              Записаться на консультацию
            </a>
            <a href="#services" className="btn-outline text-lg px-8 py-4">
              Наши услуги
            </a>
          </div>

          {/* Stats row */}
          <div className="flex gap-8 sm:gap-12 mt-12 animate-fade-up" style={{ animationDelay: '0.4s' }}>
            {stats.map((s) => (
              <div key={s.label} className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-brand-50 flex items-center justify-center">
                  <s.icon className="w-5 h-5 text-brand-600" />
                </div>
                <div>
                  <div className="font-display font-bold text-xl text-navy-800">{s.value}</div>
                  <div className="text-sm text-gray-500">{s.label}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <a
        href="#advantages"
        className="relative z-10 mx-auto mb-8 w-12 h-12 rounded-full bg-white shadow-lg border border-gray-100 flex items-center justify-center text-gray-400 hover:text-brand-600 hover:border-brand-200 transition-all animate-float"
        aria-label="Прокрутить вниз"
      >
        <ChevronDown className="w-5 h-5" />
      </a>
    </section>
  );
}
