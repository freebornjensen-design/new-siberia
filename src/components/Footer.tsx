import { useState, type FormEvent } from 'react';
import { Phone, MapPin, Clock, Send, CheckCircle2, MessageCircle, Loader2, Heart } from 'lucide-react';
import { settingsValue, type Settings } from '@/api';
import { PHONE, WHATSAPP } from '@/data';

interface Props {
  settings: Settings;
}

export default function Footer({ settings }: Props) {
  const [status, setStatus] = useState<'idle' | 'sending' | 'sent' | 'error'>('idle');
  const [name, setName] = useState('');
  const [phoneInput, setPhoneInput] = useState('');
  const [consent, setConsent] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const siteTitle = settingsValue(settings, 'site_title', 'Новая Сибирь');
  const phone = settingsValue(settings, 'phone', PHONE);
  const address = settingsValue(settings, 'address', 'г. Новосибирск, в черте города');
  const workHours = settingsValue(settings, 'work_hours', 'Круглосуточно, 7 дней в неделю');
  const phoneLink = `tel:${phone.replace(/[^\d+]/g, '')}`;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!consent) { setErrorMsg('Необходимо согласие на обработку персональных данных'); setStatus('error'); return; }
    setStatus('sending'); setErrorMsg('');
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, phone: phoneInput, consent: true }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) { setErrorMsg(data.error || 'Не удалось отправить заявку.'); setStatus('error'); return; }
      setStatus('sent'); setName(''); setPhoneInput(''); setConsent(false);
      setTimeout(() => setStatus('idle'), 6000);
    } catch { setErrorMsg('Сетевая ошибка.'); setStatus('error'); }
  };

  return (
    <footer id="contacts" className="relative bg-navy-900 text-white">
      <div className="container-narrow py-20 sm:py-28">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20">
          <div>
            <span className="text-brand-400 font-semibold text-sm tracking-widest uppercase">Контакты</span>
            <h2 className="font-display font-bold text-3xl sm:text-4xl text-white mt-3 mb-4">
              Свяжитесь с нами
            </h2>
            <p className="text-navy-200 text-lg mb-8 max-w-md">
              Если вам или вашему близкому нужна помощь — позвоните нам. Консультация бесплатная и анонимная. Мы работаем круглосуточно.
            </p>

            <div className="space-y-4">
              <a href={phoneLink} className="flex items-center gap-4 group">
                <div className="w-12 h-12 rounded-2xl bg-brand-500/15 border border-brand-500/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Phone className="w-5 h-5 text-brand-400" />
                </div>
                <div><div className="text-navy-300 text-xs uppercase tracking-wide">Телефон</div><div className="text-white font-semibold text-lg group-hover:text-brand-300 transition-colors">{phone}</div></div>
              </a>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-brand-500/15 border border-brand-500/20 flex items-center justify-center"><MapPin className="w-5 h-5 text-brand-400" /></div>
                <div><div className="text-navy-300 text-xs uppercase tracking-wide">Адрес</div><div className="text-white font-semibold">{address}</div></div>
              </div>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-brand-500/15 border border-brand-500/20 flex items-center justify-center"><Clock className="w-5 h-5 text-brand-400" /></div>
                <div><div className="text-navy-300 text-xs uppercase tracking-wide">Часы работы</div><div className="text-white font-semibold">{workHours}</div></div>
              </div>
            </div>

            <a href={WHATSAPP} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 mt-8 px-5 py-3 rounded-xl bg-brand-500/15 border border-brand-500/20 text-brand-300 font-medium hover:bg-brand-500/25 transition-colors">
              <MessageCircle className="w-4 h-4" /> Написать в WhatsApp
            </a>
          </div>

          <div className="bg-navy-800/50 rounded-3xl p-6 sm:p-8 border border-navy-700/50">
            <h3 className="font-display font-bold text-2xl text-white mb-2">Запросить звонок</h3>
            <p className="text-navy-300 text-sm mb-6">Оставьте контакты — мы перезвоним в течение 15 минут.</p>
            {status === 'sent' ? (
              <div className="flex flex-col items-center justify-center py-12 text-center animate-fade-in">
                <CheckCircle2 className="w-16 h-16 text-brand-400 mb-4" />
                <h4 className="font-display font-bold text-xl text-white mb-2">Заявка отправлена!</h4>
                <p className="text-navy-300">Мы свяжемся с вами в ближайшее время.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="name" className="block text-navy-300 text-sm mb-2">Ваше имя</label>
                  <input id="name" type="text" required value={name} onChange={(e) => setName(e.target.value)} placeholder="Как к вам обращаться" className="w-full px-4 py-3.5 rounded-xl bg-navy-950/50 border border-navy-700 text-white placeholder-navy-500 focus:border-brand-500/50 focus:outline-none focus:ring-1 focus:ring-brand-500/30 transition-colors" />
                </div>
                <div>
                  <label htmlFor="phone" className="block text-navy-300 text-sm mb-2">Телефон</label>
                  <input id="phone" type="tel" required value={phoneInput} onChange={(e) => setPhoneInput(e.target.value)} placeholder="+7 (___) ___-__-__" className="w-full px-4 py-3.5 rounded-xl bg-navy-950/50 border border-navy-700 text-white placeholder-navy-500 focus:border-brand-500/50 focus:outline-none focus:ring-1 focus:ring-brand-500/30 transition-colors" />
                </div>
                <label className="flex items-start gap-2.5 text-navy-400 text-xs cursor-pointer select-none">
                  <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} className="mt-0.5 w-4 h-4 rounded bg-navy-950/50 border border-navy-600 accent-brand-500" />
                  <span>Я даю согласие на обработку персональных данных в соответствии с политикой конфиденциальности.</span>
                </label>
                {status === 'error' && <p className="text-red-400 text-sm">{errorMsg}</p>}
                <button type="submit" disabled={status === 'sending'} className="w-full inline-flex items-center justify-center gap-2 px-6 py-4 rounded-xl bg-gradient-to-r from-brand-500 to-brand-600 text-white font-semibold shadow-lg shadow-brand-500/20 hover:shadow-brand-500/30 hover:scale-[1.02] transition-all disabled:opacity-60 disabled:hover:scale-100">
                  {status === 'sending' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                  {status === 'sending' ? 'Отправка…' : 'Отправить заявку'}
                </button>
              </form>
            )}
          </div>
        </div>

        <div className="mt-16 pt-8 border-t border-navy-700/50 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center">
              <Heart className="w-4 h-4 text-white" />
            </div>
            <div className="text-navy-400 text-sm">© {new Date().getFullYear()} Реабилитационный центр «{siteTitle}». Все права защищены.</div>
          </div>
          <div className="text-navy-500 text-xs">Помощь доступна 24/7. Анонимно. Конфиденциально.</div>
        </div>
      </div>
    </footer>
  );
}
