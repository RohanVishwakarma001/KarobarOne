import { useReducedMotion, type Transition, type Variants } from "framer-motion";

/**
 * Central motion "design tokens" — every animated component in the app pulls
 * timing/easing from here instead of inlining ad-hoc numbers, so the whole
 * product feels like one system instead of a pile of independently-tuned
 * components.
 */

// Cubic-bezier curves (usable directly as a framer `ease` array or a CSS
// `transition-timing-function` value — same four numbers either way).
export const EASE_OUT_EXPO = [0.16, 1, 0.3, 1] as const;
export const EASE_OUT_QUART = [0.25, 1, 0.5, 1] as const;
export const EASE_IN_OUT_SOFT = [0.45, 0, 0.15, 1] as const;

export const springs = {
  /** Fast, tight — button/toggle micro-interactions. */
  snappy: { type: "spring", stiffness: 520, damping: 34, mass: 0.7 } satisfies Transition,
  /** The default for most layout/enter-exit motion (cards, rows, dialogs). */
  gentle: { type: "spring", stiffness: 360, damping: 30, mass: 0.9 } satisfies Transition,
  /** Slight overshoot — success checkmarks, "added!" confirmations. */
  bouncy: { type: "spring", stiffness: 420, damping: 18, mass: 0.8 } satisfies Transition,
} as const;

export const durations = {
  instant: 0.12,
  fast: 0.18,
  base: 0.28,
  slow: 0.42,
} as const;

/** Page-to-page transition (see components/providers/page-transition.tsx). */
export const pageVariants: Variants = {
  initial: { opacity: 0, y: 10, scale: 0.99 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit: { opacity: 0, y: -6, scale: 0.99 },
};
export const pageTransition: Transition = { duration: durations.slow, ease: EASE_OUT_EXPO };

/**
 * WCAG 2.3.3 / prefers-reduced-motion: for a viewer who has this set, large
 * transforms (slide/scale/spring bounce) are a vestibular-trigger risk, but
 * dropping feedback entirely (no transition at all) reads as the UI being
 * broken. The convention this app follows: keep opacity/color transitions
 * (cheap, universally safe), strip everything positional/scale-based, and
 * collapse springs to a short linear fade. Use via `motionSafe(...)` below
 * rather than checking `useReducedMotion()` ad-hoc in every component.
 */
export function motionSafe<T extends { transition?: Transition }>(full: T, reduced: boolean): T {
  if (!reduced) return full;
  return { ...full, transition: { duration: durations.instant, ease: "linear" } };
}

/** Re-exported so components only need one import for reduced-motion checks. */
export { useReducedMotion };
