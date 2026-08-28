import Header from './Header';
import HeroCarousel from './HeroCarousel';
import SpecialtyCards from './SpecialtyCards';
import ProductsCarousel from './ProductsCarousel';
import AboutSection from './AboutSection';
import Certifications from './Certifications';
import USPSection from './USPSection';
import InstagramFeed from './InstagramFeed';
import ContactSection from './ContactSection';
import ChatWidget from './ChatWidget';
import Footer from './Footer';

export default function App() {
  return (
    <div className="min-h-screen overflow-x-hidden">
      <Header />
      <HeroCarousel />
      <SpecialtyCards />
      <ProductsCarousel />
      <AboutSection />
      <Certifications />
      <USPSection />
      <InstagramFeed />
      <ContactSection />
      <ChatWidget />
      <Footer />
    </div>
  );
}
