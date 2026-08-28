"use client";
import Link from "next/link";
import { useState } from "react";

const designs = [
  {
    id: 1,
    name: "Design 1",
    description: "E-commerce style with product carousel",
    image: "/assets/hero-design1.png",
    route: "/design1",
  },
  {
    id: 2,
    name: "Design 2",
    description: "Clean minimal business landing page",
    image: "/assets/hero-design2.png",
    route: "/design2",
  },
  {
    id: 3,
    name: "Design 3",
    description: "Dark modern digital agency",
    image: "/assets/hero-design3.png",
    route: "/design3",
  },
  {
    id: 4,
    name: "Design 4",
    description: "Light professional corporate site",
    image: "/assets/hero-design4.png",
    route: "/design4",
  },
  {
    id: 5,
    name: "Design 5 — Excellence",
    description: "Premium e-commerce with blog & USP",
    image: "/assets/hero-design5.png",
    route: "/excellence",
  },
];

export default function Dashboard() {
  const [selected, setSelected] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-gray-950 text-white px-6 py-16">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-3">Choose Your Design</h1>
          <p className="text-gray-400 text-lg">Click on any design to preview it</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {designs.map((design) => (
            <div
              key={design.id}
              onClick={() => setSelected(design.id)}
              className="cursor-pointer rounded-2xl overflow-hidden border border-white/10 hover:border-white/30 transition-all duration-300 hover:scale-105 bg-gray-900"
            >
              <img
                src={design.image}
                alt={design.name}
                className="w-full h-48 object-cover object-top"
              />
              <div className="p-4">
                <h2 className="text-lg font-semibold">{design.name}</h2>
                <p className="text-gray-400 text-sm mt-1">{design.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Modal */}
      {selected !== null && (
        <div
          className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-6"
          onClick={() => setSelected(null)}
        >
          <div
            className="bg-gray-900 rounded-2xl overflow-hidden max-w-2xl w-full border border-white/10"
            onClick={(e) => e.stopPropagation()}
          >
            {(() => {
              const d = designs.find((x) => x.id === selected)!;
              return (
                <>
                  <img src={d.image} alt={d.name} className="w-full h-64 object-cover object-top" />
                  <div className="p-6">
                    <h2 className="text-2xl font-bold mb-2">{d.name}</h2>
                    <p className="text-gray-400 mb-6">{d.description}</p>
                    <div className="flex gap-3">
                      <Link
                        href={d.route}
                        className="flex-1 text-center bg-white text-gray-900 font-semibold py-3 rounded-xl hover:bg-gray-100 transition"
                      >
                        Open Design →
                      </Link>
                      <button
                        onClick={() => setSelected(null)}
                        className="px-6 py-3 rounded-xl border border-white/20 hover:bg-white/10 transition"
                      >
                        Close
                      </button>
                    </div>
                  </div>
                </>
              );
            })()}
          </div>
        </div>
      )}
    </div>
  );
}