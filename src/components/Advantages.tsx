import { getAdvantages, type AdvantageItem } from '@/api';
import { useApiData, useReveal } from '@/hooks';
import { CheckCircle } from 'lucide-react';
import { fallbackAdvantages } from '@/data';
import AdvantageGlyph, { type DisplayAdvantage } from '@/AdvantageGlyph';

function toDisplay(list: AdvantageItem[]): DisplayAdvantage[] {
  return list.map((a) => ({
    title: a.title,
    description: a.text ?? '',
    icon_type: a.icon_type === 'svg' ? 'svg' : 'fa',
    fa_icon: a.fa_icon,
    svg_url: a.svg_url,
  }));
}

export default function Advantages() {
  const { ref, visible } = useReveal<HTMLDivElement>();
  const { data } = useApiData(getAdvantages, [], []);

  const advantages: DisplayAdvantage[] =
    data.length > 0
      ? toDisplay(data)
      : fallbackAdvantages.map((a) => ({
          title: a.title,
          description: a.description,
          icon_type: 'lucide' as const,
          lucide: a.icon,
        }));

  return (
    <section id="advantages" className="section-padding bg-white">
      <div className="container-narrow">
        <div ref={ref} className={`reveal ${visible ? 'visible' : ''} text-center max-w-2xl mx-auto mb-16`}>
          <span className="badge bg-brand-50 text-brand-700 border border-brand-200">Почему мы</span>
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-navy-900 mt-4 mb-4">
            Преимущества центра
          </h2>
          <p className="text-gray-500 text-lg">
            Мы создали условия, в которых выздоровление проходит комфортно и эффективно — от первой консультации до возвращения к обычной жизни.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {advantages.map((adv, i) => (
            <div
              key={adv.title}
              className={`reveal ${visible ? 'visible' : ''} group card-hover p-7 relative`}
              style={{ transitionDelay: `${i * 0.1}s` }}
            >
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-50 to-brand-100 border border-brand-200 flex items-center justify-center mb-5 group-hover:scale-110 group-hover:border-brand-300 transition-all">
                <AdvantageGlyph adv={adv} size={28} iconClassName="text-brand-600" />
              </div>
              <h3 className="font-display font-bold text-xl text-navy-800 mb-2.5">{adv.title}</h3>
              <p className="text-gray-500 leading-relaxed text-[15px]">{adv.description}</p>
              <CheckCircle className="absolute top-7 right-7 w-5 h-5 text-brand-200 group-hover:text-brand-400 transition-colors" />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
