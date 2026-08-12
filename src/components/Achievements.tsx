import { getStatistics, getTestimonials, type StatisticItem, type TestimonialItem } from '@/api';
import { useApiData, useReveal, useCountUp } from '@/hooks';
import { Quote, Star } from 'lucide-react';
import { fallbackAchievements, fallbackTestimonials } from '@/data';

interface Achievement {
  value: number;
  suffix: string;
  label: string;
  raw: string;
}

interface TestimonialCard {
  name: string;
  text: string;
  rating: number;
}

function parseAchievement(value: string, label: string): Achievement {
  const match = value.trim().match(/^(\d+)(.*)$/);
  if (match) return { value: Number(match[1]), suffix: match[2].trim(), label, raw: value };
  return { value: 0, suffix: '', label, raw: value };
}

export default function Achievements() {
  const { ref, visible } = useReveal<HTMLDivElement>();
  const { data: stats } = useApiData(getStatistics, [], []);
  const { data: apiTestimonials } = useApiData(getTestimonials, [], []);

  const achievements: Achievement[] =
    stats.length > 0
      ? stats.map((s: StatisticItem) => parseAchievement(s.value, s.label))
      : fallbackAchievements.map((a) => ({ value: a.value, suffix: a.suffix, label: a.label, raw: `${a.value}${a.suffix}` }));

  const testimonials: TestimonialCard[] =
    apiTestimonials.length > 0
      ? apiTestimonials.map((t: TestimonialItem) => ({ name: t.name, text: t.text, rating: t.rating ?? 5 }))
      : fallbackTestimonials.map((t) => ({ name: t.name, text: t.text, rating: 5 }));

  return (
    <section id="achievements" className="section-padding bg-white">
      <div className="container-narrow">
        <div ref={ref} className={`reveal ${visible ? 'visible' : ''} text-center max-w-2xl mx-auto mb-16`}>
          <span className="badge bg-accent-50 text-accent-700 border border-accent-200">Результаты</span>
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-navy-900 mt-4 mb-4">
            Достижения центра
          </h2>
          <p className="text-gray-500 text-lg">
            Цифры и отзывы, которые говорят о результатах нашей работы лучше любых слов.
          </p>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-20">
          {achievements.map((ach, i) => (
            <AchievementCard key={`${ach.label}-${i}`} achievement={ach} visible={visible} delay={i * 0.1} />
          ))}
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map((t, i) => (
            <div
              key={t.name}
              className={`reveal ${visible ? 'visible' : ''} group card-hover p-7`}
              style={{ transitionDelay: `${0.3 + i * 0.1}s` }}
            >
              <div className="flex gap-0.5 mb-4">
                {Array.from({ length: t.rating }).map((_, j) => (
                  <Star key={j} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                ))}
              </div>
              <Quote className="w-8 h-8 text-brand-200 mb-4" />
              <p className="text-gray-600 leading-relaxed mb-5 italic">«{t.text}»</p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white font-bold text-sm">
                  {t.name.charAt(0)}
                </div>
                <div className="text-navy-800 font-semibold text-sm">{t.name}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function AchievementCard({ achievement, visible, delay }: { achievement: Achievement; visible: boolean; delay: number }) {
  const value = useCountUp(achievement.value, visible);
  return (
    <div
      className={`reveal ${visible ? 'visible' : ''} group card-hover p-6 sm:p-8 text-center`}
      style={{ transitionDelay: `${delay}s` }}
    >
      <div className="font-display font-extrabold text-4xl sm:text-5xl text-gradient mb-2">
        {achievement.raw.trim().match(/^\d/) ? `${value}${achievement.suffix}` : achievement.raw}
      </div>
      <div className="text-gray-500 text-sm leading-snug">{achievement.label}</div>
    </div>
  );
}
