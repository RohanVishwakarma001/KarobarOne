/**
 * Thin backward-compatible shim over api-client.ts (the production network
 * engine: auto Bearer + tenant headers, mutex-style 401 refresh, typed
 * Pydantic-422 error parsing). Existing call sites keep their original
 * positional signatures — new code should import from "./api-client" directly.
 */
import { apiDelete, apiGet, apiPatch, apiPost, apiPut, withTenant as apiWithTenant, ApiError as ApiClientError } from "./api-client";

export const ApiError = ApiClientError;

export const coreGet = <T>(path: string, headers?: Record<string, string>) => apiGet<T>(path, { headers });

export const corePost = <T>(path: string, body?: unknown, auth = true, headers?: Record<string, string>) =>
  apiPost<T>(path, body, { auth, headers });

export const corePatch = <T>(path: string, body?: unknown, headers?: Record<string, string>) =>
  apiPatch<T>(path, body, { headers });

export const corePut = <T>(path: string, body?: unknown, headers?: Record<string, string>) =>
  apiPut<T>(path, body, { headers });

export const coreDelete = <T>(path: string, headers?: Record<string, string>) => apiDelete<T>(path, { headers });

export const withTenant = apiWithTenant;
