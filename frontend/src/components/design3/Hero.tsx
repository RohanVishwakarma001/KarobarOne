"use client";
import React from "react";
import { TypeAnimation } from "react-type-animation";
const heroImage = "/assets/design3/hero_image.jpg";
function Hero() {
  return (
    <section id="home" className="relative h-screen overflow-hidden">
      <img
        className="w-full h-full object-cover object-[70%_20%]"
        src={heroImage}
        alt="hero"  
      />

      <div className="absolute inset-0 bg-black/50 flex items-center">
        <div className="px-8 md:px-16">
          <p className="text-blue-400 uppercase tracking-[4px] text-sm md:text-base">
            Modern Digital Agency
          </p>

          <h1 className="text-white text-4xl md:text-7xl font-extrabold leading-tight">
            We Build Business
            <br />
            <span className="text-blue-400 inline-block min-h-[80px] md:min-h-[120px]">
              <TypeAnimation
                sequence={[
                  "Websites",
                  1500,
                  "Brands",
                  1500,
                  "Experiences",
                  1500,
                  "Growth",
                  1500,
                ]}
                speed={30}
                repeat={Infinity}
                cursor={true}
              />
            </span>
          </h1>
        </div>
      </div>
    </section>
  );
}

export default Hero;
