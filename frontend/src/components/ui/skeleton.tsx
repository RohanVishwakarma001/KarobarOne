import { cn } from "./utils";

/**
 * Base pulse (bg-accent + animate-pulse) stays as the reduced-motion-safe
 * fallback — Tailwind's `animate-pulse` already no-ops under
 * `prefers-reduced-motion` via tw-animate-css. The shimmer sweep layers on
 * top and is the one explicitly disabled in globals.css's
 * `@media (prefers-reduced-motion: reduce)` block for `.skeleton-shimmer`.
 * Sizing comes entirely from `className` — this renders nothing but the
 * shimmer chrome, so it never fights the real content's footprint.
 */
function Skeleton({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="skeleton"
      className={cn("bg-accent relative overflow-hidden rounded-md", className)}
      {...props}
    >
      <div className="skeleton-shimmer absolute inset-0" />
    </div>
  );
}

export { Skeleton };
