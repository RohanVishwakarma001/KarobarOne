import { Award, Zap, Shield } from 'lucide-react';

const specialties = [
  {
    icon: Award,
    title: 'Quality Excellence',
    description: 'ISO certified processes ensuring premium quality',
    color: 'from-blue-500 to-cyan-500'
  },
  {
    icon: Zap,
    title: 'Fast Delivery',
    description: 'Quick turnaround times without compromising quality',
    color: 'from-orange-500 to-red-500'
  },
  {
    icon: Shield,
    title: 'Reliable & Secure',
    description: 'Trusted by industry leaders worldwide',
    color: 'from-green-500 to-emerald-500'
  }
];

export default function SpecialtyIcons() {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-4xl md:text-5xl text-center mb-16">
          Our Specialties
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {specialties.map((specialty, index) => {
            const Icon = specialty.icon;
            return (
              <div
                key={index}
                className="group bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:scale-105 cursor-pointer"
              >
                <div className={`w-20 h-20 rounded-full bg-gradient-to-br ${specialty.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-2xl mb-4 group-hover:text-blue-600 transition-colors">
                  {specialty.title}
                </h3>
                <p className="text-gray-600">
                  {specialty.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
