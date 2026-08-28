"use client";
import React from "react";

function SpecialityCard() {
  const items = [
    {
      title: "High Quality",
      icon: "⭐",
      desc: "Provides high-quality products and services to ensure customer satisfaction.",
    },
    {
      title: "Fast Delivery",
      icon: "🚚",
      desc: "Guarantees quick and efficient delivery of your orders.",
    },
    {
      title: "Trusted Service",
      icon: "✅",
      desc: "Built on trust and reliability for a seamless customer experience.",
    },
  ];

  return (
    <div className="grid gap-7 md:grid-cols-3 px-10 md:px-40 py-10 bg-[#0f172a] text-center">
      {items.map((item, index) => (
        <div
          key={index}
          className="group bg-[#1e293b] rounded-2xl p-6 shadow-md border border-blue-900/40 hover:shadow-blue-900/30 hover:-translate-y-2 transition-all duration-300 cursor-pointer"
        >
          <div className="flex justify-center items-center w-16 h-16 mx-auto mb-4 rounded-full bg-blue-900/40 text-3xl text-blue-300 group-hover:bg-blue-500 group-hover:text-white transition">
            {item.icon}
          </div>

          <h2 className="text-lg font-semibold text-blue-100 group-hover:text-blue-400 transition">
            {item.title}
          </h2>

          <p className="text-sm text-blue-300/70 mt-2">{item.desc}</p>
        </div>
      ))}
    </div>
  );
}

export default SpecialityCard;
