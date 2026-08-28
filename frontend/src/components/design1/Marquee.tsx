export default function Marquee() {
  const highlights = [
    '500+ Satisfied Clients',
    '30+ Countries Worldwide',
    'ISO 9001:2015 Certified',
    '24/7 Expert Support',
    '99.9% Reliability',
    'Award-Winning Quality',
    'Carbon-Neutral Operations',
    '98% Customer Retention'
  ];

  return (
    <div className="bg-blue-600 text-white py-4 overflow-hidden">
      <div className="animate-marquee whitespace-nowrap">
        <div className="inline-flex items-center gap-12 px-6">
          {[...highlights, ...highlights].map((highlight, index) => (
            <div key={index} className="inline-flex items-center gap-3">
              <span className="text-lg md:text-xl">{highlight}</span>
              <span className="text-blue-300">•</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
