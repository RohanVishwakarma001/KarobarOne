"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Compass, Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import { springs, useReducedMotion } from "@/lib/motion";

export default function NotFound() {
  const reducedMotion = useReducedMotion();

  return (
    <div className="flex min-h-[70vh] items-center justify-center px-4 py-16">
      <motion.div
        initial={reducedMotion ? { opacity: 0 } : { opacity: 0, y: 16, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={reducedMotion ? { duration: 0.15 } : springs.gentle}
        className="flex max-w-md flex-col items-center text-center"
      >
        <motion.div
          animate={reducedMotion ? {} : { y: [0, -6, 0] }}
          transition={{ duration: 2.2, repeat: Infinity, ease: "easeInOut" }}
          className="flex h-16 w-16 items-center justify-center rounded-full bg-[#5b4ef9]/10 text-[#5b4ef9]"
        >
          <Compass className="h-8 w-8" />
        </motion.div>

        <p className="mt-6 text-5xl font-bold tracking-tight text-slate-900">404</p>
        <h1 className="mt-2 text-xl font-semibold text-slate-900">Page not found</h1>
        <p className="mt-2 text-sm text-slate-500">
          The page you're looking for doesn't exist or may have moved.
        </p>

        <Link href="/" className="mt-6">
          <Button className="gap-2 bg-[#5b4ef9] hover:bg-[#4a3ee0]">
            <Home className="h-4 w-4" />
            Go home
          </Button>
        </Link>
      </motion.div>
    </div>
  );
}
