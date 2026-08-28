import { Handshake, Package, Target } from "lucide-react";

export function Features() {
  const features = [
    {
      icon: Handshake,
      title: "Win-Win Partnership",
      description: "We only succeed when you succeed. Our pricing model aligns with your growth, ensuring mutual benefit every step of the way."
    },
    {
      icon: Package,
      title: "All-In-One Platform",
      description: "From website creation to shipping logistics, manage your entire business operation from a single, unified dashboard."
    },
    {
      icon: Target,
      title: "Profit-Focused",
      description: "Every feature is designed to maximize your profit margins. We help you reduce costs while increasing revenue."
    }
  ];
  
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Choose KarobarOne?</h2>
          <p className="text-xl text-gray-600">Built for entrepreneurs who want to grow profitably</p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-white border border-gray-200 rounded-2xl p-8 hover:shadow-lg transition-shadow">
              <div className="bg-[#5b4ef9]/10 w-14 h-14 rounded-xl flex items-center justify-center mb-6">
                <feature.icon className="w-7 h-7 text-[#5b4ef9]" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
