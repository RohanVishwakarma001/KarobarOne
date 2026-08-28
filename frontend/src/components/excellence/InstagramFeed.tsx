"use client"
import Image from "next/image";
import { motion } from "motion/react";
import { FaInstagram } from "react-icons/fa";

const instagramPosts: string[] = [
  "https://images.unsplash.com/photo-1621184078903-6bfe9482d935?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
  "https://images.unsplash.com/photo-1615494487949-f5f68968330e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
  "https://images.unsplash.com/photo-1644771571408-f2b3b8782f41?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
  "https://images.unsplash.com/photo-1644771571330-f17bfb8908ea?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
  "https://images.unsplash.com/photo-1621184078816-62b9eff99925?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
  "https://images.unsplash.com/photo-1621184078811-1120e2f1fc9e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
];

export default function InstagramFeed(): React.ReactElement {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-center gap-3 mb-16">
          <FaInstagram size={40} className="text-pink-600" />
          <h2 className="text-5xl">Follow Us on Instagram</h2>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {instagramPosts.map((post: string, idx: number) => (
            <motion.div
              key={idx}
              whileHover={{
                scale: 1.05,
                rotate: idx % 2 === 0 ? 2 : -2,
              }}
              className="relative aspect-square overflow-hidden rounded-lg shadow-lg cursor-pointer group"
            >
              <Image
                src={post}
                alt={`Instagram post ${idx + 1}`}
                width={400}
                height={400}
                className="w-full h-full object-cover"
              />

              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end justify-center pb-4">
                <FaInstagram className="text-white" size={32} />
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}