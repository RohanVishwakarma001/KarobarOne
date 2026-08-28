"use client";
import { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const images = [
  'https://images.unsplash.com/photo-1674981208693-de5a9c4c4f44?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBidXNpbmVzcyUyMG9mZmljZSUyMGJ1aWxkaW5nfGVufDF8fHx8MTc3Njg0NTAwMHww&ixlib=rb-4.1.0&q=80&w=1080',
  'https://images.unsplash.com/photo-1662318682624-89652a1c8206?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwyfHxtb2Rlcm4lMjBidXNpbmVzcyUyMG9mZmljZSUyMGJ1aWxkaW5nfGVufDF8fHx8MTc3Njg0NTAwMHww&ixlib=rb-4.1.0&q=80&w=1080',
  'https://images.unsplash.com/photo-1716827172024-f63110d8e0f2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwzfHxtb2Rlcm4lMjBidXNpbmVzcyUyMG9mZmljZSUyMGJ1aWxkaW5nfGVufDF8fHx8MTc3Njg0NTAwMHww&ixlib=rb-4.1.0&q=80&w=1080',
  'https://images.unsplash.com/photo-1772309748311-94587cae2b37?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHw0fHxtb2Rlcm4lMjBidXNpbmVzcyUyMG9mZmljZSUyMGJ1aWxkaW5nfGVufDF8fHx8MTc3Njg0NTAwMHww&ixlib=rb-4.1.0&q=80&w=1080',
];

export default function HeroCarousel() {
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % images.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % images.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + images.length) % images.length);
  };

  return (
    <div className="relative w-full min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 pt-32 pb-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left: Image Carousel */}
          <div className="relative w-full h-[500px] lg:h-[600px] overflow-hidden rounded-2xl shadow-2xl">
            {images.map((image, index) => (
              <div
                key={index}
                className={`absolute inset-0 transition-all duration-1000 ease-in-out ${
                  index === currentSlide ? 'opacity-100 scale-100' : 'opacity-0 scale-110'
                }`}
              >
                <img
                  src={image}
                  alt={`Slide ${index + 1}`}
                  className="w-full h-full object-cover"
                />
              </div>
            ))}

            <button
              onClick={prevSlide}
              className="absolute left-4 top-1/2 -translate-y-1/2 z-10 bg-white/30 hover:bg-white/50 p-3 rounded-full transition-colors backdrop-blur-sm"
            >
              <ChevronLeft className="w-6 h-6 text-white" />
            </button>
            <button
              onClick={nextSlide}
              className="absolute right-4 top-1/2 -translate-y-1/2 z-10 bg-white/30 hover:bg-white/50 p-3 rounded-full transition-colors backdrop-blur-sm"
            >
              <ChevronRight className="w-6 h-6 text-white" />
            </button>

            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-10 flex gap-2">
              {images.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentSlide(index)}
                  className={`h-2 rounded-full transition-all ${
                    index === currentSlide ? 'bg-white w-8' : 'bg-white/50 w-2'
                  }`}
                />
              ))}
            </div>
          </div>

          {/* Right: Headline + CTA */}
          <div className="space-y-8">
            <h1 className="text-5xl md:text-6xl lg:text-7xl text-gray-900 leading-tight">
              Excellence in Every Solution
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 leading-relaxed">
              Delivering innovative products and services that drive success for businesses worldwide
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg transition-colors shadow-lg hover:shadow-xl">
                Discover More
              </button>
              <button className="border-2 border-gray-300 hover:border-blue-600 text-gray-900 px-8 py-4 rounded-lg transition-colors hover:bg-gray-50">
                Contact Us
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
