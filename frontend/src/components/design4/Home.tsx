import React from "react";
import Navbar from "./Navbar";
import HeroSection from "./HeroSection";
import About from "./About";
import USP from "./USP";
import Contact from "./Contact";
import Footer from "./Footer";
import SpecialitySection from "./SpecialitySection";
import ChatWidget from "./ChatWidget";
import ServicesSection from "./ServicesSection";
function Home() {
  return (
    <div>
      <Navbar />
      <HeroSection />
      <SpecialitySection/>
      <ServicesSection/>
      <About />
      <USP />
      <Contact />
      <ChatWidget />
      <Footer />
    </div>
  );
}
export default Home;
