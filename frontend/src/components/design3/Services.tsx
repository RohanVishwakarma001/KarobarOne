"use client";
import ServiceCard from "./ServiceCard";
const img1 = "/assets/design3/service/img1.webp";
const img2 = "/assets/design3/service/img2.webp";
const img3 = "/assets/design3/service/img3.webp";
const img4 = "/assets/design3/service/img4.webp";
const img5 = "/assets/design3/service/img5.webp";
const img6 = "/assets/design3/service/img6.webp";
const services = [
  {
    title: "Web Development",
    img: img1,
    desc: "Landing pages, e-commerce, and dashboards built for performance.",
  },
  {
    title: "App Development",
    img: img2,
    desc: "Android, iOS and cross-platform apps with smooth UX.",
  },
  {
    title: "UI/UX Design",
    img: img3,
    desc: "Modern interfaces focused on usability and engagement.",
  },
  {
    title: "Digital Marketing",
    img: img4,
    desc: "SEO, ads and social media strategies that convert.",
  },
  {
    title: "Content Creation",
    img: img5,
    desc: "High-quality content that builds your brand identity.",
  },
  {
    title: "Consulting",
    img: img6,
    desc: "Business and tech strategies to scale your growth.",
  },
];

function Services() {
  return (
    <div id="services" className="bg-gray-900 py-16 px-6">
      <h2 className="text-3xl font-bold text-center text-white mb-12">
        Our Services
      </h2>

      <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {services.map((service, i) => (
          <ServiceCard key={i} {...service} />
        ))}
      </div>
    </div>
  );
}

export default Services;
