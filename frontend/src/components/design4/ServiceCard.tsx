"use client";

import React, { useEffect, useState } from "react";

function ServiceCard({ slides, delay = 0 }: any) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const start = setTimeout(() => {
      const interval = setInterval(() => {
        setIndex((prev) => (prev + 1) % slides.length);
      }, 2500);

      return () => clearInterval(interval);
    }, delay);

    return () => clearTimeout(start);
  }, [slides.length, delay]);

  return (
    <div
      className="bg-white rounded-2xl shadow-md overflow-hidden 
      hover:shadow-xl hover:-translate-y-2 transition duration-300"
    >
      {/* Image carousel */}
      <div className="overflow-hidden h-48">
        <div
          className="flex transition-transform duration-700 ease-in-out h-full"
          style={{
            transform: `translateX(-${index * 100}%)`,
          }}
        >
          {slides.map((slide: any, i: any) => (
            <img
              key={i}
              src={slide.img}
              alt=""
              className="min-w-full h-48 object-cover"
            />
          ))}
        </div>
      </div>

      <div className="text-center mt-3 mb-1 px-4">
        <p
          key={index}
          className="text-gray-800 font-medium transition-opacity duration-300"
        >
          {slides[index].text}
        </p>
      </div>

      {/* Dots */}
      <div className="flex justify-center gap-2 py-3">
        {slides.map((_: any, i: any) => (
          <span
            key={i}
            className={`h-1.5 w-1.5 rounded-full ${
              i === index ? "bg-blue-500" : "bg-gray-300"
            }`}
          />
        ))}
      </div>
    </div>
  );
}

export default ServiceCard;