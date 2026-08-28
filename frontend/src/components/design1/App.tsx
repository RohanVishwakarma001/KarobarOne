import Navigation from './Navigation';
import HeroCarousel from './HeroCarousel';
import SpecialtyIcons from './SpecialtyIcons';
import ProductsCarousel from './ProductsCarousel';
import AboutSection from './AboutSection';
import USPSection from './USPSection';
import InstagramFeed from './InstagramFeed';
import ContactSection from './ContactSection';
import Footer from './Footer';
import ScrollToTop from './ScrollToTop';
import ChatWidget from "./ChatWidget";
import Marquee from './Marquee';

export default function App() {
  return (
    <div className="w-full">
      <Navigation />
      <div id="home"><HeroCarousel /></div>
      <div id="marquee"><Marquee /></div>
      <div id="specialties"><SpecialtyIcons /></div>
      <div id="products"><ProductsCarousel /></div>
      <div id="about"><AboutSection /></div>
      <div id="usp"><USPSection /></div>
      <div id="instagram"><InstagramFeed /></div>
      <div id="contact"><ContactSection /></div>
      <ChatWidget />
      <Footer />
      <ScrollToTop />
    </div>
  );
}
