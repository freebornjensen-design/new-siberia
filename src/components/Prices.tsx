import { getPrices, type PriceCategory } from '@/api';
import { useApiData, useReveal } from '@/hooks';
import { CheckCircle } from 'lucide-react';
import { fallbackPrices } from '@/data';

export default function Prices() {
  const { ref, visible } = useReveal<HTMLDivElement>();
  const { data: rawData } = useApiData(getPrices, [], []);
  const data: PriceCategory[] = (rawData as PriceCategory[]).length > 0
    ? (rawData as PriceCategory[])
    : fallbackPrices.map((cat, ci) => ({
        category: cat.category,
        items: cat.items.map((item, ii) => ({
          id: ci * 100 + ii + 1,
          name: item.name,
          price: item.price,
          description: item.description ?? null,
          order: ii,
        })),
      }));

  return (
    <section id="prices" className="section-padding bg-gray-50/50">
      <div className="container-narrow">
        <div ref={ref} className={`reveal ${visible ? 'visible' : ''} text-center max-w-2xl mx-auto mb-16`}>
          <span className="badge bg-brand-50 text-brand-700 border border-brand-200">Стоимость</span>
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-navy-900 mt-4 mb-4">
            Услуги и цены
          </h2>
          <p className="text-gray-500 text-lg">
            Прозрачные тарифы без скрытых платежей. Точную стоимость программы определяет врач после консультации.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {data.map((cat, i) => (
            <div
              key={cat.category}
              className={`reveal ${visible ? 'visible' : ''} card overflow-hidden`}
              style={{ transitionDelay: `${i * 0.15}s` }}
            >
              <div className="bg-gradient-to-r from-navy-700 to-navy-800 px-6 py-4">
                <h3 className="font-display font-bold text-lg text-white">{cat.category}</h3>
              </div>
              <div className="p-6 space-y-3">
                {cat.items.map((item) => (
                  <div key={item.name} className="flex items-start justify-between gap-4 py-3 border-b border-gray-50 last:border-0">
                    <div className="flex items-start gap-2.5">
                      <CheckCircle className="w-4 h-4 text-brand-500 mt-0.5 shrink-0" />
                      <div>
                        <div className="text-sm font-medium text-navy-800">{item.name}</div>
                        {item.description && <div className="text-xs text-gray-400 mt-0.5">{item.description}</div>}
                      </div>
                    </div>
                    <div className="text-sm font-bold text-brand-600 whitespace-nowrap">{item.price}</div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-10">
          <p className="text-gray-400 text-sm">
            * Цены указаны для ознакомления. Окончательная стоимость зависит от индивидуальной программы лечения.
          </p>
        </div>
      </div>
    </section>
  );
}
