import { useEffect, useState } from 'react';
import { Phone, Menu, X, ChevronDown, Heart, MapPin, Clock } from 'lucide-react';
import { settingsValue, type Settings, type MenuNode, getMenu } from '@/api';
import { useApiData } from '@/hooks';
import { PHONE, WHATSAPP, fallbackMenu } from '@/data';

interface Props {
  settings: Settings;
}

export default function Header({ settings }: Props) {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const [mobileExpanded, setMobileExpanded] = useState<Record<string, boolean>>({});

  const { data: menuData } = useApiData(getMenu, [], []);
  const menuItems: MenuNode[] = (menuData as MenuNode[]).length > 0
    ? (menuData as MenuNode[])
    : fallbackMenu.map((m, i) => ({
        id: i + 1,
        title: m.title,
        url: m.url,
        icon: null,
        children: m.children?.map((c, j) => ({
          id: (i + 1) * 100 + j,
          title: c.title,
          url: c.url,
          icon: null,
        })),
      }));

  const siteTitle = settingsValue(settings, 'site_title', 'Новая Сибирь');
  const phone = settingsValue(settings, 'phone', PHONE);
  const phoneLink = `tel:${phone.replace(/[^\d+]/g, '')}`;
  const address = settingsValue(settings, 'address', 'г. Новосибирск, в черте города');
  const workHours = settingsValue(settings, 'work_hours', 'Круглосуточно, 7 дней в неделю');

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 30);
    onScroll();
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const toggleMobileChild = (title: string) => {
    setMobileExpanded((prev) => ({ ...prev, [title]: !prev[title] }));
  };

  return (
    <header className="fixed top-0 inset-x-0 z-50">
      {/* Top bar */}
      <div className={`hidden lg:block bg-navy-900 text-white/80 text-sm transition-all duration-300 ${scrolled ? 'h-0 overflow-hidden opacity-0' : 'h-auto opacity-100'}`}>
        <div className="max-w-7xl mx-auto px-5 sm:px-8 flex items-center justify-between py-2">
          <div className="flex items-center gap-6">
            <span className="flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5 text-brand-400" />
              {address}
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-brand-400" />
              {workHours}
            </span>
          </div>
          <div className="flex items-center gap-4">
            <a href={WHATSAPP} target="_blank" rel="noopener noreferrer" className="hover:text-brand-300 transition-colors">
              WhatsApp
            </a>
            <span className="text-white/30">|</span>
            <span className="text-white font-medium">Анонимно • Конфиденциально</span>
          </div>
        </div>
      </div>

      {/* Main header */}
      <div className={`transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-lg shadow-lg shadow-navy-900/5 border-b border-gray-100' : 'bg-white border-b border-transparent'}`}>
        <div className="max-w-7xl mx-auto px-5 sm:px-8 flex items-center justify-between py-3">
          {/* Logo */}
          <a href="#top" className="flex items-center gap-3 group shrink-0">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-lg shadow-brand-200 group-hover:scale-105 transition-transform">
              <Heart className="w-6 h-6 text-white" strokeWidth={2.5} />
            </div>
            <div className="leading-tight hidden sm:block">
              <div className="font-display font-bold text-navy-800 text-lg tracking-tight">{siteTitle}</div>
              <div className="text-[11px] text-brand-600 font-semibold tracking-wide uppercase">Реабилитационный центр</div>
            </div>
          </a>

          {/* Desktop navigation */}
          <nav className="hidden lg:flex items-center gap-0.5">
            {menuItems.map((item) => (
              <div
                key={item.title}
                className="relative"
                onMouseEnter={() => item.children && setActiveDropdown(item.title)}
                onMouseLeave={() => setActiveDropdown(null)}
              >
                <a
                  href={item.url || `#${item.title.toLowerCase()}`}
                  className={`flex items-center gap-1 px-3.5 py-2 text-sm font-medium rounded-lg transition-colors ${
                    activeDropdown === item.title
                      ? 'text-brand-600 bg-brand-50'
                      : 'text-navy-600 hover:text-brand-600 hover:bg-gray-50'
                  }`}
                >
                  {item.title}
                  {item.children && <ChevronDown className={`w-3.5 h-3.5 transition-transform ${activeDropdown === item.title ? 'rotate-180' : ''}`} />}
                </a>

                {/* Dropdown */}
                {item.children && activeDropdown === item.title && (
                  <div className="absolute top-full left-0 mt-1 w-60 bg-white rounded-2xl shadow-xl border border-gray-100 py-2 animate-slide-down">
                    {item.children.map((child) => (
                      <a
                        key={child.title}
                        href={child.url || '#'}
                        className="block px-5 py-2.5 text-sm text-navy-600 hover:text-brand-600 hover:bg-brand-50/50 transition-colors first:rounded-t-2xl last:rounded-b-2xl"
                      >
                        {child.title}
                      </a>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </nav>

          {/* CTA + Mobile toggle */}
          <div className="flex items-center gap-3">
            <a
              href={phoneLink}
              className="hidden md:inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-500 to-brand-600 text-white font-semibold text-sm shadow-lg shadow-brand-200 hover:shadow-brand-300 hover:scale-105 transition-all"
            >
              <Phone className="w-4 h-4" />
              <span>{phone}</span>
            </a>
            <a href={phoneLink} className="md:hidden inline-flex items-center justify-center w-10 h-10 rounded-xl bg-brand-500 text-white">
              <Phone className="w-5 h-5" />
            </a>
            <button
              onClick={() => setMenuOpen((v) => !v)}
              className="lg:hidden w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center text-navy-700 hover:bg-gray-200 transition-colors"
              aria-label="Меню"
            >
              {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="lg:hidden bg-white border-t border-gray-100 shadow-xl animate-fade-in max-h-[80vh] overflow-y-auto">
          <nav className="max-w-7xl mx-auto px-5 py-4 flex flex-col gap-1">
            {menuItems.map((item) => (
              <div key={item.title}>
                {item.children ? (
                  <>
                    <button
                      onClick={() => toggleMobileChild(item.title)}
                      className="w-full flex items-center justify-between px-4 py-3 text-navy-700 font-medium hover:bg-gray-50 rounded-xl transition-colors"
                    >
                      {item.title}
                      <ChevronDown className={`w-4 h-4 transition-transform ${mobileExpanded[item.title] ? 'rotate-180' : ''}`} />
                    </button>
                    {mobileExpanded[item.title] && (
                      <div className="ml-4 border-l-2 border-brand-100 pl-3 space-y-1 mt-1">
                        {item.children.map((child) => (
                          <a
                            key={child.title}
                            href={child.url || '#'}
                            onClick={() => setMenuOpen(false)}
                            className="block px-4 py-2.5 text-sm text-navy-600 hover:text-brand-600 hover:bg-brand-50/50 rounded-xl transition-colors"
                          >
                            {child.title}
                          </a>
                        ))}
                      </div>
                    )}
                  </>
                ) : (
                  <a
                    href={item.url || '#'}
                    onClick={() => setMenuOpen(false)}
                    className="block px-4 py-3 text-navy-700 font-medium hover:bg-gray-50 rounded-xl transition-colors"
                  >
                    {item.title}
                  </a>
                )}
              </div>
            ))}
            <a
              href={phoneLink}
              className="mt-2 px-4 py-3.5 text-center rounded-xl bg-gradient-to-r from-brand-500 to-brand-600 text-white font-semibold"
            >
              <Phone className="w-4 h-4 inline mr-2" />
              {phone}
            </a>
          </nav>
        </div>
      )}
    </header>
  );
}
