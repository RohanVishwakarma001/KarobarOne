import { CORE_API_BASE_URL } from "./config";
import { getAccessToken } from "@/lib/auth/session";

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

/**
 * Same three-shape error body parsing as lib/api/client.ts (see backend
 * README §API consistency): {error:{code,message}}, {detail:"..."} and {detail:{...}}.
 */
async function parseErrorBody(res: Response): Promise<{ message: string; code?: string; details?: unknown }> {
  let body: unknown;
  try {
    body = await res.json();
  } catch {
    return { message: res.statusText || `Request failed (${res.status})` };
  }

  if (body && typeof body === "object") {
    const b = body as Record<string, unknown>;

    if (b.error && typeof b.error === "object") {
      const e = b.error as Record<string, unknown>;
      let message = typeof e.message === "string" ? e.message : "Request failed";
      if (e.code === "VALIDATION_ERROR" && Array.isArray(e.details)) {
        const fieldMessages = (e.details as Array<{ msg?: string }>)
          .map((d) => d.msg?.replace(/^Value error, /, ""))
          .filter(Boolean);
        if (fieldMessages.length) message = fieldMessages.join(" ");
      }
      return {
        message,
        code: typeof e.code === "string" ? e.code : undefined,
        details: e,
      };
    }

    if (typeof b.detail === "string") {
      return { message: b.detail };
    }

    if (b.detail && typeof b.detail === "object") {
      const d = b.detail as Record<string, unknown>;
      const message = typeof d.message === "string" ? d.message : JSON.stringify(d);
      return { message, code: typeof d.code === "string" ? d.code : undefined, details: d };
    }
  }

  return { message: res.statusText || `Request failed (${res.status})` };
}

export async function coreRequest<T>(path: string, options: RequestInit = {}, auth = true): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json", ...(options.headers as Record<string, string>) };
  if (auth) {
    const token = getAccessToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  let res: Response;
  try {
    res = await fetch(`${CORE_API_BASE_URL}${path}`, { ...options, headers });
  } catch {
    throw new ApiError("Could not reach the server. Check your connection and try again.", 0);
  }

  if (!res.ok) {
    const { message, code, details } = await parseErrorBody(res);
    throw new ApiError(message, res.status, code, details);
  }

  if (res.status === 204) return undefined as T;
  const text = await res.text();
  return text ? (JSON.parse(text) as T) : (undefined as T);
}

export const coreGet = <T>(path: string) => coreRequest<T>(path, { method: "GET" });
export const corePost = <T>(path: string, body?: unknown, auth = true) =>
  coreRequest<T>(path, { method: "POST", body: body !== undefined ? JSON.stringify(body) : undefined }, auth);
export const corePatch = <T>(path: string, body?: unknown) =>
  coreRequest<T>(path, { method: "PATCH", body: body !== undefined ? JSON.stringify(body) : undefined });
export const coreDelete = <T>(path: string) => coreRequest<T>(path, { method: "DELETE" });
