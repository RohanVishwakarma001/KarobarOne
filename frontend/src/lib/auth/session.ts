"use client";

const ACCESS_TOKEN_KEY = "karobar_access_token";
const REFRESH_TOKEN_KEY = "karobar_refresh_token";

export type SessionClaims = {
  userId: string;
  role: string | null;
  tenantId: string | null;
  exp: number;
};

export function saveSession({ accessToken, refreshToken }: { accessToken: string; refreshToken: string }): void {
  window.localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  window.localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
}

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(ACCESS_TOKEN_KEY);
}

/**
 * Decodes the JWT payload client-side (base64 only, no signature check) purely
 * to drive UI routing decisions (e.g. "does this user have a store yet?").
 * The backend remains the sole authorization boundary — every protected
 * endpoint independently verifies the token's signature and claims.
 */
export function getSession(): SessionClaims | null {
  const token = getAccessToken();
  if (!token) return null;
  try {
    const payloadB64 = token.split(".")[1];
    const payload = JSON.parse(atob(payloadB64.replace(/-/g, "+").replace(/_/g, "/")));
    return {
      userId: payload.sub,
      role: payload.role ?? null,
      tenantId: payload.tenantId ?? null,
      exp: payload.exp,
    };
  } catch {
    return null;
  }
}

export function isAuthenticated(): boolean {
  const session = getSession();
  if (!session) return false;
  return session.exp * 1000 > Date.now();
}

export function clearSession(): void {
  window.localStorage.removeItem(ACCESS_TOKEN_KEY);
  window.localStorage.removeItem(REFRESH_TOKEN_KEY);
}
