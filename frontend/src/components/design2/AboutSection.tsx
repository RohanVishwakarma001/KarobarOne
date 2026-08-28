"use client";
import { Building2, Users, Target, Calendar } from 'lucide-react';
import { useRef } from 'react';
import { motion, useScroll, useTransform } from 'motion/react';

const aboutItems = [
  {
    icon: Users,
    title: 'Promoter',
    content: 'Founded by industry veterans with over 40 years of combined experience in delivering excellence and innovation to the corporate sector.'
  },
  {
    icon: Building2,
    title: 'Company',
    content: 'A leading provider of corporate solutions with a commitment to quality, integrity, and customer satisfaction across all our operations.'
  },
  {
    icon: Target,
    title: 'Mission & Vision',
    content: 'To be the most trusted partner for businesses worldwide, delivering sustainable value through innovative solutions and exceptional service.'
  },
  {
    icon: Calendar,
    title: 'Inception',
    content: 'Established in 1990, we have grown from a small startup to a global enterprise serving thousands of satisfied clients worldwide.'
  }
];

export default function AboutSection() {
  const sectionRef = useRef(null);

  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start end", "end start"]
  });

  const y1 = useTransform(scrollYProgress, [0, 1], [100, -100]);
  const y2 = useTransform(scrollYProgress, [0, 1], [-100, 100]);
  const opacity = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [0, 1, 1, 0]);
  const scale = useTransform(scrollYProgress, [0, 0.5, 1], [0.8, 1, 0.8]);

  return (
    <section
      id="about"
      ref={sectionRef}
      className="relative py-20 px-4 overflow-hidden w-full"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-gray-50" />

      <motion.div
        className="absolute top-20 -left-20 sm:left-10 w-48 h-48 sm:w-72 sm:h-72 bg-blue-200/30 rounded-full blur-3xl"
        style={{ y: y1 }}
      />
      <motion.div
        className="absolute bottom-20 -right-20 sm:right-10 w-64 h-64 sm:w-96 sm:h-96 bg-purple-200/20 rounded-full blur-3xl"
        style={{ y: y2 }}
      />
      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] sm:w-[600px] sm:h-[600px] bg-gradient-to-br from-blue-100/20 to-transparent rounded-full blur-2xl"
        style={{ scale }}
      />

      <div className="container mx-auto max-w-7xl relative z-10">
        <motion.div className="text-center mb-16" style={{ opacity }}>
          <h2 className="text-3xl sm:text-4xl md:text-5xl mb-4">About Us</h2>
          <p className="text-gray-600 text-base sm:text-lg max-w-3xl mx-auto">
            Decades of excellence in delivering innovative solutions that drive business growth
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
          {aboutItems.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{
                duration: 0.6,
                delay: index * 0.1,
                ease: "easeOut"
              }}
              whileHover={{
                scale: 1.02,
                transition: { duration: 0.2 }
              }}
              className="bg-white p-6 sm:p-8 rounded-xl shadow-lg hover:shadow-2xl transition-shadow"
            >
              <div className="flex items-start gap-4">
                <motion.div
                  className="w-12 h-12 sm:w-14 sm:h-14 bg-blue-600 rounded-lg flex items-center justify-center flex-shrink-0"
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.5 }}
                >
                  <item.icon className="text-white" size={24} />
                </motion.div>

                <div>
                  <h3 className="text-xl sm:text-2xl mb-2 sm:mb-3">
                    {item.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed text-sm sm:text-base">
                    {item.content}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}