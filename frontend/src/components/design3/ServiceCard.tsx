"use client";
import React, { useState } from "react";

function ServiceCard({ title, img, desc }) {
  const [flipped, setFlipped] = useState(false);

  return (
    <div
      className="group [perspective:1000px]"
      onClick={() => setFlipped(!flipped)}
    >
      <div
        className={`relative h-64 w-full transition-transform duration-700 
        [transform-style:preserve-3d]
        ${flipped ? "[transform:rotateY(180deg)]" : ""}
        md:group-hover:[transform:rotateY(180deg)]`}
      >
        {/* FRONT */}
        <div className="absolute inset-0 backface-hidden rounded-2xl overflow-hidden shadow-md">
          <img src={img} alt={title} className="w-full h-full object-cover" />

          <div className="absolute inset-0 bg-black/30 flex items-end justify-center pb-4">
            <h3 className="text-white text-lg font-semibold">{title}</h3>
          </div>
        </div>

        {/* BACK */}
        <div
          className="absolute inset-0 rounded-2xl 
          bg-gradient-to-br from-white to-gray-100 
          shadow-lg p-6 flex flex-col justify-between text-center
          [transform:rotateY(180deg)] backface-hidden"
        >
          <div className="w-10 h-1 bg-blue-500 mx-auto rounded-full mb-3"></div>

          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              {title}
            </h3>

            <p className="text-sm text-gray-600 leading-relaxed px-2">{desc}</p>
          </div>

          <div className="border-t border-gray-200 my-4"></div>

          <button className="text-sm text-blue-500 font-medium">
            Learn More →
          </button>
        </div>
      </div>
    </div>
  );
}

export default ServiceCard;
