"use client";

import { useState } from "react";
import { CheckCircle2 } from "lucide-react";
import Image from "next/image";

export default function BookDemoPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    companySize: "",
    phone: "",
    message: "",
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: connect to your backend / API route
    console.log(formData);
    setSubmitted(true);
  };

  const benefits = [
    "Launch your online store in days, not months",
    "Manage inventory, orders and shipping in one place",
    "Reach customers across web, app and marketplaces",
    "Get insights that help you grow profitably",
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="max-w-7xl mx-auto px-6 py-16 grid md:grid-cols-2 gap-12 items-start">
        {/* Left side */}
        <div>
          <div className="flex items-center gap-3 mb-8">
            <Image
              src="/Logo.jpeg"
              alt="Karobar Logo"
              width={40}
              height={40}
              className="rounded-md object-contain"
            />
            <span className="text-lg font-semibold">KarobarOne</span>
          </div>

          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Let&apos;s Talk About{" "}
            <span className="text-[#5b4ef9]">Your Business</span>
          </h1>
          <p className="text-gray-400 text-lg mb-10 max-w-md">
            Book a free walkthrough with our team. We&apos;ll show you exactly
            how KarobarOne can help you sell more, everywhere.
          </p>

          <ul className="space-y-4">
            {benefits.map((benefit) => (
              <li key={benefit} className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-[#5b4ef9] flex-shrink-0 mt-0.5" />
                <span className="text-gray-300">{benefit}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Right side - Form */}
        <div className="bg-gray-900 rounded-2xl p-8 border border-gray-800">
          {submitted ? (
            <div className="text-center py-16">
              <CheckCircle2 className="w-14 h-14 text-[#5b4ef9] mx-auto mb-4" />
              <h2 className="text-2xl font-semibold mb-2">Thank you!</h2>
              <p className="text-gray-400">
                Our team will reach out to you shortly to schedule your demo.
              </p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm text-gray-300 mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-[#5b4ef9]"
                  placeholder="Your name"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-300 mb-2">
                  Work Email
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-[#5b4ef9]"
                  placeholder="you@company.com"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-300 mb-2">
                    Company Size
                  </label>
                  <select
                    value={formData.companySize}
                    onChange={(e) =>
                      setFormData({ ...formData, companySize: e.target.value })
                    }
                    className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#5b4ef9]"
                  >
                    <option value="">Select</option>
                    <option value="1-10">1–10</option>
                    <option value="11-50">11–50</option>
                    <option value="51-200">51–200</option>
                    <option value="200+">200+</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm text-gray-300 mb-2">
                    Phone
                  </label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) =>
                      setFormData({ ...formData, phone: e.target.value })
                    }
                    className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-[#5b4ef9]"
                    placeholder="+91"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm text-gray-300 mb-2">
                  Message (optional)
                </label>
                <textarea
                  rows={4}
                  value={formData.message}
                  onChange={(e) =>
                    setFormData({ ...formData, message: e.target.value })
                  }
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-[#5b4ef9] resize-none"
                  placeholder="Tell us about your business"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-[#5b4ef9] hover:bg-[#4a3ee0] text-white font-semibold py-3 rounded-lg transition-colors"
              >
                Request Demo
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}