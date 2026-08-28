"use client";
import React, { useState } from "react";

const images = [
  { src: "/assets/design3/gallery/photo-1.jpg", title: "Team Collaboration" },
  { src: "/assets/design3/gallery/photo-2.jpg", title: "Office Meeting" },
  { src: "/assets/design3/gallery/photo-3.jpg", title: "Work Culture" },
  { src: "/assets/design3/gallery/photo-4.jpg", title: "Coding Session" },
  { src: "/assets/design3/gallery/photo-5.jpg", title: "Client Discussion" },
  { src: "/assets/design3/gallery/photo-6.jpg", title: "Team Bonding" },
  { src: "/assets/design3/gallery/photo-7.jpg", title: "Office Party" },
  { src: "/assets/design3/gallery/photo-8.jpg", title: "Workspace Setup" },
  { src: "/assets/design3/gallery/photo-9.jpg", title: "Quick Standup Meeting" },
];

function Gallery() {
  const [selected, setSelected] = useState<{ src: string; title: string } | null>(null);
  return (
    <section id="gallery" className="gallery py-10 px-4 bg-gray-900">
      <h2 className="text-3xl text-white font-bold text-center mb-10">
        Our Work Gallery
      </h2>
      <div className="max-w-6xl mx-auto columns-1 sm:columns-2 md:columns-3 gap-3 space-y-4">
        {images.map((item, i) => (
          <div
            key={i}
            className="relative overflow-hidden rounded-xl cursor-pointer group"
            onClick={() => setSelected(item)}
          >
            <img
              src={item.src}
              alt={item.title}
              className="w-full object-cover rounded-xl transition duration-500 group-hover:scale-110"
            />
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center">
              <p className="text-white text-sm font-medium">{item.title}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
export default Gallery;