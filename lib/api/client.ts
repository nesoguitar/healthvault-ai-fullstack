"use client";

/**
 * Thin fetch wrapper around the FastAPI backend.
 *
 * - Attaches the bearer access token from localStorage automatically.
 * - On a 401, attempts a single silent refresh (via /auth/refresh) and
 *   retries the original request once before giving up and forcing a
 *   logout — this keeps the 30-minute access token invisible to the rest
 *   of the app.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const ACCESS_TOKEN_KEY = "healthvault_access_token";
const REFRESH_TOKEN_KEY = "healthvault_refresh_token";

export const tokenStorage = {
  getAccess: () => (typeof window === "undefined" ? null : localStorage.getItem(ACCESS_TOKEN_KEY)),
  getRefresh: () => (typeof window === "undefined" ? null : localStorage.getItem(REFRESH_TOKEN_KEY)),
  set: (access: string, refresh: string) => {
    localStorage.setItem(ACCESS_TOKEN_KEY, access);
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
  },
  clear: () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  },
};

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function refreshAccessToken(): Promise<boolean> {
  const refresh = tokenStorage.getRefresh();
  if (!refresh) return false;

  const res = await fetch(`${API_URL}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refresh }),
  });
  if (!res.ok) return false;

  const data = await res.json();
  tokenStorage.set(data.access_token, data.refresh_token);
  return true;
}

interface RequestOptions {
  method?: "GET" | "POST" | "PATCH" | "DELETE" | "PUT";
  body?: unknown;
  isForm?: boolean;
  skipAuth?: boolean;
}

export async function apiFetch<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, isForm = false, skipAuth = false } = options;

  const doFetch = async (): Promise<Response> => {
    const headers: Record<string, string> = {};
    if (!isForm) headers["Content-Type"] = "application/json";

    const token = tokenStorage.getAccess();
    if (token && !skipAuth) headers["Authorization"] = `Bearer ${token}`;

    return fetch(`${API_URL}${path}`, {
      method,
      headers,
      body: body ? (isForm ? (body as FormData) : JSON.stringify(body)) : undefined,
    });
  };

  let res = await doFetch();

  if (res.status === 401 && !skipAuth) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      res = await doFetch();
    } else {
      tokenStorage.clear();
      if (typeof window !== "undefined") window.location.href = "/login";
      throw new ApiError(401, "Session expired. Please sign in again.");
    }
  }

  if (res.status === 204) return undefined as T;

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    const message = data?.detail ?? (typeof data === "string" ? data : "Request failed");
    throw new ApiError(res.status, typeof message === "string" ? message : "Request failed");
  }

  return data as T;
}
