"use client";

import { useEffect, useRef } from "react";
import {
  TrendingUp,
  Users,
  Target,
  Sparkles
} from "lucide-react";

type USP = {
  icon: React.ReactNode;
  title: string;
  desc: string;
};

export default function USPSection() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = 600;

    type Particle = {
      x: number;
      y: number;
      vx: number;
      vy: number;
      size: number;
    };

    const particles: Particle[] = [];

    for (let i = 0; i < 100; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 3 + 1
      });
    }

    function animate() {
      if (!ctx || !canvas) return;

      ctx.fillStyle = "rgba(15, 23, 42, 0.1)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      particles.forEach((particle, i) => {
        particle.x += particle.vx;
        particle.y += particle.vy;

        if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;

        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(59, 130, 246, ${0.5 + Math.random() * 0.5})`;
        ctx.fill();

        particles.forEach((otherParticle, j) => {
          if (i === j) return;

          const dx = particle.x - otherParticle.x;
          const dy = particle.y - otherParticle.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 100) {
            ctx.beginPath();
            ctx.moveTo(particle.x, particle.y);
            ctx.lineTo(otherParticle.x, otherParticle.y);
            ctx.strokeStyle = `rgba(147, 51, 234, ${
              0.2 * (1 - distance / 100)
            })`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        });
      });

      requestAnimationFrame(animate);
    }

    animate();

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = 600;
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const usps: USP[] = [
    { icon: <TrendingUp size={48} />, title: "Growth Focused", desc: "300% ROI" },
    { icon: <Users size={48} />, title: "Client First", desc: "10K+ clients" },
    { icon: <Target size={48} />, title: "Precision Delivery", desc: "99.9% on-time" },
    { icon: <Sparkles size={48} />, title: "Innovation", desc: "Award-winning" }
  ];

  return (
    <section id="usp" className="relative py-20 px-4 overflow-hidden">
      <canvas
        ref={canvasRef}
        className="absolute inset-0 bg-slate-900"
      />

      <div className="relative z-10 max-w-7xl mx-auto">
        <h2 className="text-5xl text-center mb-16 text-white">
          Why Choose Us
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {usps.map((usp, idx) => (
            <div
              key={idx}
              className="bg-white/10 backdrop-blur-md rounded-xl p-8 text-center text-white"
            >
              <div className="flex justify-center mb-4 text-blue-400">
                {usp.icon}
              </div>
              <h3 className="text-2xl mb-2">{usp.title}</h3>
              <p className="text-gray-300">{usp.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}