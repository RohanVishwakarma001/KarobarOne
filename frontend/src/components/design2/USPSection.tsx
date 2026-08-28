import { Check } from 'lucide-react';

const usps = [
  '24/7 Customer Support with dedicated account managers',
  'Industry-leading 99.9% uptime guarantee',
  'Competitive pricing with transparent billing',
  'Customized solutions tailored to your needs',
  'Fast delivery and implementation timelines',
  'Comprehensive training and onboarding support'
];

export default function USPSection() {
  return (
    <section className="py-20 px-4 bg-gradient-to-br from-blue-600 to-blue-800 relative overflow-hidden w-full">
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-0 left-0 w-64 h-64 sm:w-96 sm:h-96 bg-white rounded-full -translate-x-1/2 -translate-y-1/2 animate-pulse" />
        <div className="absolute bottom-0 right-0 w-64 h-64 sm:w-96 sm:h-96 bg-white rounded-full translate-x-1/2 translate-y-1/2 animate-pulse delay-1000" />
      </div>

      <div className="container mx-auto max-w-7xl relative z-10">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl md:text-5xl mb-4 text-white">Why Choose Us</h2>
          <p className="text-blue-100 text-base sm:text-lg max-w-2xl mx-auto">
            Unique value propositions that set us apart from the competition
          </p>
        </div>

        <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
          {usps.map((usp, index) => (
            <div
              key={index}
              className="flex items-start gap-3 sm:gap-4 bg-white/10 backdrop-blur-sm p-4 sm:p-6 rounded-lg hover:bg-white/20 transition-colors"
            >
              <div className="w-7 h-7 sm:w-8 sm:h-8 bg-white rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                <Check className="text-blue-600" size={18} />
              </div>
              <p className="text-white text-base sm:text-lg">{usp}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
