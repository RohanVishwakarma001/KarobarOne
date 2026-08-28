"use client";

import { useRef, useState, useEffect } from "react";
import {
  motion,
  useScroll,
  useTransform,
  AnimatePresence,
} from "framer-motion";
import { ArrowRight, TrendingUp, Users, DollarSign, ShoppingCart } from "lucide-react";
import Link from "next/link";

const VANISHING_WORDS = [
  "Smarter",
  "Faster",
  "Globally",
  "With AI",
  "Securely",
  "Effortlessly",
  "Across Every Channel",
  "Without Complexity",
  "Without Developers",
  "With Automations",
];

function VanishingText() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % VANISHING_WORDS.length);
    }, 1800);
    return () => clearInterval(interval);
  }, []);

  return (
    <AnimatePresence mode="wait">
      <motion.span
        key={VANISHING_WORDS[index]}
        initial={{ opacity: 0, filter: "blur(6px)" }}
        animate={{ opacity: 1, filter: "blur(0px)" }}
        exit={{ opacity: 0, filter: "blur(6px)" }}
        transition={{ duration: 0.5, ease: "easeInOut" }}
        className="inline-block font-semibold bg-gradient-to-r from-[#5b4ef9] via-[#8b5cf6] to-[#ec4899] bg-clip-text text-transparent"
      >
        {VANISHING_WORDS[index]}
      </motion.span>
    </AnimatePresence>
  );
}

export function Hero() {
  // This wrapper's height is exactly how much scroll distance the pin
  // effect uses. Because the video is position:sticky (not fixed), it
  // visually fills this entire range the whole time - growing then
  // shrinking - so there is never any empty/dead space, and scrolling
  // up always correctly reverses it (no JS measurement involved at all).
  const pinWrapRef = useRef<HTMLDivElement>(null);

  const { scrollYProgress } = useScroll({
    target: pinWrapRef,
    offset: ["start start", "end end"],
  });

  // grow (0 -> 0.5) then shrink back (0.5 -> 1), video always visible
  const scale = useTransform(scrollYProgress, [0, 0.5, 1], [1, 2.6, 1]);
  const borderRadius = useTransform(scrollYProgress, [0, 0.5, 1], [24, 4, 24]);

  return (
    <section id="home" className="bg-white">
      <div className="max-w-7xl mx-auto px-6 pt-24">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start mb-4">
          {/* Left: text content */}
          <div className="text-left">
            <h1 className="text-4xl md:text-5xl font-bold mb-4 leading-tight text-pink-500">
              The complete Commerce Platform To Build, Sell &amp; Scale
            </h1>

            <div className="text-4xl md:text-5xl font-bold mb-4 leading-tight">
              <VanishingText />
            </div>

            <p className="text-4xl md:text-5xl font-bold mb-4 leading-tight text-[#5b4ef9]">
              For every Passionate &amp; Ambitious Business
            </p>

            <p className="text-base text-gray-500 mb-8 max-w-xl">
              AI-Powered omnichannel commerce platform built in India for ambitious
              business. Launch your store in minutes, sell across marketplaces and
              social channels, automate operations, accept global payments, and scale
              securely - all from a single dashboard.
            </p>

            <Link
              href="/questionaree"
              className="bg-[#5b4ef9] text-white px-8 py-4 rounded-lg hover:bg-[#4a3ee0] transition-colors inline-flex items-center gap-2"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>

          {/* Right: sticky-pinned video. The tall tracker below is
              absolutely positioned, so it never stretches this grid row -
              the row's height is decided by the text column only, keeping
              both columns perfectly top-aligned. */}
          <div className="relative">
            <div ref={pinWrapRef} className="absolute inset-x-0 top-0 h-[160vh]">
              <div className="sticky top-0 flex justify-center md:justify-end">
                <motion.div
                  style={{ scale, borderRadius }}
                  className="w-full max-w-md aspect-video overflow-hidden shadow-2xl relative z-30"
                >
                  <video
                    autoPlay
                    muted
                    loop
                    playsInline
                    className="w-full h-full object-cover"
                    src="/videos/hero-video.mp4"
                  />
                </motion.div>
              </div>
            </div>
            {/* Invisible spacer so this column still reserves the video's
                normal box size for correct alignment at rest */}
            <div className="w-full max-w-md aspect-video invisible" />
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-24">
        <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl p-8 border border-gray-200">
          <div className="bg-gradient-to-br from-[#5b4ef9] to-[#4a3ee0] rounded-xl p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-white text-xl font-semibold">Business Dashboard</h3>
              <div className="bg-white/20 px-3 py-1 rounded-full text-white text-sm">
                Live
              </div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-4 h-4 text-white" />
                  <span className="text-white/80 text-sm">Revenue</span>
                </div>
                <p className="text-white text-2xl font-bold">₹2.4L</p>
                <p className="text-green-300 text-xs">+23% this month</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Users className="w-4 h-4 text-white" />
                  <span className="text-white/80 text-sm">Customers</span>
                </div>
                <p className="text-white text-2xl font-bold">1,234</p>
                <p className="text-green-300 text-xs">+12% this month</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <ShoppingCart className="w-4 h-4 text-white" />
                  <span className="text-white/80 text-sm">Orders</span>
                </div>
                <p className="text-white text-2xl font-bold">456</p>
                <p className="text-green-300 text-xs">+8% this month</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <DollarSign className="w-4 h-4 text-white" />
                  <span className="text-white/80 text-sm">Profit</span>
                </div>
                <p className="text-white text-2xl font-bold">₹48K</p>
                <p className="text-green-300 text-xs">+15% this month</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="h-2 bg-[#5b4ef9] rounded-full mb-2" style={{ width: '75%' }}></div>
              <p className="text-sm text-gray-600">Conversion Rate</p>
              <p className="text-lg font-semibold text-gray-900">3.2%</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="h-2 bg-[#5b4ef9] rounded-full mb-2" style={{ width: '60%' }}></div>
              <p className="text-sm text-gray-600">Avg Order Value</p>
              <p className="text-lg font-semibold text-gray-900">₹1,850</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="h-2 bg-[#5b4ef9] rounded-full mb-2" style={{ width: '90%' }}></div>
              <p className="text-sm text-gray-600">Customer Satisfaction</p>
              <p className="text-lg font-semibold text-gray-900">4.8/5</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}