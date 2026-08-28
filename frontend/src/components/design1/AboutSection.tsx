"use client";
import { useEffect, useRef, useState } from 'react';
import { Building2, Target, Lightbulb, Calendar, Award, FileCheck } from 'lucide-react';

export default function AboutSection() {
  const [scrollY, setScrollY] = useState(0);
 const sectionRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const handleScroll = () => {
      if (sectionRef.current) {
        const rect = sectionRef.current.getBoundingClientRect();
        const scrollProgress = Math.max(0, Math.min(1, 1 - rect.top / window.innerHeight));
        setScrollY(scrollProgress);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const sections = [
    {
      icon: Building2,
      title: 'The Promoter',
      content: 'Founded by industry veterans with 25+ years of combined experience, our leadership brings deep expertise and vision to every project.'
    },
    {
      icon: Target,
      title: 'Our Company',
      content: 'A leading provider of innovative solutions, serving 500+ clients across 30 countries with cutting-edge technology and exceptional service.'
    },
    {
      icon: Lightbulb,
      title: 'Mission & Vision',
      content: 'Mission: To deliver excellence through innovation. Vision: To be the global standard for quality and reliability in our industry.'
    },
    {
      icon: Calendar,
      title: 'Our Inception',
      content: 'Established in 2015, we have grown from a startup to an industry leader through dedication, innovation, and customer-first approach.'
    },
    {
      icon: Award,
      title: 'Certifications',
      content: 'ISO 9001:2015, ISO 14001:2015, ISO 45001:2018 certified. Recognized for excellence in quality management and sustainability.'
    },
    {
      icon: FileCheck,
      title: 'Statutory Certifications',
      content: 'Fully compliant with all regulatory requirements. Licensed and certified by relevant authorities in all operating jurisdictions.'
    }
  ];

  return (
    <section ref={sectionRef} className="relative py-20 px-4 bg-gray-900 text-white overflow-hidden">
      <div
        className="absolute inset-0 bg-cover bg-center bg-fixed opacity-20"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1634547487344-c3aa2e1aacdf?q=80&w=1080)',
          transform: `translateY(${scrollY * 50}px)`
        }}
      />

      <div className="relative z-10 max-w-7xl mx-auto">
        <h2 className="text-4xl md:text-5xl text-center mb-4">
          About Us
        </h2>
        <p className="text-center text-gray-300 mb-16 text-lg">
          Building excellence since 2015
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {sections.map((section, index) => {
            const Icon = section.icon;
            return (
              <div
                key={index}
                className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20 hover:bg-white/20 transition-all duration-300"
                style={{
                  transform: `translateY(${Math.max(0, 50 - scrollY * 100)}px)`,
                  opacity: Math.min(1, scrollY * 2)
                }}
              >
                <Icon className="w-12 h-12 text-blue-400 mb-4" />
                <h3 className="text-2xl mb-3">{section.title}</h3>
                <p className="text-gray-300 leading-relaxed">{section.content}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}