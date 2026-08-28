"use client";
import FlipCard from "./FlipCard";
import { toast } from "sonner";

type Product = {
  title: string;
  description: string;
  image: string;
  backContent: string;
  longDescription: string;
};

const products: Product[] = [
  {
    title: "Premium Cloud Solutions",
    description: "Enterprise-grade cloud infrastructure for scalable business operations",
    image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    backContent: "Industry-leading product designed to exceed your expectations with cutting-edge technology and 99.9% uptime guarantee.",
    longDescription: "Our Premium Cloud Solutions provide enterprise-grade infrastructure with advanced security features, automatic scaling, real-time monitoring, and 24/7 technical support. Built on industry-leading platforms, our solutions ensure your business operations run smoothly with maximum reliability and performance."
  },
  {
    title: "Advanced Security Suite",
    description: "Comprehensive security framework protecting your digital assets",
    image: "https://images.unsplash.com/photo-1563986768609-322da13575f3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    backContent: "Bank-level security features ensuring your data and operations remain protected 24/7 with multi-layer encryption.",
    longDescription: "Our Advanced Security Suite combines cutting-edge encryption, threat detection, and compliance management into a comprehensive security framework. With real-time monitoring, automated threat response, and regular security audits, your digital assets remain protected against evolving cyber threats."
  },
  {
    title: "Lightning Performance Engine",
    description: "Ultra-fast processing power for demanding applications",
    image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    backContent: "Optimized performance that delivers results in milliseconds, powered by next-gen architecture.",
    longDescription: "Experience unparalleled speed with our Lightning Performance Engine. Leveraging cutting-edge optimization algorithms and distributed computing, we deliver blazing-fast response times for even the most demanding workloads."
  },
  {
    title: "Global Network Services",
    description: "Worldwide infrastructure for seamless connectivity",
    image: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    backContent: "Worldwide infrastructure ensuring seamless service delivery across all continents with low-latency connections.",
    longDescription: "Our Global Network Services span across 50+ countries with strategically positioned data centers ensuring optimal performance worldwide. Benefit from intelligent traffic routing, automatic failover, and content delivery acceleration."
  },
  {
    title: "Premium Support Package",
    description: "Round-the-clock expert assistance whenever you need it",
    image: "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    backContent: "Round-the-clock expert support team ready to help you succeed at any time, in any timezone.",
    longDescription: "Never face technical challenges alone with our Premium Support Package. Our certified experts are available 24/7/365 via phone, chat, and email. Get priority response times, dedicated account management, and proactive system monitoring."
  },
  {
    title: "Excellence Awards Program",
    description: "Industry-recognized quality and innovation standards",
    image: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?...",
    backContent: "Recognized excellence in innovation and customer satisfaction year after year by leading industry bodies.",
    longDescription: "Join the ranks of award-winning businesses with our Excellence Awards Program. We provide comprehensive quality frameworks, innovation methodologies, and best practices recognized by leading industry organizations."
  }
];

export default function ProductsSection() {
  const handleAddToCart = (productName: string) => {
    toast.success(`${productName} added to cart!`);
  };

  const handleAddToWishlist = (productName: string) => {
    toast.success(`${productName} added to wishlist!`);
  };

  return (
    <section id="products" className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-5xl text-center mb-16">Our Products</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {products.map((product, idx) => (
            <FlipCard
              key={idx}
              {...product}
              onAddToCart={() => handleAddToCart(product.title)}
              onAddToWishlist={() => handleAddToWishlist(product.title)}
            />
          ))}
        </div>
      </div>
    </section>
  );
}