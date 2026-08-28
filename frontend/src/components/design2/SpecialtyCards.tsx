import { Award, Globe, TrendingUp } from 'lucide-react';

const specialties = [
  {
    icon: Award,
    title: 'Quality Assurance',
    description: 'ISO certified processes ensuring the highest quality standards in every product we deliver.'
  },
  {
    icon: Globe,
    title: 'Global Reach',
    description: 'Serving clients across 50+ countries with localized support and international expertise.'
  },
  {
    icon: TrendingUp,
    title: 'Innovation First',
    description: 'Cutting-edge solutions powered by research and development that drives industry progress.'
  }
];

export default function SpecialtyCards() {
  return (
    <section className="py-20 px-4 bg-gray-50 overflow-hidden">
      <div className="container mx-auto max-w-7xl">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
          {specialties.map((specialty, index) => (
            <div
              key={index}
              className="bg-white p-6 sm:p-8 rounded-lg shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-2 group"
            >
              <div className="w-14 h-14 sm:w-16 sm:h-16 bg-blue-600 rounded-full flex items-center justify-center mb-4 sm:mb-6 group-hover:bg-blue-700 transition-colors">
                <specialty.icon className="text-white" size={28} />
              </div>
              <h3 className="text-xl sm:text-2xl mb-3 sm:mb-4">{specialty.title}</h3>
              <p className="text-gray-600 text-sm sm:text-base">{specialty.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
