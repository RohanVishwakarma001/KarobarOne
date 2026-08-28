"use client"

import { motion } from "motion/react";

type MarqueeProps = {
  text: string;
  direction?: "left" | "right";
};

export default function Marquee({
  text,
  direction = "left",
}: MarqueeProps): React.ReactElement {
  return (
    <div className="overflow-hidden whitespace-nowrap py-8 bg-gradient-to-r from-blue-600 to-purple-600">
      <motion.div
        className="inline-block"
        animate={{
          x: direction === "left" ? [0, -1000] : [-1000, 0],
        }}
        transition={{
          x: {
            repeat: Infinity,
            repeatType: "loop",
            duration: 20,
            ease: "linear",
          },
        }}
      >
        <span className="text-4xl md:text-6xl text-white mx-8">
          {text} • {text} • {text} • {text} •
        </span>
      </motion.div>
    </div>
  );
}