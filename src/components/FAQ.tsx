import { useState } from 'react';
import { getFAQ, type FAQItem } from '@/api';
import { useApiData, useReveal } from '@/hooks';
import { ChevronDown, HelpCircle } from 'lucide-react';
import { fallbackFAQ } from '@/data';

function FAQAccordion({ item, open, onToggle }: { item: FAQItem; open: boolean; onToggle: () => void }) {
  return (
    <div className="card overflow-hidden transition-all">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between gap-4 px-6 py-5 text-left hover:bg-gray-50/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <HelpCircle className={`w-5 h-5 shrink-0 transition-colors ${open ? 'text-brand-500' : 'text-gray-400'}`} />
          <span className={`font-semibold transition-colors ${open ? 'text-navy-800' : 'text-navy-700'}`}>{item.question}</span>
        </div>
        <ChevronDown className={`w-5 h-5 shrink-0 text-gray-400 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      <div className={`overflow-hidden transition-all duration-300 ${open ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'}`}>
        <div className="px-6 pb-5 pl-14 text-gray-600 leading-relaxed text-[15px]">{item.answer}</div>
      </div>
    </div>
  );
}

export default function FAQ() {
  const { ref, visible } = useReveal<HTMLDivElement>();
  const { data: rawData } = useApiData(getFAQ, [], []);
  const data: FAQItem[] = rawData.length > 0 ? rawData : fallbackFAQ.map((f, i) => ({ id: i + 1, question: f.question, answer: f.answer }));
  const [openId, setOpenId] = useState<number | null>(null);

  return (
    <section id="faq" className="section-padding bg-white">
      <div className="container-narrow">
        <div ref={ref} className={`reveal ${visible ? 'visible' : ''} text-center max-w-2xl mx-auto mb-16`}>
          <span className="badge bg-accent-50 text-accent-700 border border-accent-200">FAQ</span>
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-navy-900 mt-4 mb-4">
            Часто задаваемые вопросы
          </h2>
          <p className="text-gray-500 text-lg">
            Ответы на самые популярные вопросы о реабилитации и лечении зависимостей.
          </p>
        </div>

        <div className="max-w-3xl mx-auto space-y-3">
          {data.map((item, i) => (
            <div
              key={item.id}
              className={`reveal ${visible ? 'visible' : ''}`}
              style={{ transitionDelay: `${i * 0.1}s` }}
            >
              <FAQAccordion
                item={item}
                open={openId === item.id}
                onToggle={() => setOpenId(openId === item.id ? null : item.id)}
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
