"use client";
import { useEffect, useRef } from "react";

export default function MouseTracker({ children }) {
  const cursorRef = useRef<HTMLDivElement | null>(null);
 const glowRef = useRef<HTMLDivElement | null>(null);

  const pos = useRef({ x: 0, y: 0 });
  const target = useRef({ x: 0, y: 0 });
  const magneticItems = useRef<HTMLElement[]>([]);

  const isTouchDevice = () =>
    "ontouchstart" in window || navigator.maxTouchPoints > 0;

  useEffect(() => {
    if (isTouchDevice()) return;
    magneticItems.current = Array.from(
      document.querySelectorAll(".magnetic")
    );

    let frame: number;

    const animate = () => {
      frame = requestAnimationFrame(animate);
      pos.current.x += (target.current.x - pos.current.x) * 0.15;
      pos.current.y += (target.current.y - pos.current.y) * 0.15;

      const x = pos.current.x;
      const y = pos.current.y;

      // Move cursor
      if (cursorRef.current) {
        cursorRef.current.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      }

      if (glowRef.current) {
        glowRef.current.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      }

      // Magnetic effect
      magneticItems.current.forEach((el) => {
        if (!el) return;

        const rect = el.getBoundingClientRect();
        const elX = rect.left + rect.width / 2;
        const elY = rect.top + rect.height / 2;

        const dx = target.current.x - elX;
        const dy = target.current.y - elY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        const maxDistance = 140;

        if (distance < maxDistance) {
          const strength = (maxDistance - distance) / maxDistance;

          el.style.transform = `translate3d(${dx * 0.3 * strength}px, ${
            dy * 0.3 * strength
          }px, 0) scale(${1 + strength * 0.1})`;
        } else {
          el.style.transform = "translate3d(0,0,0) scale(1)";
        }
      });
    };

    frame = requestAnimationFrame(animate);

    const move = (e: MouseEvent) => {
      target.current.x = e.clientX;
      target.current.y = e.clientY;
    };

    window.addEventListener("mousemove", move);

    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("mousemove", move);
    };
  }, []);

  if (typeof window !== "undefined" && isTouchDevice()) {
    return <>{children}</>;
  }

  return (
    <>
      {children}

      {/* Glow */}
      <div
        ref={glowRef}
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: 60,
          height: 60,
          borderRadius: "50%",
          background: "rgba(127,119,221,0.15)",
          filter: "blur(20px)",
          transform: "translate3d(-50%, -50%, 0)",
          pointerEvents: "none",
          zIndex: 9998,
          willChange: "transform",
        }}
      />

      {/* Cursor */}
      <div
        ref={cursorRef}
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: 28,
          height: 28,
          borderRadius: "50%",
          border: "1.5px solid rgba(255,255,255,0.6)",
          backdropFilter: "blur(6px)",
          WebkitBackdropFilter: "blur(6px)",
          mixBlendMode: "difference",
          transform: "translate3d(-50%, -50%, 0)",
          pointerEvents: "none",
          zIndex: 9999,
          willChange: "transform",
        }}
      />
    </>
  );
}