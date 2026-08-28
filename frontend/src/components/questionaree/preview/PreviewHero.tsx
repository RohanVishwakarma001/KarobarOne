"use client";

import { useQuestionnaire } from "@/context/questionnaire-context";
import { ArrowRight, Phone } from "lucide-react";

export function PreviewHero() {
  const { data } = useQuestionnaire();

  return (
    <section className="relative overflow-hidden bg-gradient-to-r from-indigo-600 via-blue-600 to-cyan-600 text-white">

      {/* Background Effect */}

      <div className="absolute inset-0 opacity-10">
        <div className="absolute -top-16 -left-16 h-60 w-60 rounded-full bg-white blur-3xl" />
        <div className="absolute bottom-0 right-0 h-72 w-72 rounded-full bg-white blur-3xl" />
      </div>

      <div className="relative px-8 py-16">

        <div className="inline-flex rounded-full bg-white/15 px-4 py-2 text-sm backdrop-blur">

          {data.businessNature
            ? data.businessNature.toUpperCase()
            : "BUSINESS WEBSITE"}

        </div>

        <h1 className="mt-6 text-4xl font-bold leading-tight">

          {data.businessName ? (
            data.businessName
          ) : (
            <span className="text-white/70">
              Your Business Name
            </span>
          )}

        </h1>

        <p className="mt-5 max-w-xl text-lg text-white/90 leading-8">

          {data.brandTagline ? (
            data.brandTagline
          ) : (
            <span className="text-white/60">
              Your business tagline will appear here.
            </span>
          )}

        </p>

        <div className="mt-10 flex gap-4">

          <button className="flex items-center gap-2 rounded-xl bg-white px-6 py-3 font-semibold text-blue-700 shadow">

            Contact Us

            <ArrowRight size={18} />

          </button>

          <button className="flex items-center gap-2 rounded-xl border border-white/40 px-6 py-3 backdrop-blur">

            <Phone size={18} />

            {data.phoneNumber || "+91 XXXXX XXXXX"}

          </button>

        </div>

      </div>

    </section>
  );
}