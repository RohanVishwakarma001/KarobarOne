"use client";

import Image from "next/image";
import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

type Section = {
  title: string;
  content: string;
  image: string;
};

const aboutSections: Section[] = [
  {
    title: "Promoter",
    content:
      "Founded by visionary leaders with decades of industry experience, our company is built on a foundation of innovation and excellence.",
    image:
      "https://images.unsplash.com/photo-1600880292089-90a7e086ee0c"
  },
  {
    title: "Company",
    content:
      "A leading force in the industry, we pride ourselves on delivering exceptional value through cutting-edge solutions and unwavering commitment to quality.",
    image:
      "https://images.unsplash.com/photo-1522071820081-009f0129c71c"
  },
  {
    title: "Mission & Vision",
    content:
      "To empower businesses worldwide with innovative solutions while maintaining sustainable growth and creating lasting value for all stakeholders.",
    image:
      "https://images.unsplash.com/photo-1622675363311-3e1904dc1885"
  },
  {
    title: "Inception",
    content:
      "Established in 2010, we have grown from a small startup to an industry leader serving clients across 50+ countries.",
    image:
      "https://images.unsplash.com/photo-1758691737246-95bf8f09a997"
  },
  {
    title: "Certifications",
    content:
      "ISO 9001:2015, ISO 27001:2013, and multiple industry-specific certifications validate our commitment to excellence and security.",
    image:
      "https://images.unsplash.com/photo-1666790676906-0295230c121d"
  },
  {
    title: "Statutory",
    content:
      "Fully compliant with all national and international regulations, ensuring transparent and ethical business practices at every level.",
    image:
      "https://images.unsplash.com/photo-1758630737900-a28682c5aa69"
  }
];

type Props = {
  section: Section;
  index: number;
};

function ParallaxCard({ section, index }: Props) {
  const ref = useRef<HTMLDivElement | null>(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);
  const opacity = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [0, 1, 1, 0]);

  return (
    <motion.div
      ref={ref}
      style={{ y, opacity }}
      className={`flex flex-col ${
        index % 2 === 0 ? "md:flex-row" : "md:flex-row-reverse"
      } gap-8 items-center mb-20`}
    >
      <div className="w-full md:w-1/2">
        <Image
          src={section.image}
          alt={section.title}
          width={800}
          height={320}
          className="rounded-2xl shadow-2xl w-full h-80 object-cover"
        />
      </div>

      <div className="w-full md:w-1/2 px-4">
        <h3 className="text-4xl mb-4">{section.title}</h3>
        <p className="text-xl text-gray-600 leading-relaxed">
          {section.content}
        </p>
      </div>
    </motion.div>
  );
}

export default function AboutSection() {
  return (
    <section id="about" className="py-20 px-4 bg-white overflow-hidden">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-5xl text-center mb-20">About Us</h2>

        {aboutSections.map((section, idx) => (
          <ParallaxCard key={idx} section={section} index={idx} />
        ))}
      </div>
    </section>
  );
}