import { GITHUB_API_BASE_URL } from "./config";

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
 * The backend has three coexisting error body shapes (see backend README §API
 * consistency): {error:{code,message}}, {detail:"..."} and {detail:{...}}.
 * Branch on shape rather than assuming one.
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
      return {
        message: typeof e.message === "string" ? e.message : "Request failed",
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

export async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${GITHUB_API_BASE_URL}${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...options.headers },
    });
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

export const apiGet = <T>(path: string) => apiRequest<T>(path, { method: "GET" });
export const apiPost = <T>(path: string, body?: unknown) =>
  apiRequest<T>(path, { method: "POST", body: body !== undefined ? JSON.stringify(body) : undefined });
export const apiPut = <T>(path: string, body?: unknown) =>
  apiRequest<T>(path, { method: "PUT", body: body !== undefined ? JSON.stringify(body) : undefined });
export const apiDelete = <T>(path: string) => apiRequest<T>(path, { method: "DELETE" });
