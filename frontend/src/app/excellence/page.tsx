import Header from "@/components/excellence/Header";
import HeroCarousel from "@/components/excellence/HeroCarousel";
import Marquee from "@/components/excellence/Marquee";
import ProductsSection from "@/components/excellence/ProductsSection";
import AboutSection from "@/components/excellence/AboutSection";
import USPSection from "@/components/excellence/USPSection";
import InstagramFeed from "@/components/excellence/InstagramFeed";
import ContactSection from "@/components/excellence/ContactSection";
import Footer from "@/components/excellence/Footer";
import BlogSection from "@/components/excellence/BlogSection";
import { Toaster } from "sonner";

export default function ExcellencePage() {
  return (
    <div className="min-h-screen">
      <Toaster position="top-right" richColors />

      <Header />

      <HeroCarousel />

      <Marquee
        text="INNOVATION • EXCELLENCE • RELIABILITY"
        direction="left"
      />

      <ProductsSection />

      <Marquee
        text="TRUSTED BY THOUSANDS • GLOBAL REACH • 24/7 SUPPORT"
        direction="right"
      />

      <AboutSection />

      <USPSection />

      <InstagramFeed />

      <BlogSection />

      <ContactSection />

      <Footer />
    </div>
  );
}
