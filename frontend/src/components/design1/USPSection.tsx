"use client";
import { CheckCircle2 } from 'lucide-react';

const usps = [
  {
    title: 'Industry-Leading Quality',
    description: 'Our products undergo rigorous testing and quality control, ensuring 99.9% reliability and performance.'
  },
  {
    title: 'Faster Time-to-Market',
    description: 'Advanced automation and streamlined processes reduce delivery time by 40% compared to competitors.'
  },
  {
    title: 'Cost-Effective Solutions',
    description: 'Premium quality at competitive prices, with flexible payment plans and volume discounts available.'
  },
  {
    title: '24/7 Expert Support',
    description: 'Dedicated support team available round-the-clock to ensure your operations run smoothly.'
  },
  {
    title: 'Sustainable Practices',
    description: 'Eco-friendly manufacturing with carbon-neutral operations and 100% recyclable materials.'
  },
  {
    title: 'Proven Track Record',
    description: '500+ satisfied clients, 98% customer retention rate, and industry-leading satisfaction scores.'
  }
];

export default function USPSection() {
  return (
    <section className="relative py-20 px-4 bg-gradient-to-br from-blue-900 via-purple-900 to-blue-900 text-white overflow-hidden">
      <div className="relative z-10 max-w-7xl mx-auto">
        <h2 className="text-4xl md:text-5xl text-center mb-4">
          Why Choose Us?
        </h2>
        <p className="text-center text-blue-200 mb-16 text-lg">
          The competitive advantages that set us apart
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {usps.map((usp, index) => (
            <div
              key={index}
              className="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/20 hover:bg-white/20 transition-all duration-300 hover:scale-105"
            >
              <CheckCircle2 className="w-10 h-10 text-green-400 mb-4" />
              <h3 className="text-xl mb-3">{usp.title}</h3>
              <p className="text-blue-100 leading-relaxed">{usp.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}