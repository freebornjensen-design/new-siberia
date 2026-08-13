import Header from '@/components/Header';
import Hero from '@/components/Hero';
import Services from '@/components/Services';
import Advantages from '@/components/Advantages';
import Specialists from '@/components/Specialists';
import Prices from '@/components/Prices';
import Articles from '@/components/Articles';
import Gallery from '@/components/Gallery';
import Achievements from '@/components/Achievements';
import FAQ from '@/components/FAQ';
import Licenses from '@/components/Licenses';
import Footer from '@/components/Footer';
import SeoManager from '@/components/SeoManager';
import ServiceLanding from '@/components/ServiceLanding';
import { useApiData } from '@/hooks';
import { getSettings, type Settings } from '@/api';

function parseServiceSlug(pathname: string): string | null {
  const match = pathname.match(/^\/services\/([^/]+)\/?$/);
  return match ? decodeURIComponent(match[1]) : null;
}

function App() {
  const { data: settings } = useApiData<Settings>(getSettings, {});
  const serviceSlug = parseServiceSlug(window.location.pathname);

  if (serviceSlug) {
    return (
      <div className="min-h-screen bg-white">
        <SeoManager settings={settings} />
        <ServiceLanding slug={serviceSlug} settings={settings} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <SeoManager settings={settings} />
      <Header settings={settings} />
      <main>
        <Hero />
        <Services />
        <Advantages />
        <Specialists />
        <Prices />
        <Articles />
        <Gallery />
        <Achievements />
        <FAQ />
        <Licenses />
      </main>
      <Footer settings={settings} />
    </div>
  );
}

export default App;
