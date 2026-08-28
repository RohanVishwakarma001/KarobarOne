"use client";

import { useEffect, useRef } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";

interface GlassModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export default function GlassModal({
  isOpen,
  onClose,
  title,
  children,
}: GlassModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  // Close on Escape key
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "hidden"; // lock scroll behind modal
    }
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [isOpen, onClose]);

  // Close on outside click
  function handleBackdropClick(e: React.MouseEvent<HTMLDivElement>) {
    if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
      onClose();
    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          onMouseDown={handleBackdropClick}
        >
          {/* Backdrop - no blur, just dark overlay so page behind stays sharp */}
          <div className="absolute inset-0 bg-black/30" />

          {/* Glass modal box */}
          <motion.div
            ref={modalRef}
            role="dialog"
            aria-modal="true"
            aria-labelledby={title ? "glass-modal-title" : undefined}
            className="relative w-full max-w-md rounded-2xl border border-white/20
                       bg-white/10 p-6 shadow-2xl backdrop-blur-xl
                       backdrop-saturate-150"
            initial={{ opacity: 0, scale: 0.92, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.92, y: 20 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
          >
            {/* Close button */}
            <button
              onClick={onClose}
              aria-label="Close modal"
              className="absolute right-4 top-4 rounded-full p-1.5 text-white/70
                         transition hover:bg-white/10 hover:text-white
                         focus:outline-none focus:ring-2 focus:ring-white/40"
            >
              <X size={18} />
            </button>

            {title && (
              <h2
                id="glass-modal-title"
                className="mb-4 pr-8 text-lg font-semibold text-white"
              >
                {title}
              </h2>
            )}

            <div className="text-white/90">{children}</div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}