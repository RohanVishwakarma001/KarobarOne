"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight } from "lucide-react";

type Slide = {
  image: string;
  title: string;
  subtitle: string;
};

const slides: Slide[] = [
  {
    image:
      "https://images.unsplash.com/photo-1568740118571-da7e1ee1f545?auto=format&fit=crop&w=1080&q=80",
    title: "Welcome to Excellence",
    subtitle: "Transform your business with our innovative solutions",
  },
  {
    image:
      "https://images.unsplash.com/photo-1651331189447-704ac3643c07?auto=format&fit=crop&w=1080&q=80",
    title: "Innovation Meets Performance",
    subtitle: "Leading the way in modern technology",
  },
  {
    image:
      "https://images.unsplash.com/photo-1697092433137-33f25c1da715?auto=format&fit=crop&w=1080&q=80",
    title: "Your Success Partner",
    subtitle: "Building tomorrow together",
  },
];

export default function HeroCarousel() {
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % slides.length);
    }, 5000);

    return () => clearInterval(timer);
  }, []);

  const prev = () =>
    setCurrent((p) => (p - 1 + slides.length) % slides.length);

  const next = () => setCurrent((p) => (p + 1) % slides.length);

  return (
    <div className="relative h-screen overflow-hidden">

      {/* Slides */}
      <AnimatePresence mode="wait">
        <motion.div
          key={current}
          initial={{ opacity: 0, scale: 1.1 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.7 }}
          className="absolute inset-0"
        >
          <div
            className="absolute inset-0 bg-cover bg-center"
            style={{ backgroundImage: `url(${slides[current].image})` }}
          />

          <div className="absolute inset-0 bg-black/40" />

          <div className="relative h-full flex items-center justify-center text-center text-white px-4">
            <div>
              <h1 className="text-5xl md:text-7xl mb-4">
                {slides[current].title}
              </h1>
              <p className="text-xl md:text-2xl">
                {slides[current].subtitle}
              </p>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Prev Button */}
      <button
        onClick={prev}
        className="absolute left-4 top-1/2 -translate-y-1/2 z-10 bg-white/20 hover:bg-white/30 p-2 rounded-full"
      >
        <ChevronLeft className="text-white" size={32} />
      </button>

      {/* Next Button */}
      <button
        onClick={next}
        className="absolute right-4 top-1/2 -translate-y-1/2 z-10 bg-white/20 hover:bg-white/30 p-2 rounded-full"
      >
        <ChevronRight className="text-white" size={32} />
      </button>

      {/* Dots */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-2 z-10">
        {slides.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrent(idx)}
            className={`h-3 rounded-full transition-all ${
              idx === current ? "w-8 bg-white" : "w-3 bg-white/50"
            }`}
          />
        ))}
      </div>
    </div>
  );
}