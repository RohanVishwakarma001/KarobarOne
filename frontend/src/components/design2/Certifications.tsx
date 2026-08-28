import { Shield, Award, CheckCircle, Star } from 'lucide-react';

const certifications = [
  { icon: Shield, name: 'ISO 9001:2015', description: 'Quality Management' },
  { icon: Award, name: 'ISO 14001:2015', description: 'Environmental Management' },
  { icon: CheckCircle, name: 'OHSAS 18001', description: 'Health & Safety' },
  { icon: Star, name: 'CE Certification', description: 'European Standards' }
];

export default function Certifications() {
  return (
    <section id="certifications" className="relative py-20 sm:py-32 px-4 overflow-hidden w-full">
      <div
        className="absolute inset-0 bg-cover bg-center bg-fixed"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1700727448686-b314cb5f9948?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1920&q=80)'
        }}
      >
        <div className="absolute inset-0 bg-blue-900/85" />
      </div>

      <div className="container mx-auto max-w-7xl relative z-10">
        <div className="text-center mb-12 sm:mb-16">
          <h2 className="text-3xl sm:text-4xl md:text-5xl mb-4 text-white">Statutory Certifications</h2>
          <p className="text-blue-100 text-base sm:text-lg max-w-2xl mx-auto">
            Certified excellence backed by international standards
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
          {certifications.map((cert, index) => (
            <div
              key={index}
              className="bg-white/95 backdrop-blur-sm p-6 sm:p-8 rounded-xl text-center hover:bg-white hover:scale-105 transition-all duration-300 shadow-xl"
            >
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 sm:mb-6">
                <cert.icon className="text-white" size={32} />
              </div>
              <h3 className="text-lg sm:text-xl mb-2">{cert.name}</h3>
              <p className="text-gray-600 text-sm sm:text-base">{cert.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
