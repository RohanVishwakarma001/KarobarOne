"use client";

import { useEffect } from "react";
import { motion } from "framer-motion";
import { ShieldAlert } from "lucide-react";
import "./globals.css";

/**
 * Last-resort boundary — only renders if the ROOT layout itself throws (a
 * far rarer case than error.tsx's per-segment boundary). Next.js requires
 * this file to render its own complete <html>/<body>, since the root
 * layout — and everything it would have provided (QueryProvider, fonts,
 * Toaster) — is exactly what just crashed and can't be relied on here.
 * Kept deliberately dependency-light for the same reason: fewer things that
 * could also fail while rendering the fallback for a failure.
 */
export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Root layout error boundary caught:", error);
  }, [error]);

  return (
    <html lang="en">
      <body style={{ margin: 0, minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "system-ui, sans-serif" }}>
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ type: "spring", stiffness: 360, damping: 30 }}
          style={{ display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center", maxWidth: 420, padding: "0 16px" }}
        >
          <div
            style={{
              display: "flex",
              height: 64,
              width: 64,
              alignItems: "center",
              justifyContent: "center",
              borderRadius: "9999px",
              backgroundColor: "#fef2f2",
              color: "#ef4444",
            }}
          >
            <ShieldAlert size={32} />
          </div>
          <h1 style={{ marginTop: 24, fontSize: 20, fontWeight: 600, color: "#0f172a" }}>The application hit an unexpected error</h1>
          <p style={{ marginTop: 8, fontSize: 14, color: "#64748b" }}>
            Something went wrong loading KarobarOne. Try reloading — if this keeps happening, please contact support.
          </p>
          {error.digest && <p style={{ marginTop: 8, fontFamily: "monospace", fontSize: 12, color: "#94a3b8" }}>Reference: {error.digest}</p>}

          <button
            onClick={reset}
            style={{
              marginTop: 24,
              borderRadius: 9999,
              backgroundColor: "#5b4ef9",
              color: "#ffffff",
              padding: "10px 24px",
              fontSize: 14,
              fontWeight: 500,
              border: "none",
              cursor: "pointer",
            }}
          >
            Reload
          </button>
        </motion.div>
      </body>
    </html>
  );
}
