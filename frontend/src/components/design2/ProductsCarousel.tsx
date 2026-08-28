"use client";
import { useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const products = [
  {
    image: 'https://images.unsplash.com/photo-1768145488772-db787036bb13?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=800&q=80',
    title: 'Premium Products',
    category: 'Retail Solutions'
  },
  {
    image: 'https://images.unsplash.com/photo-1762330464415-e971f55ae0b8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=800&q=80',
    title: 'Digital Services',
    category: 'Technology'
  },
  {
    image: 'https://images.unsplash.com/photo-1759134155377-4207d89b39ec?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=800&q=80',
    title: 'Professional Services',
    category: 'Consulting'
  },
  {
    image: 'https://images.unsplash.com/photo-1761934657948-708146148588?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=800&q=80',
    title: 'Quality Materials',
    category: 'Manufacturing'
  },
  {
    image: 'https://images.unsplash.com/photo-1776728017050-69b5de52c100?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=800&q=80',
    title: 'Artisan Crafts',
    category: 'Specialty Goods'
  }
];

export default function ProductsCarousel() {
  const scrollRef = useRef(null);

  const scroll = (direction) => {
    if (scrollRef.current) {
      const scrollAmount = 400;
      scrollRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  return (
    <section id="products" className="py-20 px-4 bg-white overflow-hidden">
      <div className="container mx-auto">
        
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl mb-4">Our Products & Services</h2>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Comprehensive solutions tailored to meet your business needs
          </p>
        </div>

        <div className="relative">
          
          {/* Left Button */}
          <button
            onClick={() => scroll('left')}
            className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white shadow-lg p-3 rounded-full hover:bg-gray-100 transition-colors"
          >
            <ChevronLeft size={24} />
          </button>

          {/* Carousel */}
          <div
            ref={scrollRef}
            className="flex gap-6 overflow-x-auto scroll-smooth px-12"
            style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
          >
            {products.map((product, index) => (
              <div
                key={index}
                className="flex-shrink-0 w-80 bg-white rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition-shadow"
              >
                <div className="h-64 overflow-hidden">
                  <img
                    src={product.image}
                    alt={product.title}
                    className="w-full h-full object-cover hover:scale-110 transition-transform duration-500"
                  />
                </div>

                <div className="p-6">
                  <p className="text-blue-600 text-sm mb-2">{product.category}</p>
                  <h3 className="text-xl">{product.title}</h3>
                </div>
              </div>
            ))}
          </div>

          {/* Right Button */}
          <button
            onClick={() => scroll('right')}
            className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white shadow-lg p-3 rounded-full hover:bg-gray-100 transition-colors"
          >
            <ChevronRight size={24} />
          </button>

        </div>
      </div>
    </section>
  );
}