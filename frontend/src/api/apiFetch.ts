import { API_BASE_URL } from "./config";

let refreshPromise: Promise<boolean> | null = null;

async function refreshAccessToken(): Promise<boolean> {
  // If a refresh is already in flight (e.g. two requests 401'd at the
  // same moment), share the same attempt instead of firing two.
  if (!refreshPromise) {
    refreshPromise = fetch(`${API_BASE_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    })
      .then((res) => res.ok)
      .finally(() => {
        refreshPromise = null;
      });
  }
  return refreshPromise;
}

export async function apiFetch(
  path: string,
  options: RequestInit = {},
): Promise<Response> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    credentials: "include",
  });

  if (response.status !== 401) {
    return response;
  }

  const refreshed = await refreshAccessToken();
  if (!refreshed) {
    return response; // refresh failed too — caller will see the original 401
  }

  // Retry the original request once, now with a fresh access token cookie.
  return fetch(`${API_BASE_URL}${path}`, {
    ...options,
    credentials: "include",
  });
}
