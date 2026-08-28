"use client"
import { useState } from "react";
import { Globe, Megaphone, TrendingUp, MessageSquare, Truck } from "lucide-react";

export function Offerings() {
  const [activeTab, setActiveTab] = useState(0);
  
  const offerings = [
    {
      icon: Globe,
      title: "Website",
      description: "Professional e-commerce websites",
      features: [
        "Mobile-responsive design",
        "SEO optimization",
        "Fast loading speed",
        "Secure payment integration",
        "Product catalog management"
      ]
    },
    {
      icon: Megaphone,
      title: "Marketing",
      description: "Digital marketing solutions",
      features: [
        "Social media campaigns",
        "Google Ads management",
        "Email marketing",
        "Content creation",
        "Performance analytics"
      ]
    },
    {
      icon: TrendingUp,
      title: "Conversion",
      description: "Optimize for maximum conversions",
      features: [
        "A/B testing",
        "Funnel optimization",
        "Cart abandonment recovery",
        "Personalization engine",
        "Conversion tracking"
      ]
    },
    {
      icon: MessageSquare,
      title: "WhatsApp",
      description: "WhatsApp Business automation",
      features: [
        "Automated responses",
        "Catalog integration",
        "Order updates",
        "Customer support",
        "Broadcast messages"
      ]
    },
    {
      icon: Truck,
      title: "Shipping",
      description: "Seamless logistics management",
      features: [
        "Multiple courier partners",
        "Real-time tracking",
        "Automated label generation",
        "COD reconciliation",
        "Returns management"
      ]
    }
  ];
  
  return (
    <section id="offerings" className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Offerings</h2>
          <p className="text-xl text-gray-600">Complete solutions for your online business</p>
        </div>
        
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {offerings.map((offering, index) => (
            <button
              key={index}
              onClick={() => setActiveTab(index)}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-all ${
                activeTab === index
                  ? "bg-[#5b4ef9] text-white shadow-lg"
                  : "bg-white text-gray-700 hover:bg-gray-100"
              }`}
            >
              <offering.icon className="w-5 h-5" />
              <span>{offering.title}</span>
            </button>
          ))}
        </div>
        
        <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
          <div className="flex items-start gap-4 mb-6">
           <div className="bg-[#5b4ef9]/10 w-16 h-16 rounded-xl flex items-center justify-center flex-shrink-0">
              {(() => {
                const Icon = offerings[activeTab].icon;
                return <Icon className="w-8 h-8 text-[#5b4ef9]" />;
              })()}
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">{offerings[activeTab].title}</h3>
              <p className="text-gray-600">{offerings[activeTab].description}</p>
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-4">
            {offerings[activeTab].features.map((feature, index) => (
              <div key={index} className="flex items-center gap-3">
               <div className="w-6 h-6 rounded-full bg-[#5b4ef9]/10 flex items-center justify-center flex-shrink-0">
                  <div className="w-2 h-2 rounded-full bg-[#5b4ef9]"></div>
                </div>
                <span className="text-gray-700">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
