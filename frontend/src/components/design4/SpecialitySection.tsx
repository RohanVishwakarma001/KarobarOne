"use client";

import React from "react";
import { FaCheckCircle, FaUsers, FaRupeeSign } from "react-icons/fa";

const cards = [
  {
    icon: FaCheckCircle,
    title: "Quality Assurance",
    desc: "We ensure reliable and high-performance solutions with strict standards.",
  },
  {
    icon: FaUsers,
    title: "Client Focused",
    desc: "We build solutions based on real user needs and business goals.",
  },
  {
    icon: FaRupeeSign,
    title: "Affordable Pricing",
    desc: "Get premium quality services at cost-effective pricing.",
  },
];

function SpecialitySection() {
  return (
    <div className="bg-gradient-to-b from-[#f9fafb] to-[#eef2ff] py-10 px-6">
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
        Our Specialities
      </h2>
      <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {cards.map((card, index) => {
          const Icon = card.icon;
          return (
            <div
              key={index}
              className="group bg-white p-8 rounded-2xl shadow-md text-center
              transition-all duration-500 hover:shadow-xl hover:-translate-y-2
              animate-float"
            >
              <div className="flex justify-center mb-4">
                <Icon className="text-4xl text-blue-500 group-hover:scale-110 transition duration-300" />
              </div>

              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {card.title}
              </h3>

              <p className="text-gray-600 text-sm">{card.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default SpecialitySection;