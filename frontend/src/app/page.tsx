import { Navbar } from "../components/Navbar";
import { Hero } from "../components/Hero";
import { SocialProof } from "../components/SocialProof";
import { Features } from "../components/Features";
import { Offerings } from "../components/Offerings";
import { Timeline } from "../components/Timeline";
import { Pricing } from "../components/Pricing";
import { Partnerships } from "../components/Partnerships";
import { Testimonials } from "../components/Testimonials";
import { About } from "../components/About";
import { Footer } from "../components/Footer";
import { StoreOwnerDashboardShowcase } from "@/components/StoreOwnerDashboardShowcase";
import { WebsiteBuilder } from "@/components/WebsiteBuilder";

export default function HomePage() {
  return (
    <div className="bg-white">
      <Navbar />
      <Hero />
      <SocialProof />
      <Features />
      <Offerings />
      <Timeline />
      <Pricing />
      <Partnerships />
      <Testimonials />
      <StoreOwnerDashboardShowcase />
      <WebsiteBuilder />
      <About />
      <Footer />
    </div>
  );
}
