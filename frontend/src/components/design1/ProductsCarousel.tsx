"use client";
import { useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const products = [
  {
    title: 'Product Suite A',
    description: 'Comprehensive solutions for enterprise needs',
    image: 'https://images.unsplash.com/photo-1647427060118-4911c9821b82?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=600',
    price: 'Custom Pricing'
  },
  {
    title: 'Product Suite B',
    description: 'Scalable solutions for growing businesses',
    image: 'https://images.unsplash.com/photo-1717386255773-1e3037c81788?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=600',
    price: 'Starting at $999'
  },
  {
    title: 'Product Suite C',
    description: 'Innovative tools for modern workflows',
    image: 'https://images.unsplash.com/photo-1455165814004-1126a7199f9b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=600',
    price: 'Contact for Quote'
  },
  {
    title: 'Service Package D',
    description: 'Professional consulting and support services',
    image: 'https://images.unsplash.com/photo-1769839271827-e7e287319dd4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=600',
    price: 'Flexible Plans'
  },
  {
    title: 'Service Package E',
    description: 'Dedicated team collaboration solutions',
    image: 'https://images.unsplash.com/photo-1758691737543-09a1b2b715fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=600',
    price: 'From $1,499/mo'
  }
];

export default function ProductsCarousel() {
  const scrollContainerRef = useRef<HTMLDivElement | null>(null);
 const scroll = (direction: 'left' | 'right') => {
    if (scrollContainerRef.current) {
      const scrollAmount = 400;
      scrollContainerRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  return (
    <section className="py-20 px-4 bg-white">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-4xl md:text-5xl text-center mb-4">
          Products & Services
        </h2>
        <p className="text-center text-gray-600 mb-12 text-lg">
          Explore our comprehensive range of solutions
        </p>

        <div className="relative">
          <button
            onClick={() => scroll('left')}
            className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white shadow-lg p-3 rounded-full hover:bg-gray-100 transition-colors -translate-x-1/2"
          >
            <ChevronLeft className="w-6 h-6" />
          </button>

          <div
            ref={scrollContainerRef}
            className="flex gap-6 overflow-x-auto scrollbar-hide scroll-smooth pb-4"
            style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
          >
            {products.map((product, index) => (
              <div
                key={index}
                className="min-w-[350px] bg-gray-50 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2"
              >
                <div className="h-48 overflow-hidden">
                  <img
                    src={product.image}
                    alt={product.title}
                    className="w-full h-full object-cover hover:scale-110 transition-transform duration-500"
                  />
                </div>
                <div className="p-6">
                  <h3 className="text-2xl mb-2">{product.title}</h3>
                  <p className="text-gray-600 mb-4">{product.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-blue-600">{product.price}</span>
                    <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors">
                      Learn More
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => scroll('right')}
            className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white shadow-lg p-3 rounded-full hover:bg-gray-100 transition-colors translate-x-1/2"
          >
            <ChevronRight className="w-6 h-6" />
          </button>
        </div>
      </div>
    </section>
  );
}