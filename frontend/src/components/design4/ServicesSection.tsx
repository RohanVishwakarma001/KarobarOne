"use client";

import ServiceCard from "./ServiceCard";
const img1 = "/assets/design4/service/img1.webp";
const img2 = "/assets/design4/service/img2.webp";
const img3 = "/assets/design4/service/img3.webp";
const img4 = "/assets/design4/service/img4.webp";
const img5 = "/assets/design4/service/img5.webp";
const img6 = "/assets/design4/service/img6.webp";
const img7 = "/assets/design4/service/img7.webp";
const img8 = "/assets/design4/service/img8.webp";
const img9 = "/assets/design4/service/img9.webp";
const img10 = "/assets/design4/service/img10.webp";
const img11 = "/assets/design4/service/img11.webp";
const img12 = "/assets/design4/service/img12.webp";
const img13 = "/assets/design4/service/img13.webp";
const img14 = "/assets/design4/service/img14.webp";

function ServicesSection() {
  const services = [
    {
      slides: [
        { img: img1, text: "Landing Pages" },
        { img: img7, text: "E-commerce Sites" },
        { img: img8, text: "Admin Dashboards" },
      ],
    },
    {
      slides: [
        { img: img2, text: "Android Apps" },
        { img: img3, text: "iOS Apps" },
        { img: img4, text: "Cross Platform" },
      ],
    },
    {
      slides: [
        { img: img10, text: "Wireframing" },
        { img: img4, text: "Prototyping" },
        { img: img5, text: "User Testing" },
      ],
    },
    {
      slides: [
        { img: img9, text: "SEO" },
        { img: img11, text: "Social Media" },
        { img: img6, text: "Ads Campaign" },
      ],
    },
    {
      slides: [
        { img: img5, text: "Blog Writing" },
        { img: img13, text: "Copywriting" },
        { img: img12, text: "Brand Content" },
      ],
    },
    {
      slides: [
        { img: img14, text: "Business Strategy" },
        { img: img1, text: "Tech Advice" },
        { img: img2, text: "Growth Planning" },
      ],
    },
  ];

  return (
    <div id="services" className="bg-gradient-to-t from-[#f9fafb] to-[#eef2ff] py-16 px-6">
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
        Our Services
      </h2>
      <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {services.map((service, i) => (
          <ServiceCard key={i} slides={service.slides} delay={i * 400} />
        ))}
      </div>
    </div>
  );
}

export default ServicesSection;
