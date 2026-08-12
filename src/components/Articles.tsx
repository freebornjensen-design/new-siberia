import { getArticles, type ArticleItem } from '@/api';
import { useApiData, useReveal } from '@/hooks';
import { ArrowRight, CalendarDays, FileText } from 'lucide-react';
import { fallbackArticles } from '@/data';

interface ArticleCard {
  title: string;
  excerpt: string;
  category: string;
  date: string;
  cover: string | null;
}

export default function Articles() {
  const { ref, visible } = useReveal<HTMLDivElement>();
  const { data } = useApiData(getArticles, [], []);

  const articles: ArticleCard[] =
    data.length > 0
      ? data.map((a: ArticleItem) => ({
          title: a.title,
          excerpt: a.excerpt,
          category: 'Статья',
          date: a.date ?? '',
          cover: null,
        }))
      : fallbackArticles.map((a) => ({
          title: a.title,
          excerpt: a.excerpt,
          category: a.category,
          date: a.date,
          cover: a.cover,
        }));

  return (
    <section id="articles" className="section-padding bg-white">
      <div className="container-narrow">
        <div ref={ref} className={`reveal ${visible ? 'visible' : ''} flex flex-col sm:flex-row sm:items-end justify-between gap-6 mb-16`}>
          <div className="max-w-2xl">
            <span className="badge bg-brand-50 text-brand-700 border border-brand-200">Блог</span>
            <h2 className="font-display font-bold text-3xl sm:text-4xl text-navy-900 mt-4 mb-4">
              Полезные статьи
            </h2>
            <p className="text-gray-500 text-lg">
              Информация о зависимостях, процессе реабилитации и поддержке близких. Написано простым языком.
            </p>
          </div>
          <a href="#articles" className="inline-flex items-center gap-2 text-brand-600 hover:text-brand-700 font-medium transition-colors group">
            Все статьи
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </a>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((article, i) => (
            <article
              key={article.title}
              className={`reveal ${visible ? 'visible' : ''} group card-hover overflow-hidden flex flex-col`}
              style={{ transitionDelay: `${i * 0.1}s` }}
            >
              <div className="relative aspect-[16/10] overflow-hidden bg-gray-100">
                {article.cover ? (
                  <img
                    src={article.cover}
                    alt={article.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-navy-50 to-brand-50">
                    <FileText className="w-12 h-12 text-navy-300 group-hover:scale-110 transition-transform duration-700" />
                  </div>
                )}
                <span className="absolute top-4 left-4 badge bg-white/90 text-navy-700 shadow-sm">
                  {article.category}
                </span>
              </div>
              <div className="p-6 flex flex-col flex-1">
                <div className="inline-flex items-center gap-1.5 text-gray-400 text-xs mb-3">
                  <CalendarDays className="w-3.5 h-3.5" />
                  {article.date}
                </div>
                <h3 className="font-display font-bold text-xl text-navy-800 mb-3 leading-tight group-hover:text-brand-600 transition-colors">
                  {article.title}
                </h3>
                <p className="text-gray-500 text-sm leading-relaxed flex-1">{article.excerpt}</p>
                <span className="inline-flex items-center gap-2 mt-5 text-brand-600 font-medium text-sm group-hover:gap-3 transition-all">
                  Читать далее
                  <ArrowRight className="w-4 h-4" />
                </span>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
