"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getSession, isAuthenticated, type SessionClaims } from "@/lib/auth/session";

/**
 * Client-side route guard. There's no Next.js middleware for this since the
 * session token lives in localStorage, not a cookie — redirecting has to
 * happen after mount, in the browser.
 */
export function useRequireAuth() {
  const router = useRouter();
  const [session, setSession] = useState<SessionClaims | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace("/login");
      return;
    }
    setSession(getSession());
    setReady(true);
  }, [router]);

  return { session, ready };
}
