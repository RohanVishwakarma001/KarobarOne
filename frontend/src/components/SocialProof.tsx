export function SocialProof() {
  const brands = [
    "Amazon", "Flipkart", "Myntra", "Shopify", "WooCommerce",
    "Razorpay", "Shiprocket", "Delhivery", "PayU", "Instamojo"
  ];
  
  return (
    <section className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-6">
        <h3 className="text-center text-gray-600 mb-8">Trusted by 10,000+ businesses across India</h3>
        <div className="relative overflow-hidden">
          <div className="flex animate-marquee whitespace-nowrap">
            {[...brands, ...brands].map((brand, index) => (
              <div 
                key={index} 
                className="inline-flex items-center justify-center px-8 mx-4 text-2xl font-semibold text-gray-400"
              >
                {brand}
              </div>
            ))}
          </div>
        </div>
      </div>
      <style>{`
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-marquee {
          animation: marquee 30s linear infinite;
        }
      `}</style>
    </section>
  );
}
