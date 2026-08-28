"use client";

import React from "react";

import { TypeAnimation } from "react-type-animation";
import { motion } from "framer-motion";

function HeroSection() {
  return (
    <div id="home" className="relative w-full h-screen overflow-hidden">
      <video
        className="absolute w-full h-full object-cover"
        muted
        autoPlay
        loop
        playsInline
        preload="auto"
      >
        <source src="/hero_video.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      <div className="absolute inset-0 bg-black/50 backdrop-blur-[2px]" />
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-center px-4">
        <motion.h1
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-white text-3xl md:text-6xl font-extrabold leading-tight"
        >
          <span className="block">We Don't Just Build</span>
          <span className="text-blue-500 drop-shadow-[0_0_1px_rgba(59,130,246,0.7)]">
            <TypeAnimation
              sequence={[
                "Websites",
                2000,
                "Experiences",
                2000,
                "Digital Brands",
                2000,
              ]}
              speed={60}
              repeat={Infinity}
            />
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="text-gray-300 mt-4 max-w-xl text-sm md:text-lg"
        >
          We craft high-performance websites with modern UI, smooth animations,
          and real business impact.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="flex gap-4 mt-6"
        >
          <a href="#contact">
            <button className="px-6 py-3 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600 hover:scale-105 transition">
              Get Started
            </button>
          </a>

          <a href="#services">
            <button className="px-6 py-3 border border-blue-400 text-blue-400 rounded-full hover:bg-blue-500 hover:text-white transition">
              View Work
            </button>
          </a>
        </motion.div>
      </div>
    </div>
  );
}

export default HeroSection;
