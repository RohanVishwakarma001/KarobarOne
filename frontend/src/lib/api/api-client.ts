import { CORE_API_BASE_URL } from "./config";
import { clearSession, getAccessToken, getRefreshToken, getSession, updateAccessToken } from "@/lib/auth/session";

// ============================================================================
// Errors
// ============================================================================

export class ApiError extends Error {
  status: number;
  code?: string;
  details?: unknown;

  constructor(message: string, status: number, code?: string, details?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

/** One entry of FastAPI/Pydantic's 422 `detail` array: `{loc, msg, type}`. */
export type PydanticValidationErrorItem = {
  loc: (string | number)[];
  msg: string;
  type: string;
};

function isPydanticValidationErrorItem(value: unknown): value is PydanticValidationErrorItem {
  if (!value || typeof value !== "object") return false;
  const v = value as Record<string, unknown>;
  return Array.isArray(v.loc) && typeof v.msg === "string" && typeof v.type === "string";
}

/**
 * Turns a Pydantic 422 `detail`/`error.details` array into one readable
 * string: "email: field required; password: ensure this value has at least
 * 8 characters". `loc` is field-path-shaped, e.g. ["body", "email"] — the
 * leading "body"/"query"/"path" is dropped since it's implementation detail,
 * not something a form should show next to a field label.
 */
export function flattenValidationErrors(items: PydanticValidationErrorItem[]): string {
  return items
    .map((item) => {
      const field = item.loc.filter((seg) => seg !== "body" && seg !== "query" && seg !== "path").join(".");
      const message = item.msg.replace(/^Value error, /, "");
      return field ? `${field}: ${message}` : message;
    })
    .join("; ");
}

type ParsedErrorBody = { message: string; code?: string; details?: unknown };

/**
 * Handles every shape this backend (and plain FastAPI defaults) can return:
 *   1. {"success": false, "error": {"code", "message", "details"?}}  — this
 *      app's AppException/validation handlers (app/core/exceptions.py)
 *   2. {"detail": "..."}                                              — a
 *      raw FastAPI HTTPException (e.g. auth.py's refresh endpoint)
 *   3. {"detail": [{"loc", "msg", "type"}, ...]}                      — the
 *      framework's own default 422 body, in case a route ever bypasses the
 *      custom validation handler
 */
async function parseErrorBody(res: Response): Promise<ParsedErrorBody> {
  let body: unknown;
  try {
    body = await res.json();
  } catch {
    return { message: res.statusText || `Request failed (${res.status})` };
  }

  if (!body || typeof body !== "object") {
    return { message: res.statusText || `Request failed (${res.status})` };
  }
  const b = body as Record<string, unknown>;

  if (b.error && typeof b.error === "object") {
    const e = b.error as Record<string, unknown>;
    let message = typeof e.message === "string" ? e.message : "Request failed";
    if (Array.isArray(e.details) && e.details.every(isPydanticValidationErrorItem)) {
      message = flattenValidationErrors(e.details);
    }
    return { message, code: typeof e.code === "string" ? e.code : undefined, details: e.details ?? e };
  }

  if (typeof b.detail === "string") {
    return { message: b.detail };
  }

  if (Array.isArray(b.detail) && b.detail.every(isPydanticValidationErrorItem)) {
    return { message: flattenValidationErrors(b.detail), code: "VALIDATION_ERROR", details: b.detail };
  }

  if (b.detail && typeof b.detail === "object") {
    const d = b.detail as Record<string, unknown>;
    const message = typeof d.message === "string" ? d.message : JSON.stringify(d);
    return { message, code: typeof d.code === "string" ? d.code : undefined, details: d };
  }

  return { message: res.statusText || `Request failed (${res.status})` };
}

// ============================================================================
// 401 refresh — mutex-style: concurrent 401s share one in-flight refresh
// ============================================================================

let refreshPromise: Promise<string> | null = null;

async function performRefresh(): Promise<string> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    throw new ApiError("Not signed in", 401, "NO_REFRESH_TOKEN");
  }

  const res = await fetch(`${CORE_API_BASE_URL}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refreshToken }),
  });

  if (!res.ok) {
    const { message, code } = await parseErrorBody(res);
    throw new ApiError(message, res.status, code ?? "REFRESH_FAILED");
  }

  const data = (await res.json()) as { accessToken: string };
  updateAccessToken(data.accessToken);
  return data.accessToken;
}

/**
 * Ensures only one /auth/refresh call is ever in flight — every 401 that
 * lands while a refresh is already running just awaits the same promise
 * instead of firing its own request. `refreshPromise` is cleared in
 * `finally` so the *next* 401 (after this one settles) starts a fresh cycle.
 */
function refreshAccessTokenOnce(): Promise<string> {
  if (!refreshPromise) {
    refreshPromise = performRefresh().finally(() => {
      refreshPromise = null;
    });
  }
  return refreshPromise;
}

// ============================================================================
// Request core
// ============================================================================

export type RequestOptions = {
  /** Attach `Authorization: Bearer <token>` and participate in 401 refresh. Default true. */
  auth?: boolean;
  /** Attach `X-Tenant-ID` from the current session. Default true. Ignored if `headers` already sets it. */
  tenant?: boolean;
  headers?: Record<string, string>;
};

async function request<T>(path: string, init: RequestInit, options: RequestOptions = {}, _isRetry = false): Promise<T> {
  const { auth = true, tenant = true, headers: extraHeaders } = options;

  const headers: Record<string, string> = { "Content-Type": "application/json", ...extraHeaders };

  if (auth) {
    const token = getAccessToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }
  if (tenant && !headers["X-Tenant-ID"]) {
    const session = getSession();
    if (session?.tenantId) headers["X-Tenant-ID"] = session.tenantId;
  }

  let res: Response;
  try {
    res = await fetch(`${CORE_API_BASE_URL}${path}`, { ...init, headers });
  } catch {
    throw new ApiError("Could not reach the server. Check your connection and try again.", 0);
  }

  if (res.status === 401 && auth && !_isRetry) {
    try {
      await refreshAccessTokenOnce();
    } catch {
      clearSession();
      if (typeof window !== "undefined") window.location.href = "/login";
      throw new ApiError("Your session has expired — please log in again.", 401, "SESSION_EXPIRED");
    }
    return request<T>(path, init, options, true);
  }

  if (!res.ok) {
    const { message, code, details } = await parseErrorBody(res);
    throw new ApiError(message, res.status, code, details);
  }

  if (res.status === 204) return undefined as T;
  const text = await res.text();
  return text ? (JSON.parse(text) as T) : (undefined as T);
}

// ============================================================================
// Public API
// ============================================================================

export const apiGet = <T>(path: string, options?: RequestOptions) => request<T>(path, { method: "GET" }, options);

export const apiPost = <T>(path: string, body?: unknown, options?: RequestOptions) =>
  request<T>(path, { method: "POST", body: body !== undefined ? JSON.stringify(body) : undefined }, options);

export const apiPatch = <T>(path: string, body?: unknown, options?: RequestOptions) =>
  request<T>(path, { method: "PATCH", body: body !== undefined ? JSON.stringify(body) : undefined }, options);

export const apiPut = <T>(path: string, body?: unknown, options?: RequestOptions) =>
  request<T>(path, { method: "PUT", body: body !== undefined ? JSON.stringify(body) : undefined }, options);

export const apiDelete = <T>(path: string, options?: RequestOptions) =>
  request<T>(path, { method: "DELETE" }, options);

/** Explicit per-call tenant override (e.g. a platform-admin screen acting on a tenant other than the caller's own). */
export const withTenant = (tenantId: string): Record<string, string> => ({ "X-Tenant-ID": tenantId });
