"use client";
import React from "react";
import Navbar from "./Navbar";
import Hero from "./Hero";
import SpecialityCard from "./SpecialityCard";
import USPSection from "./USPSection";
import Gallery from "./Gallery";
import Contact from "./Contact";
import Footer from "./Footer";
import ParallaxScroll from "./ParallaxScroll";
import ChatWidget from "./ChatWidget";
import Services from "./Services";
function Home() {
  return (
    <div className="bg-slate-600">
      <Navbar />
      <Hero />
      <SpecialityCard />
      <ParallaxScroll/>
      <Services/>
      <USPSection />
      <Gallery />
      <Contact />
      <ChatWidget />
      <Footer />
    </div>
  );
}
export default Home;
